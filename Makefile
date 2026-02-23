# Makefile for en.blog.alswl.com
# Image compression + CDN mechanism aligned with blog.alswl.com.
# CDN uses original domain (baseURL) so image URLs become absolute same-origin.

SHELL := /bin/bash
SED=$(shell which gsed || which sed)
HUGO := hugo
PUBLIC_FOLDER := public/
UPDATE_FOLDER := static/images/
# CP is ( in bash, solution from https://stackoverflow.com/a/40751291
CP := (

QSHELL := qshell
BUCKET = empty
# CDN: use original domain so /images/ -> https://en.blog.alswl.com/images/
CDN_HOST := https://en.blog.alswl.com/img
DOMAIN = en.blog.alswl.com
SITEMAP_URL = https://en.blog.alswl.com/sitemap.xml

.PHONY: build-production
build-production:
	HUGO_ENV=production $(HUGO)


.PHONY: cdn
cdn:
	# public/404.html is works as appendix, just like and 1=1 in sql
	@$(SED) -i 's#src="/images/#src="$(CDN_HOST)/#g' $(shell grep -Rl 'src="/images/' public) public/404.html
	@$(SED) -i 's#href="/images/#href="$(CDN_HOST)/#g' $(shell grep -Rl 'href="/images/' public) public/404.html
	
	@$(SED) -E -i 's#!\[([^]]+)\]\(/images/#!\[\1]\($(CDN_HOST)/#g' $(shell grep -RlE '!\[.+\]\$(CP)\/images\/' public) public/404.html

	# curl --silent "http://www.google.com/ping?sitemap=$(SITEMAP_URL)"
	# curl --silent "http://www.bing.com/webmaster/ping.aspx?siteMap=$(SITEMAP_URL)"
	@echo done

.PHONY: new
name = $(shell date +%Y-%m-%d)-new.md
new:
	$(HUGO) new "posts/$(name)" && open "content/posts/$(name)"

.PHONY: find-remote-images
find-remote-images:
	@echo images is remote:
	bash ./hack/find-remote-images.sh


.PHONY: resize-images-in-git-workdir
resize-images-in-git-workdir:
	@echo resize images in git worktree;
	bash ./hack/resize-images-in-git-workdir.sh

.PHONY: resize-images-to-public
resize-images-to-public:
	@echo resize images to public dir
	bash ./hack/resize-images.sh
