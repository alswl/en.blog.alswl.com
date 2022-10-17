SHELL := /bin/bash
HUGO := hugo
QSHELL := qshell
PUBLIC_FOLDER := public/
UPDATE_FOLDER := static/images/
BUCKET = blog-alswl-com-202210
# CLOUDFRONT_ID := ABCDE12345678
CDN_HOST = https://d05fae.dijingchao.com
DOMAIN = en.blog.alswl.com
SITEMAP_URL = https://en.blog.alswl.com/sitemap.xml

# DEPLOY_LOG := deploy.log

.PHONY: build-production
build-production:
	HUGO_ENV=production $(HUGO)


.PHONY: sync-images
sync-images:
	echo "Copying files to server..."
	$(QSHELL) qupload2 --thread-count=5 --rescan-local --src-dir=$(shell pwd)/$(UPDATE_FOLDER) --bucket=$(BUCKET)


.PHONY: cdn
cdn: build-production
	# not works in github actions now
	# echo "Copying files to server..."
	# $(QSHELL) qupload2 --thread-count=5 --check-size --src-dir=$(shell pwd)/$(UPDATE_FOLDER) --bucket=$(BUCKET)

	sed -i 's#src="/images/#src="$(CDN_HOST)/#g' $(shell grep -Rl 'src="/images/' public)
	sed -i 's#href="/images/#href="$(CDN_HOST)/#g' $(shell grep -Rl 'href="/images/' public)


	# curl --silent "http://www.google.com/ping?sitemap=$(SITEMAP_URL)"
	# curl --silent "http://www.bing.com/webmaster/ping.aspx?siteMap=$(SITEMAP_URL)"

