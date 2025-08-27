# Contributing to Rulebook-AI

Thank you for considering contributing to Rulebook-AI! This document provides guidelines and instructions for contributing to this project.

## Development Environment Setup

We recommend using `uv` for managing your Python development environment:

```bash
# Install uv if you don't have it
curl -fsSL https://astral.sh/uv/install.sh | bash

# Create development environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies including development tools
uv sync

# Install pre-commit hooks
pre-commit install
```

## Project Structure

- `src/rulebook_ai/`: Core package code
- `rule_sets/`: AI ruleset templates organized by category
- `memory_starters/`: Starter templates for AI memory functionality
- `tool_starters/`: Starter templates for AI tool interactions
- `tests/`: Test suite

## Development Workflow

1. **Create a feature branch** from `main` for your changes
2. **Make your changes** following the coding conventions
3. **Run pre-commit checks** to ensure code quality: `pre-commit run --all-files`
4. **Run tests** to ensure functionality: `pytest`
5. **Submit a Pull Request** with a clear description of the changes

## Coding Conventions

- We use `ruff` and `mypy` for code quality enforcement
- Follow PEP 8 style guide for Python code
- Write docstrings for all modules, classes, and functions
- Include type hints for function parameters and return values
- Keep code modular and functions small and focused

## Testing

We use `pytest` for testing. Please include tests for new functionality:

```bash
# Run all tests
pytest

# Run specific tests
pytest tests/test_specific_file.py

# Run tests with coverage report
pytest --cov=rulebook_ai
```

## Documentation

- Update README.md with any necessary changes
- Document new features or changes in behavior
- Keep example code up-to-date

## Release Process

1. Update the version in `src/rulebook_ai/__init__.py`
2. Update the CHANGELOG.md file
3. Create a new GitHub release with appropriate tag
4. Ensure CI passes on the release tag

## Getting Help

If you have any questions or need assistance, please:
- Open an issue with a clear description
- Reach out to the maintainers

Thank you for contributing to Rulebook-AI!
