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
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Project Structure

- `src/rulebook_ai/`: Core package code
- `src/rulebook_ai/rule_sets/`: AI ruleset templates organized by category
- `src/rulebook_ai/memory_starters/`: Starter templates for AI memory functionality
- `src/rulebook_ai/tool_starters/`: Starter templates for AI tool interactions
- `memory/`: The "Memory Bank" containing all project context and documentation.
- `tests/`: Test suite

## Project Context & Onboarding

To effectively contribute, both human developers and AI assistants need to understand the project's context. The `memory/` directory serves as the "Memory Bank" for this purpose.

### High-Level Context

For a broad understanding of the project's goals, architecture, and features, please refer to:

- **Product Requirement Document (PRD):** [`memory/docs/product_requirement_docs.md`](./memory/docs/product_requirement_docs.md) - Understand the "why" behind the project.
- **Architecture Design:** [`memory/docs/architecture.md`](./memory/docs/architecture.md) - Get an overview of the system's structure.
- **Feature Overview:** [`memory/docs/feature_tasks.md`](./memory/docs/feature_tasks.md) - See a high-level list and plan for project features.

### Low-Level & Implementation Context

For detailed technical information:

- **Detailed Feature Specs:** The [`memory/docs/features/`](./memory/docs/features/) directory contains detailed engineering design documents for individual features. This is the best place to understand the implementation details of a specific feature.
- **Technical Details:** [`memory/docs/technical.md`](./memory/docs/technical.md) - Find overall low-level design and technical specifications.
- **Design Analysis:** The [`memory/docs/analysis/`](./memory/docs/analysis/) directory contains deep-dive design documents for various components.
- **Source Code:** The `src/` directory is the ultimate source of truth for implementation.

## Contribution Workflow: Step-by-Step

Here is a more detailed guide to making a contribution, from idea to merged pull request.

**1. Fork & Clone the Repository**

First, fork the repository to your own GitHub account. Then, clone your fork to your local machine:

```bash
git clone https://github.com/botingw/rulebook-ai.git
cd rulebook-ai
```

It is also good practice to configure a remote for the original "upstream" repository to keep your fork's `main` branch up-to-date:

```bash
git remote add upstream https://github.com/botingw/rulebook-ai.git
git fetch upstream
```

**2. Set Up Your Environment**

Now that you have the code, follow the `Development Environment Setup` instructions to create a virtual environment and install all necessary dependencies.

**3. Find an Issue to Work On**

- The best place to start is the [GitHub Issues tab](https://github.com/botingw/rulebook-ai/issues).
- Look for issues tagged with `good first issue` if you are new, or `help wanted` for well-defined tasks.
- If you have a new idea, please open an issue first to discuss it with the maintainers.

**4. Create a Feature Branch**

Once you've chosen an issue, create a branch from the `main` branch. A good branch name is descriptive, like `feature/new-cli-command` or `fix/readme-typo`.

```bash
# Make sure your main branch is up-to-date with the upstream repository
git checkout main
git pull upstream main

# Create your feature branch
git checkout -b feature/your-new-feature
```

**5. Develop and Test Your Changes**

This is the core part of the contribution.

- **Understand the Context:** Before writing code, be sure to review the documents mentioned in the `Project Context & Onboarding` section.
- **Write Code:** Make your changes, following the `Coding Conventions`.
- **Write Tests:** This project uses `pytest`. Please add unit or integration tests for any new functionality you create. We aim for high test coverage. You can run the tests and see the coverage report with:
  ```bash
  uv run pytest --cov=rulebook_ai
  ```

**6. Ensure Code Quality and Style**

We use `pre-commit` to automatically check for code style, formatting, and common errors. Before you commit, run the checks:

```bash
pre-commit run --all-files
```
This will run tools like `ruff` and `mypy`. Fix any issues that it reports.

**7. Update Documentation**

If your changes impact how users interact with the project, please update the relevant documentation (like `README.md` or other guides).

**8. Commit and Push Your Changes**

Commit your changes with a clear and descriptive commit message.

```bash
git add .
git commit -m "feat: Add new CLI command for X"
git push origin feature/your-new-feature
```

**9. Submit a Pull Request (PR)**

- Go to the repository on GitHub. You will see a prompt to create a Pull Request from your new branch.
- Write a clear PR description:
    - Link to the issue you are solving (e.g., "Closes #123").
    - Explain *why* you made the change and *what* the change does.
    - Explain *what* context engineering approaches you use when develop and where are context docs related to your contribution.
- The project's CI pipeline will automatically run your tests. All checks must pass before your PR can be merged.
- A maintainer will review your code, and may ask for changes. Please be responsive to feedback!

## Coding Conventions

- We use `ruff` and `mypy` for code quality enforcement
- Follow PEP 8 style guide for Python code
- Write docstrings for all modules, classes, and functions
- Include type hints for function parameters and return values
- Keep code modular and functions small and focused

## Testing

We use `pytest` for testing. Please include tests for new functionality:

if not in virtual environment, need activate it first
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
Here are recommend commands:

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
