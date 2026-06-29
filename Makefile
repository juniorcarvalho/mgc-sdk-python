.DEFAULT_GOAL := help

.PHONY: help lint sync-dev ruff-check ruff-format-check ruff-format test

help:
	@printf "Targets available:\n"
	@printf "  make lint              Run the full lint workflow\n"
	@printf "  make sync-dev          Install development dependencies\n"
	@printf "  make ruff-check        Run Ruff lint checks\n"
	@printf "  make ruff-format-check Check Ruff formatting\n"
	@printf "  make ruff-format       Format code with Ruff\n"
	@printf "  make test              Run pytest test suite\n"

lint: sync-dev ruff-check ruff-format-check

sync-dev:
	uv sync --dev

ruff-check:
	uv run ruff check .

ruff-format-check:
	uv run ruff format . --check

ruff-format:
	uv run ruff format .

test: sync-dev
	uv run pytest
