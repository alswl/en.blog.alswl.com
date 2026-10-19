PYTHON ?= python3
BLOG := $(PYTHON) -B -m scripts
.DEFAULT_GOAL := help

export BLOG_POST_NAME = $(name)
export BLOG_POST = $(post)
export BLOG_VERIFY_URL = $(url)
ifneq ($(base),)
export CHANGED_FILES_BASE = $(base)
endif

.PHONY: help init-theme install-git-hooks check-tools new-post preview-site fetch-banner-metadata format-markdown resize-images check-content build-site resize-images-to-public warm-cdn-images verify-publication build-cdn-site test-toolchain clean-build build-production cdn resize-images-in-git-workdir find-remote-images

help: ## Show commands, scope, and side effects
	@awk 'BEGIN {FS = ":.*## "} /^##@/ {printf "\n%s\n", substr($$0, 5)} /^[a-zA-Z0-9_-]+:.*## / {printf "  make %-28s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

##@ Environment
init-theme: ## Initialize the theme submodule
	git submodule sync -- themes/hugo-PaperMod
	git submodule update --init -- themes/hugo-PaperMod

install-git-hooks: ## Install lefthook Git hooks
	lefthook install

check-tools: ## Show installed Hugo, Prettier, and ImageMagick versions
	@$(BLOG) doctor

##@ Writing
new-post: ## Create a draft: name=YYYY-MM-DD-slug.md
	@$(BLOG) new

preview-site: ## Preview the site including drafts
	@$(BLOG) serve

fetch-banner-metadata: ## Fetch card image and description: post=content/posts/…
	@$(BLOG) enrich

##@ Before commit
format-markdown: ## Format changed Markdown without staging it
	@$(BLOG) format-markdown

resize-images: ## Shrink changed images to at most 1000×1000
	@$(BLOG) resize-images

check-content: ## Check changed content and all unused images
	@$(BLOG) check-content

build-site: ## Build the production site into public/
	@$(BLOG) build-site

resize-images-to-public: ## Generate deploy copies under static/img/
	@$(BLOG) resize-images-to-public

##@ Publication checks
warm-cdn-images: ## GET changed images from the CDN: base=<previous commit>
	@$(BLOG) warm-images

verify-publication: ## Retry checks for published pages and changed images
	@$(BLOG) verify

##@ Maintenance and CI
build-cdn-site: ## CI: build a temporary site and rewrite image URLs
	@$(BLOG) build-publication

test-toolchain: ## Run Python toolchain regression tests
	@$(BLOG) test

clean-build: ## Remove build artifacts
	@$(BLOG) clean

# Keep existing command names available.
build-production:
	@$(BLOG) build-production $(if $(filter cdn,$(MAKECMDGOALS)),--cdn,)
cdn: ; @:
resize-images-in-git-workdir: resize-images
find-remote-images: check-content
