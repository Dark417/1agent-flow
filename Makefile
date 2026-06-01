# Makefile for 1agent-flow — common tasks for the learning project.
# Run `make help` to see available targets.

.PHONY: help install-google install-amazon install smoke test clean

help:  ## Show this help
	@echo "Targets:"
	@echo "  install-google  Install deps for the Google ADK examples"
	@echo "  install-amazon  Install deps for the Amazon Strands examples"
	@echo "  install         Install both sets of deps"
	@echo "  smoke           Run dependency-free smoke tests (compile + structure)"
	@echo "  test            Alias for smoke"

install-google:  ## Install Google ADK example dependencies
	pip install -r requirements-google.txt

install-amazon:  ## Install Amazon Strands example dependencies
	pip install -r requirements-amazon.txt

install: install-google install-amazon  ## Install all dependencies

smoke:  ## Run the smoke tests (no API keys or SDKs required)
	python tests/smoke_test.py

test: smoke  ## Run the test suite

clean:  ## Remove Python caches
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name '.pytest_cache' -prune -exec rm -rf {} +
