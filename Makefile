.PHONY: help sync test test-spork test-python typecheck build dist check-dist clean

SPORK ?= spork
VENV_PYTHON := .venv/bin/python

help:
	@echo "sync         Install development dependencies"
	@echo "test         Run Spork, Python, and typing tests"
	@echo "build        Compile project sources"
	@echo "dist         Build wheel and source distribution"
	@echo "check-dist   Validate built distributions"
	@echo "clean        Remove environments and build artifacts"

sync:
	$(SPORK) sync --dev

test: test-spork test-python typecheck

test-spork:
	$(SPORK) test --spork-only

test-python:
	$(SPORK) test --python-only

typecheck:
	$(VENV_PYTHON) -m mypy tests/typing/usage.py

build:
	$(SPORK) build --clean

dist:
	$(SPORK) dist --clean

check-dist: dist
	$(VENV_PYTHON) -m twine check dist/*

clean:
	$(SPORK) clean --all
