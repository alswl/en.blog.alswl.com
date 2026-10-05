#!/usr/bin/env bash
# Verify Hugo build output before publishing.
#
# For each built page given as argument, checks that:
#   1. the page file exists
#   2. every same-origin image/asset URL (src/href) resolves to a real
#      file under public/
#   3. every internal content link (/YYYY/MM/..., /posts/..., etc.)
#      resolves to a built page
#
# External URLs, anchors, mailto/javascript links are skipped.
# Paths listed in $VERIFY_SKIP (space-separated) are ignored — used for
# known-missing assets (safari-pinned-tab.svg and apple-touch-icon.png are
# PaperMod default references, absent on the Chinese site too).
#
# Usage (run from repo root, AFTER `make build-production cdn`):
#   bash hack/verify-publish.sh \
#     public/2026/10/<slug>/index.html \
#     public/2026/09/<slug>/index.html
#
# Exits non-zero if any page, asset, or link is missing.

set -u

ORIGIN="https://en.blog.alswl.com"
VERIFY_SKIP="${VERIFY_SKIP:-safari-pinned-tab.svg apple-touch-icon.png}"
failed=0

for page in "$@"; do
  if [ ! -f "$page" ]; then
    echo "FAIL: page not found: $page"
    failed=1
    continue
  fi
  echo "== $page"
  urls=$(grep -ohE '(src|href)="[^"]*"' "$page" | sed -E 's/^[a-z]+="//; s/"$//' | sort -u)
  for u in $urls; do
    p=""
    case "$u" in
      "$ORIGIN"/*) p="${u#"$ORIGIN"}" ;;
      /*) p="$u" ;;
      *) continue ;;
    esac
    p="${p%%#*}"
    [ -n "$p" ] || continue
    case " $VERIFY_SKIP " in *" ${p##*/} "*) continue ;; esac
    case "$p" in
      *.png|*.jpg|*.jpeg|*.gif|*.webp|*.svg|*.ico|*.pdf|*.css|*.js|*.xml|*.woff|*.woff2)
        if [ ! -f "public$p" ]; then
          echo "MISSING asset: $u"
          failed=1
        fi
        ;;
      /2[0-9][0-9][0-9]/*|/posts/*|/about*|/archives*|/categories/*|/tags/*|/page/*)
        if [ ! -f "public${p%/}/index.html" ] && [ ! -f "public$p" ]; then
          echo "MISSING link: $u"
          failed=1
        fi
        ;;
    esac
  done
done

if [ "$failed" -ne 0 ]; then
  echo "VERIFY: FAILED"
  exit 1
fi
echo "VERIFY: OK"
