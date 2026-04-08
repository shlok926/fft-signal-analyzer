.PHONY: help install install-dev run dashboard cli test test-cov lint format clean benchmark docs
.PHONY: setup-pre-commit dev-setup

.DEFAULT_GOAL := help

help:
	@echo "FFT Signal Analyzer - Development Makefile"
	@echo ""
	@echo "Available commands:"
	@echo "  make install          Install dependencies via poetry"
	@echo "  make install-dev      Install dev dependencies"
	@echo "  make run              Launch Dash dashboard"
	@echo "  make cli              Show CLI help"
	@echo "  make test             Run all tests with coverage"
	@echo "  make test-cov         Run tests and generate coverage report"
	@echo "  make lint             Run ruff + mypy linting"
	@echo "  make format           Auto-format code with black + ruff"
	@echo "  make benchmark        Run performance benchmarks"
	@echo "  make clean            Remove cache/build files"
	@echo "  make docs             Build documentation"
	@echo "  make setup-pre-commit  Setup pre-commit hooks"
	@echo "  make dev-setup        Full development environment setup"

install:
	poetry install --no-root --no-dev

install-dev:
	poetry install

run: install-dev
	python -m fft_analyzer.ui.app

dashboard: install-dev
	poetry run fft-dashboard

cli: install-dev
	poetry run fft-analyzer --help

test: install-dev
	poetry run pytest tests/ -v

test-cov: install-dev
	poetry run pytest tests/ --cov=src/fft_analyzer --cov-report=html --cov-report=term-missing

lint: install-dev
	poetry run ruff check src/ tests/
	poetry run mypy src/fft_analyzer

format: install-dev
	poetry run black src/ tests/
	poetry run ruff check --fix src/ tests/

benchmark: install-dev
	poetry run python scripts/benchmark.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/

docs: install-dev
	@echo "Documentation build not yet implemented"

setup-pre-commit: install-dev
	poetry run pre-commit install
	poetry run pre-commit autoupdate
	@echo "Pre-commit hooks installed successfully"

dev-setup: install-dev setup-pre-commit
	@echo "Development environment setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  To run the dashboard: make run"
	@echo "  To run tests: make test"
	@echo "  To format code: make format"
	@echo "  To lint code: make lint"
