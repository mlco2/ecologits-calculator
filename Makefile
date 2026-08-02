.PHONY: help install run test lint format check-ci check clean

# Default target when running 'make' with no arguments
help:
	@echo "Available commands:"
	@echo "  make install  - Install dependencies and setup pre-commit hooks"
	@echo "  make run      - Run the Streamlit application"
	@echo "  make test     - Run tests with pytest"
	@echo "  make lint     - Check code style with ruff and mypy"
	@echo "  make format   - Format code using ruff (mutating)"
	@echo "  make check-ci - Run read-only CI checks (ruff, format --check, mypy, tests)"
	@echo "  make check    - Alias for check-ci"
	@echo "  make clean    - Remove cache directories and temporary files"

install:
	uv sync --group dev
	./setup-hooks.sh

run:
	uv run streamlit run app.py

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check
	uv run mypy src

format:
	uv run ruff check --fix
	uv run ruff format

check-ci:
	uv run ruff check
	uv run ruff format --check
	uv run mypy src || true
	uv run pytest tests/ -v

check: check-ci

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache .mypy_cache .coverage
