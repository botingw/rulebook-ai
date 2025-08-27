"""Unit test configuration and fixtures."""

import pytest
import os
import tempfile
import shutil
from pathlib import Path

# Path to project root for accessing test data
PROJECT_ROOT = Path(__file__).parent.parent.parent


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def test_data_dir():
    """Return path to test data directory."""
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir


@pytest.fixture
def mock_rule_manager_env(temp_dir):
    """
    Create a minimal environment for testing RuleManager methods.
    
    This fixture creates just enough directory structure and files
    to test RuleManager methods without involving the full package.
    """
    # Create a mock project structure in the temp directory
    project_root = Path(temp_dir)
    
    # Create source directories
    rule_sets_dir = project_root / "rule_sets"
    rule_sets_dir.mkdir()
    
    test_rule_set = rule_sets_dir / "test-set"
    test_rule_set.mkdir()
    
    # Create a test rule file
    with open(test_rule_set / "01-test-rule.md", "w") as f:
        f.write("# Test Rule\n\nThis is a test rule.")
    
    memory_dir = project_root / "memory_starters"
    memory_dir.mkdir()
    with open(memory_dir / "test-memory.md", "w") as f:
        f.write("# Test Memory\n\nThis is a test memory.")
    
    tools_dir = project_root / "tool_starters"
    tools_dir.mkdir()
    with open(tools_dir / "test-tool.md", "w") as f:
        f.write("# Test Tool\n\nThis is a test tool.")
    
    # Create a test env.example file
    with open(project_root / ".env.example", "w") as f:
        f.write("API_KEY=your-api-key-here")
    
    return project_root
