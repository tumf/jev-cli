UV ?= uv
UV_TOOL_BIN := $(shell $(UV) tool dir --bin)

.PHONY: install test build check

install:
	@command -v "$(UV)" >/dev/null || { echo "uv is required: https://docs.astral.sh/uv/" >&2; exit 1; }
	$(UV) tool install --force .
	"$(UV_TOOL_BIN)/jev-cli" --version

test:
	$(UV) run --python 3.13 -m unittest discover -s tests -v

build:
	$(UV) build

check: test build
