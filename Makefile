IMAGE_NAME ?= chimera-dev

.PHONY: setup docker-build test spec-check

setup:
	uv sync

docker-build:
	docker build -t $(IMAGE_NAME) .

docker-test: docker-build
	docker run --rm $(IMAGE_NAME)

test: docker-test

spec-check:
	uv run python scripts/spec_check.py
