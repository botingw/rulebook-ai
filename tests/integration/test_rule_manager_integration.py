"""Integration tests for the rulebook_ai.core module."""

import os
import tempfile
import shutil
from pathlib import Path
import pytest

# Import RuleManager using standard import - testing installed package
from rulebook_ai.core import RuleManager


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def rule_manager(temp_dir):
    """Create a RuleManager instance for testing."""
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
    
    # Initialize RuleManager with the test project root
    manager = RuleManager(project_root=project_root)
    return manager


def test_install(rule_manager, temp_dir):
    """Test the full installation workflow."""
    project_root = Path(temp_dir)
    target_dir = project_root / "target"
    target_dir.mkdir()
    
    result = rule_manager.install(
        rule_set="test-set", 
        project_dir=str(target_dir),
        include_copilot=True
    )
    
    # Verify the end-to-end installation process worked
    assert result == 0
    assert (target_dir / "project_rules").exists()
    assert (target_dir / "memory").exists()
    assert (target_dir / "tools").exists()
    assert (target_dir / ".github" / "copilot-instructions.md").exists()
