SHELL := /usr/bin/env sh
PY    := python

# For quiet builds, override with make Q= for verbose output
Q ?= @

# Where to fetch Happy-Hare's source from, and which ref to pin to. HAPPY_HARE_REF
# is a tracked file (one line) rather than a Makefile variable so bumping the pin
# is a one-line diff, not a Makefile edit. Tracks the 'v4' branch while v4 is still
# under active development - move to a tagged release once Happy-Hare starts
# cutting them, for reproducible regeneration.
HAPPY_HARE_REPO_URL ?= https://github.com/moggieuk/Happy-Hare.git
HAPPY_HARE_REF      := $(shell cat HAPPY_HARE_REF)

# Where the fetched checkout lands - gitignored, never committed here. Override to
# point at a checkout you already have for fast local iteration, e.g.:
#   HAPPY_HARE_SRC=/path/to/Happy-Hare make shots
HAPPY_HARE_SRC ?= $(CURDIR)/.happy-hare-src

# Stamp files avoid Make target parsing issues when workspace paths contain
# spaces or '#'.
SOURCE_FETCH_STAMP := .make/source-fetched.stamp
VENV_READY_STAMP   := .make/venv-ready.stamp

# Shared venv for doc tooling (pyte, Pillow, zensical - see doc_tools/requirements.txt)
VENV     ?= venv
VENV_PY  := $(VENV)/bin/python
BOOTSTRAP_PY := $(if $(shell command -v $(PY) 2>/dev/null),$(PY),python3)

.PHONY: fetch-source clean-source shots command_reference docs docs_build docs_preview


###########################
##### Source fetching #####
###########################

# Only 'shots' and 'command_reference' need this - they read Happy-Hare's source
# tree directly (extras/mmu/**, installer/Kconfig*, installer/lib/kconfiglib).
# 'docs'/'docs_build'/'docs_preview' only render already-committed doc/*.md and
# never touch this, which is also why the CI deploy workflow doesn't fetch it.
#
# Tries a fast shallow clone first (works for a branch or tag name); falls back to
# a full clone + checkout, which is needed if HAPPY_HARE_REF is ever pinned to an
# arbitrary commit SHA rather than a branch/tag.
$(SOURCE_FETCH_STAMP):
	$(Q)echo "Fetching Happy-Hare @ $(HAPPY_HARE_REF) into $(HAPPY_HARE_SRC)"
	$(Q)mkdir -p "$(dir $@)"
	$(Q)test -d "$(HAPPY_HARE_SRC)/.git" || \
	    (git clone --depth 1 --branch "$(HAPPY_HARE_REF)" "$(HAPPY_HARE_REPO_URL)" "$(HAPPY_HARE_SRC)" 2>/dev/null || \
	    (git clone "$(HAPPY_HARE_REPO_URL)" "$(HAPPY_HARE_SRC)" && cd "$(HAPPY_HARE_SRC)" && git checkout "$(HAPPY_HARE_REF)")
	$(Q)touch "$@"

fetch-source: $(SOURCE_FETCH_STAMP)

clean-source:
	$(Q)rm -rf "$(HAPPY_HARE_SRC)"
	$(Q)rm -f "$(SOURCE_FETCH_STAMP)"


#######################
##### Python venv #####
#######################

$(VENV_READY_STAMP): doc_tools/requirements.txt
	$(Q)mkdir -p "$(dir $@)"
	$(Q)if [ ! -x "$(VENV_PY)" ]; then echo "Creating virtualenv in $(VENV)/"; "$(BOOTSTRAP_PY)" -m venv "$(VENV)"; fi
	$(Q)"$(VENV_PY)" -m pip install --quiet --disable-pip-version-check -r "$<"
	$(Q)touch "$@"


#################################
##### Documentation targets #####
#################################

# Documentation screenshots: runs a real menuconfig session against the fetched
# Happy-Hare checkout and renders its screens to per-page image folders under
# doc/ - see doc_tools/README.md. Pass flags through ARGS, e.g.:
#   make shots ARGS='--list'
#   make shots ARGS='--only feature-espooler'
shots: fetch-source $(VENV_READY_STAMP)
	$(Q)HAPPY_HARE_SRC="$(HAPPY_HARE_SRC)" "$(VENV_PY)" -m doc_tools.$(if $(CAPTURE),capture,shots) $(ARGS)

# Regenerates doc/Command-Reference.md and doc/Dev-Command-Reference.md from
# the real HELP_BRIEF/HELP_PARAMS/HELP_SUPPLEMENT text in the fetched
# checkout's extras/mmu/** - stdlib only, no venv needed.
command_reference: fetch-source
	$(Q)HAPPY_HARE_SRC="$(HAPPY_HARE_SRC)" "$(PY)" -m doc_tools.gen_command_reference

# Builds and serves the doc/ site at http://127.0.0.1:8000 with live reload -
# rebuilds on every source change, so this is the one to leave running while
# writing a page. Reads mkdocs.yml at the repo root. Needs no Happy-Hare source -
# it only renders the doc/*.md and images already committed in this repo.
docs: $(VENV_READY_STAMP)
	$(Q)"$(VENV)/bin/zensical" serve

# Builds the static site into ./site - what actually gets published (and what
# the CI deploy workflow runs).
docs_build: $(VENV_READY_STAMP)
	$(Q)"$(VENV)/bin/zensical" build

# Serves the already-built ./site as plain static files - no rebuild, no live
# reload. This is what GitHub Pages (or any static host) actually does with the
# site, so it's the one to use for a final check before publishing.
docs_preview: docs_build
	$(Q)echo "Serving ./site at http://127.0.0.1:8000 (Ctrl-C to stop)"
	$(Q)cd site && $(PY) -m http.server 8000
