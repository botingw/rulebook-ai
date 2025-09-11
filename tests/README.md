# Rulebook-AI Test Suite

This directory contains integration tests for the rulebook-ai project. The tests focus on verifying that the package works correctly as a whole, particularly for its primary purpose of managing LLM rules and tools in third-party projects.

## Test Organization

### Integration Tests (`tests/integration/`)
- Tests that verify the package works correctly as a whole
- Tests that require external resources (filesystem, network)
- Installation verification test (`test_installation.py`)
- CLI tests (`test_manage_rules.py`)
- Core functionality tests (`test_core.py`)
- Tool integration test (`test_tools_integration.py`)

## Running Tests

### Using the Test Runner

The simplest way to run tests is using the provided test runner script:

```bash
# Set up the test environment
python tests/run_integration_tests.py --setup

# Run the integration tests
python tests/run_integration_tests.py --run
```

### Manual Test Setup

If you prefer to set up the test environment manually:

```bash
# Create a test environment
mkdir -p test_env
cd test_env
uv venv .venv

# Install the package in the test environment
uv pip install -e '..[dev]'

# Create a symlink for the tools module
cd .venv/lib/python*/site-packages
ln -sf ../../../../tool_starters tools
cd ../../../../..

# Run integration tests
cd test_env
uv run python -m pytest ../tests/integration -v
```

## Key Test Fixtures

- `temp_project_dir`: Creates a temporary project directory with mock rule sets, memory starters, and tool starters
- `tools_symlink`: Creates a symlink from `tools` to `tool_starters` in the site-packages directory
- `tmp_source_repo_root`: Creates a temporary source repository for CLI tests
- `script_runner`: Helper for running the CLI script in tests

## Best Practices

1. Integration tests should clean up after themselves
2. Use fixtures to set up and tear down test environments
3. Always install the package in development mode for testing
4. Use `uv` for environment management as specified in the modernization roadmap
5. Test against the installed package, not the source code directly

---

## Testing Strategy for External Dependencies

This section outlines the high-level strategy for testing features that interact with external systems, such as the Community Packs feature.

### `Integration Tests` vs. `Unit Tests`

Most tests in this suite, especially those involving file system I/O or external processes like `Git`, are classified as **`integration tests`**. Their purpose is to verify that our application correctly integrates with these external systems.

Pure `unit tests` would involve `mocking` these external dependencies to test a function's logic in complete isolation.

### Mocking Git Repositories: Local vs. Online

To test features like `packs add <slug>`, we need to simulate an external Git repository. The best practice, which we follow here, is to use **local Git repositories** created within the test suite (e.g., under `tests/fixtures/`).

We explicitly **avoid** using live, online `GitHub` repositories for our automated tests due to several first principles of good testing:

1.  **Speed**: Local operations are orders of magnitude faster than network operations. This keeps our test suite fast and our feedback loop short.
2.  **Stability & Repeatability**: Online tests are prone to failure due to network issues or `GitHub` service outages. These `flaky tests` reduce confidence in our test suite. Local tests are 100% repeatable.
3.  **Independence**: Local tests can be run anywhere, even offline, without requiring special authentication (`SSH keys`, `tokens`) or `CI` configuration.

### Mocking the Community Index

Similarly, when testing the `packs update` command, we use a local, mock `packs.json` file. Tests are configured to fetch this local file instead of a live production URL. This ensures the test environment is isolated, deterministic, and not affected by changes to the production index.
