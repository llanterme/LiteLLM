.PHONY: help install setup run test clean format lint check env

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies with Poetry"
	@echo "  make setup      - Set up the development environment"
	@echo "  make run        - Run the CLI with a default topic"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Clean up cache and temporary files"
	@echo "  make format     - Format code with black"
	@echo "  make lint       - Lint code with flake8"
	@echo "  make check      - Run format and lint checks"
	@echo "  make env        - Copy .env.example to .env"

install:
	poetry install

setup: install env
	@echo "✅ Development environment is ready!"
	@echo "Please edit .env file with your API keys"

env:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Created .env file from template"; \
		echo "⚠️  Please edit .env with your API keys"; \
	else \
		echo "✅ .env file already exists"; \
	fi

run:
	@if [ -z "$(TOPIC)" ]; then \
		poetry run python -m src.cli "The impact of AI on education"; \
	else \
		poetry run python -m src.cli "$(TOPIC)"; \
	fi

run-ollama:
	poetry run python -m src.cli "$(TOPIC)" --provider ollama

run-openai:
	poetry run python -m src.cli "$(TOPIC)" --provider openai

run-anthropic:
	poetry run python -m src.cli "$(TOPIC)" --provider anthropic

run-gemini:
	poetry run python -m src.cli "$(TOPIC)" --provider gemini

test:
	poetry run pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov

format:
	poetry run black src/ tests/

lint:
	poetry run flake8 src/ tests/ --max-line-length=100

check: format lint

dev-install:
	poetry add --group dev black flake8 pytest pytest-asyncio

shell:
	poetry shell

update:
	poetry update

build:
	poetry build