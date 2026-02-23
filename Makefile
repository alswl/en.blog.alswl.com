# Makefile for en.blog.alswl.com
# Aligned with reference blog (blog.alswl.com); no CDN target (images use original links).

SHELL := /bin/bash
HUGO := hugo
PUBLIC_FOLDER := public/

.PHONY: build-production
build-production:
	HUGO_ENV=production $(HUGO)
