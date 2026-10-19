"""Offline workflow coverage for tool lookup, banners and CDN artifacts."""

import io
import json
import tempfile
import unittest
from email.message import Message
from pathlib import Path
from unittest import mock
from urllib.error import URLError

from scripts import banners, publishing, runtime


class ToolResolutionTests(unittest.TestCase):
    def test_uses_installed_tools_without_version_files(self):
        with tempfile.TemporaryDirectory() as directory:
            tools = runtime.Tools(Path(directory))
            with mock.patch.object(
                runtime.shutil, "which", return_value="/usr/bin/hugo"
            ):
                self.assertEqual(tools.resolve("hugo"), "/usr/bin/hugo")

    def test_local_prettier_precedes_global_install(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            binary = root / "node_modules/.bin/prettier"
            binary.parent.mkdir(parents=True)
            binary.write_text("#!/bin/sh\necho 3.9.6\n")
            binary.chmod(0o755)
            with mock.patch.object(
                runtime.shutil, "which", return_value="/usr/bin/prettier"
            ):
                self.assertEqual(runtime.Tools(root).resolve("prettier"), str(binary))

    def test_missing_tool_reports_install_documentation(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            mock.patch.object(runtime.shutil, "which", return_value=None),
        ):
            with self.assertRaisesRegex(ValueError, "docs/dev/README.md"):
                runtime.Tools(Path(directory)).resolve("hugo")


class BannerWorkflowTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        patch = mock.patch.object(banners, "ROOT", self.root)
        patch.start()
        self.addCleanup(patch.stop)
        self.post = self.root / "2026-10-19-test.md"
        self.post.write_text('[example](https://example.com/page "!banner")\n')

    def response(self, body, url, content_type):
        response = io.BytesIO(body)
        response.geturl = lambda: url
        response.headers = Message()
        response.headers["Content-Type"] = content_type
        return response

    def test_fetch_update_cache_and_recover_missing_image(self):
        page = b'<meta property="og:image" content="/cover.png"><meta property="og:description" content="hello  &amp; world">'

        def fetch(request, **kwargs):
            url = request.full_url
            return self.response(
                page if url.endswith("/page") else b"image bytes",
                url,
                "text/html; charset=utf-8" if url.endswith("/page") else "image/png",
            )

        with mock.patch.object(banners, "urlopen", side_effect=fetch) as network:
            self.assertTrue(banners.update_file(self.post))
            self.assertEqual(network.call_count, 2)
            self.assertIn("hello &amp; world", self.post.read_text())
            images = list((self.root / "static/images/202610").glob("*.png"))
            self.assertEqual(len(images), 1)
            before = self.post.read_bytes()
            self.assertTrue(banners.update_file(self.post))
            self.assertEqual(network.call_count, 2)
            self.assertEqual(self.post.read_bytes(), before)
            images[0].unlink()
            self.assertTrue(banners.update_file(self.post))
            self.assertEqual(network.call_count, 3)
            self.assertEqual(images[0].read_bytes(), b"image bytes")

    def test_failed_page_refresh_preserves_existing_marker(self):
        before = self.post.read_bytes()
        with mock.patch.object(banners, "urlopen", side_effect=URLError("offline")):
            self.assertFalse(banners.update_file(self.post, refresh=True))
        self.assertEqual(self.post.read_bytes(), before)

    def test_fenced_examples_do_not_fetch(self):
        self.post.write_text("```markdown\n" + self.post.read_text() + "```\n")
        before = self.post.read_bytes()
        with mock.patch.object(banners, "urlopen") as network:
            self.assertTrue(banners.update_file(self.post))
            network.assert_not_called()
        self.assertEqual(self.post.read_bytes(), before)

    def test_youtube_oembed_fallback_omits_generic_description(self):
        with mock.patch.object(
            banners,
            "fetch",
            side_effect=[
                (
                    b'<meta name="description" content="generic service">',
                    "https://www.youtube.com/watch?v=x",
                    "text/html",
                    "utf-8",
                ),
                (
                    json.dumps(
                        {"thumbnail_url": "https://img.example/video.jpg"}
                    ).encode(),
                    "https://www.youtube.com/oembed",
                    "application/json",
                    "utf-8",
                ),
            ],
        ):
            result = banners.page_metadata("https://youtu.be/x")
        self.assertEqual(result["image_url"], "https://img.example/video.jpg")
        self.assertEqual(result["description"], "")


class ArtifactWorkflowTests(unittest.TestCase):
    def test_bulk_conversion_preserves_binary_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sources = {
                "index.html": '<img src="/images/a.png">',
                "rss.xml": "<rss>&lt;img src=&quot;/images/a.png&quot;&gt;</rss>",
                "post.md": "![a](/images/a.png)",
                "index.json": '{"image":"/images/a.png"}',
            }
            for name, source in sources.items():
                (root / name).write_text(source)
            binary = b"\x89PNG\xff/images/a.png"
            (root / "a.png").write_bytes(binary)
            config = {
                "site_url": "https://blog.example",
                "cdn_url": "https://cdn.example",
            }
            self.assertEqual(publishing.cdn_artifacts(root, config), 4)
            for name in sources:
                self.assertIn("https://cdn.example/a.png", (root / name).read_text())
            self.assertEqual(
                json.loads((root / "index.json").read_text())["image"],
                "https://cdn.example/a.png",
            )
            self.assertEqual((root / "a.png").read_bytes(), binary)
            self.assertEqual(publishing.cdn_artifacts(root, config), 0)
