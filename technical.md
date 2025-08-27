# Modern Python Development Learning Guide

**Using rulebook-ai as a Learning Example**

This repository demonstrates modern Python development practices and serves as a comprehensive learning resource for developers. By studying this codebase, you'll learn industry-standard approaches to Python project structure, dependency management, testing, and development workflows.

## 🔍 Learning Checklist

Track your progress through the following modern Python development concepts:

- [ ] **Modern Python Project Structure (src layout)**
- [ ] **Declarative Project Configuration with pyproject.toml**
- [ ] **Dependency Management with uv/uvx**
- [ ] **Clean Code Architecture and Separation of Concerns**
- [ ] **Type Safety with Python Type Annotations**
- [ ] **Modern File Operations with pathlib**
- [ ] **CLI Development with Entry Points**
- [ ] **Integration Testing with tox**
- [ ] **Code Quality Tools Integration**
- [ ] **Error Handling Best Practices**
- [ ] **Package Distribution and CLI Development**

---

## 📋 What rulebook-ai Does

**rulebook-ai** is a Python package that manages LLM (Large Language Model) rulesets and assistant configurations for development teams. It helps developers:

- **Install and manage rule templates** for different AI coding assistants (Cursor, Windsurf, GitHub Copilot, etc.)
- **Synchronize rules across projects** to maintain consistency
- **Organize memory banks and tool starters** for AI-assisted development
- **Provide CLI commands** for easy rule management in any project

### Core Functionality
- **Rule Management**: Install, sync, and clean rule sets for AI assistants
- **Memory Banking**: Organize and share knowledge bases across projects  
- **Tool Integration**: Manage reusable tools and utilities
- **CLI Interface**: Professional command-line interface for all operations

### Target Users
- Development teams using AI coding assistants
- Individual developers wanting consistent AI configurations
- Organizations standardizing AI-assisted development practices

---

## 🏗️ Project Structure Overview

### Directory Layout
```
rulebook-ai/
├── src/rulebook_ai/          # Main package (src layout)
│   ├── __init__.py           # Package initialization
│   ├── __main__.py           # Allow python -m rulebook_ai
│   ├── core.py               # Business logic (RuleManager class)
│   └── cli.py                # Command-line interface
├── tests/integration/        # Integration tests only
│   ├── conftest.py           # Shared test fixtures
│   ├── test_package_installation.py
│   ├── test_rule_manager.py
│   ├── test_cli_commands.py
│   └── test_tools_integration.py
├── rule_sets/                # Rule templates for AI assistants
├── memory_starters/          # Memory bank templates
├── tool_starters/            # Tool integration examples
├── pyproject.toml            # Project configuration
└── README.md                 # Project documentation
```

---

## 📚 Learning Modules

### 1. Modern Python Project Structure (src layout)

**Why it matters**: The `src/` layout separates source code from tests and configuration, prevents import issues during development, and ensures tests run against the installed package rather than the source code directly.

**Implementation in rulebook-ai**:
- Package code is in `src/rulebook_ai/` rather than at the repository root
- Tests import from the installed package, not directly from source
- Installation with `-e` makes development changes immediately available

**Code example**:
```python
# Project structure ensures imports work like this:
from rulebook_ai.core import RuleManager  # Clean import path
```

**Key advantages**:
- Prevents accidental imports from the wrong version of the code
- Forces tests to use the installed package as end users would
- Makes packaging more reliable and deployment-like during testing
- Reduces "works on my machine" issues

### 2. Declarative Project Configuration with pyproject.toml

**Why it matters**: PEP 621 brought standardized, declarative project metadata to Python, eliminating the need for executable `setup.py` files and consolidating configuration in one place.

**Implementation in rulebook-ai**:
- All project metadata, dependencies, and build settings in one file
- Development dependencies specified as optional extras
- Tool configurations (pytest, mypy, ruff) in the same file
- Entry points configured declaratively

**Code example**:
```toml
[project]
name = "rulebook-ai"
version = "0.1.0"
description = "Management system for LLM rules and instructions"
requires-python = ">=3.8"
dependencies = [
    "rich>=10.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.5",
    "mypy>=1.5.1",
    "ruff>=0.0.292",
    "tox>=4.11.3",
]

[project.scripts]
rulebook-ai = "rulebook_ai.cli:main"

[tool.pytest]
testpaths = ["tests"]
```

**Key advantages**:
- Single source of truth for project configuration
- Standard format understood by modern tools
- Supports both traditional and modern build systems
- Declarative rather than imperative configuration

### 3. Dependency Management with uv/uvx

**Why it matters**: Traditional Python package managers can be slow and introduce inconsistencies. Modern tools like `uv` provide faster, more reliable dependency resolution and installation.

**Implementation in rulebook-ai**:
- All dependencies installed with `uv pip install`
- Development environment created with `uv venv`
- Uses `uv pip install -e '.[dev]'` for development installation

**Code example**:
```bash
# Instead of traditional pip:
$ uv venv
$ source .venv/bin/activate
$ uv pip install -e '.[dev]'
```

**Key advantages**:
- 10-100x faster than pip for large dependency graphs
- Consistent dependency resolution
- Lockfile support for reproducible environments
- Better performance and reliability

### 4. Clean Code Architecture and Separation of Concerns

**Why it matters**: Separating business logic from interface code improves testability, maintainability, and allows multiple interfaces to the same core functionality.

**Implementation in rulebook-ai**:
- `core.py` contains the `RuleManager` class with all business logic
- `cli.py` provides only the command-line interface
- CLI delegates to core functions with minimal logic of its own

**Code example**:
```python
class RuleManager:
    """Manages the installation and synchronization of AI rules and related files."""
    
    def install(self, rule_set: str = DEFAULT_RULE_SET, 
               target_dir: Optional[str] = None,
               clean_first: bool = False) -> bool:
        """Install a rule set with full type safety."""
        # Implementation...

# In cli.py:
def handle_install(args: argparse.Namespace) -> int:
    """Handle the 'install' command."""
    manager = RuleManager()
    success = manager.install(
        rule_set=args.rule_set,
        target_dir=args.project_dir,
        clean_first=args.clean
    )
    return 0 if success else 1
```

**Key advantages**:
- Business logic can be tested independently of the interface
- Multiple interfaces can share the same core functionality
- Changes to the interface don't affect core logic
- Better code organization and maintainability

### 5. Type Safety with Python Type Annotations

**Why it matters**: Type hints provide documentation, enable static analysis, and catch type-related bugs before runtime.

**Implementation in rulebook-ai**:
- All functions and methods have complete type annotations
- Complex return types specified with `List`, `Tuple`, and other type hints
- Optional parameters properly annotated with `Optional`

**Code example**:
```python
def get_ordered_source_files(self, source_dir: Path) -> List[Tuple[Path, str]]:
    """Get ordered list of source files with their relative paths."""
    result = []
    for file_path in sorted(source_dir.glob('**/*')):
        if file_path.is_file():
            rel_path = file_path.relative_to(source_dir)
            result.append((file_path, str(rel_path)))
    return result
```

**Key advantages**:
- Self-documenting code with clear input/output types
- Static type checking with mypy catches errors early
- Better IDE autocompletion and code navigation
- Enables refactoring with confidence

### 6. Modern File Operations with pathlib

**Why it matters**: Traditional `os.path` string operations are error-prone and difficult to read. The `pathlib` module provides an object-oriented API for path operations.

**Implementation in rulebook-ai**:
- All file operations use `pathlib.Path` instead of string paths
- Path joining uses the `/` operator for readability
- Path methods used for existence checks, file/directory operations
- Relative path operations use `relative_to`

**Code example**:
```python
# Instead of:
# os.path.join(os.path.dirname(__file__), '..', '..', 'rule_sets')

# rulebook-ai uses:
source_dir = Path(__file__).parent.parent.parent / 'rule_sets'

# And for file operations:
if target_path.exists():
    backup_path = target_path.with_suffix(target_path.suffix + '.backup')
    shutil.copy2(target_path, backup_path)
    
# Creating directories:
target_path.parent.mkdir(parents=True, exist_ok=True)
```

**Key advantages**:
- More readable, intuitive path operations
- Object-oriented approach prevents string manipulation errors
- Cross-platform compatibility built in
- Comprehensive API for common file operations

### 7. CLI Development with Entry Points

**Why it matters**: Professional command-line tools should be installed system-wide and available directly from the command line without Python-specific invocation.

**Implementation in rulebook-ai**:
- Entry point defined in pyproject.toml for the `rulebook-ai` command
- CLI module has proper argument parsing and subcommands
- Command handlers follow a consistent pattern
- Returns proper exit codes for script integration

**Code example**:
```toml
# In pyproject.toml:
[project.scripts]
rulebook-ai = "rulebook_ai.cli:main"
```

```python
# In cli.py:
def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parsed_args = parse_args(args)
    
    # Command dispatcher
    handlers = {
        "install": handle_install,
        "sync": handle_sync,
        "clean-rules": handle_clean_rules,
        "clean-all": handle_clean_all,
        "list-rules": handle_list_rules,
        "doctor": handle_doctor
    }
    
    if parsed_args.command in handlers:
        return handlers[parsed_args.command](parsed_args)
    else:
        print("No command specified. Use --help for usage information.")
        return 1
```

**Key advantages**:
- Tool available as `rulebook-ai` after installation
- Professional command-line interface with subcommands
- Follows Unix conventions for exit codes
- Seamless integration with shell scripts

### 8. Integration Testing with tox

**Why it matters**: Testing should verify that the package works correctly when installed, not just that the source code works in development.

**Implementation in rulebook-ai**:
- Uses tox for isolated test environments
- Tests run against the installed package
- Coverage reporting configured in pyproject.toml
- Integration tests focus on real-world usage patterns

**Code example**:
```toml
# In pyproject.toml:
[tool.tox]
legacy_tox_ini = """
[tox]
toxworkdir = {toxinidir}/test_env
isolated_build = True
envlist = py3

[testenv]
# No usedevelop - we'll install explicitly in commands_pre
# No extras needed - all dependencies explicitly listed in deps
deps =
    pytest>=8.0.0
    pytest-asyncio>=0.23.5
    pytest-cov>=4.1.0
    pytest-mock>=3.12.0
    respx>=0.20.2
    darglint>=1.8.1

commands_pre =
    python -c "import sys; print(f'Python: {sys.executable}')"
    pip install -e .
    python -c "import rulebook_ai; print(f'✅ Package installed: rulebook-ai v{rulebook_ai.__version__}')"
    python -c "from rulebook_ai.core import RuleManager; print('✅ Core module importable')"

commands =
    python -m pytest tests/ -v -s --cov=rulebook_ai --cov-report=term-missing
    python -m pytest tests/integration -v -s --cov=rulebook_ai --cov-append --no-cov-on-fail
"""
```

**Key advantages**:
- Tests in isolated environments
- Verifies the package installs correctly
- Tests the actual package as users would use it
- Prevents "works in development only" issues

### 9. Code Quality Tools Integration

**Why it matters**: Automated tools for linting, formatting, and type checking ensure consistent code quality and catch issues early.

**Implementation in rulebook-ai**:
- ruff for linting and formatting
- mypy for type checking
- pytest for testing
- All configured in pyproject.toml

**Code example**:
```toml
[tool.ruff]
target-version = "py38"
line-length = 100
select = ["E", "F", "I", "N", "UP", "YTT", "ANN"]
ignore = ["ANN101"]

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = false
```

**Key advantages**:
- Consistent code style across the project
- Early detection of common issues
- Reduces code review overhead
- Improves maintainability and readability

### 10. Error Handling Best Practices

**Why it matters**: Robust error handling separates error detection from reporting and ensures users get actionable information.

**Implementation in rulebook-ai**:
- Core functions return boolean success indicators
- Detailed error messages logged but not directly printed
- CLI formats errors appropriate for the command line
- User-facing messages are actionable

**Code example**:
```python
def copy_file(self, source: Path, target: Path, backup: bool = True) -> bool:
    """Copy file with backup and conflict resolution."""
    try:
        if target.exists() and backup:
            # Create backup before overwriting
            backup_path = target.with_suffix(target.suffix + '.backup')
            shutil.copy2(target, backup_path)
        
        # Ensure parent directory exists
        target.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy with metadata preservation
        shutil.copy2(source, target)
        return True
    except (OSError, PermissionError) as e:
        self._log_error(f"Failed to copy {source} to {target}: {e}")
        return False
```

**Key advantages**:
- Clean separation of concerns in error handling
- Consistent error reporting pattern
- Makes testing error conditions easier
- Provides meaningful feedback to users

### 11. Package Distribution and CLI Development

**Why it matters**: Professional Python packages should be easy to install and use, with proper entry points and documentation.

**Implementation in rulebook-ai**:
- Package configured for PyPI distribution
- Entry points for command-line tools
- Comprehensive README and documentation
- Clean import structure

**Code example**:
```python
# In __main__.py:
"""
Allows running the package directly as `python -m rulebook_ai`.
"""

from .cli import main

if __name__ == "__main__":
    main()
```

**Key advantages**:
- Users can install with standard tools (`pip install rulebook-ai`)
- Command-line tools available system-wide
- Clear documentation for users and contributors
- Professional package distribution

---

## 💡 Key Insights for Modern Python Development

1. **src/ layout prevents common import issues** and encourages proper packaging
2. **Integration tests provide more value** than extensive unit test suites for many projects
3. **Tool integration in pyproject.toml** creates a cohesive development experience
4. **uv and tox together** provide fast, reliable development and testing workflows
5. **Entry points make CLI tools professional** and easy to distribute
6. **Type annotations improve maintainability** and catch errors before runtime
7. **pathlib simplifies file operations** and improves cross-platform compatibility
8. **Clean separation of concerns** makes code more testable and maintainable
9. **Declarative configuration** reduces boilerplate and improves consistency
10. **Modern error handling** separates error detection from reporting

---

## 📝 Next Steps and Further Learning

After mastering these concepts, consider exploring:

- **Property-based testing** with hypothesis for more thorough test cases
- **Async Python** for concurrent operations and API development
- **Container-based development** for even more isolation and reproducibility
- **CI/CD pipeline integration** for automated testing and deployment
- **Documentation generation** with Sphinx or MkDocs
- **API development** with FastAPI or Flask for web services
- **Package versioning strategies** for sustainable development
