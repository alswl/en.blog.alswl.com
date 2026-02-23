# Makefile for en.blog.alswl.com
# Image compression + CDN mechanism aligned with blog.alswl.com.
# CDN uses original domain (baseURL) so image URLs become absolute same-origin.

SHELL := /bin/bash
SED := $(shell which gsed 2>/dev/null || which sed)
HUGO := hugo
PUBLIC_FOLDER := public/
UPDATE_FOLDER := static/images/
# CP is ( in bash, for sed pattern !\[.+\]$(CP)/images/
CP := (

# CDN: use original domain so /images/ -> https://en.blog.alswl.com/images/
CDN_HOST := https://en.blog.alswl.com

.PHONY: build-production
build-production:
	HUGO_ENV=production $(HUGO)

.PHONY: cdn
cdn:
	@$(SED) -i.bak 's#src="/images/#src="$(CDN_HOST)/#g' $(shell grep -Rl 'src="/images/' public 2>/dev/null || true) public/404.html 2>/dev/null || true
	@$(SED) -i.bak 's#href="/images/#href="$(CDN_HOST)/#g' $(shell grep -Rl 'href="/images/' public 2>/dev/null || true) public/404.html 2>/dev/null || true
	@$(SED) -E -i.bak 's#!\[([^]]+)\]\(/images/#![\1]($(CDN_HOST)/#g' $(shell grep -RlE '!\[.+\]\(/images/' public 2>/dev/null || true) public/404.html 2>/dev/null || true
	@find public -name '*.bak' -delete 2>/dev/null || true
	@echo cdn done

.PHONY: sync-images
sync-images:
	@echo "en.blog: images served from same origin; sync-images no-op unless you set S3 bucket."
	@# aws s3 sync --endpoint-url ... ./$(UPDATE_FOLDER) s3://your-bucket/

.PHONY: resize-images-in-git-workdir
resize-images-in-git-workdir:
	@echo resize images in git worktree
	@bash ./hack/resize-images-in-git-workdir.sh


.PHONY: resize-images-to-public
resize-images-to-public:
	@echo resize images to public dir
	bash ./hack/resize-images.sh
