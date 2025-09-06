"""Integration tests for the rulebook_ai.core module."""

import os
import tempfile
import shutil
import json
import yaml
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
    packs_dir = project_root / "packs"
    test_pack_dir = packs_dir / "test-set"
    rules_dir = test_pack_dir / "rules"
    memory_dir = test_pack_dir / "memory_starters"
    tools_dir = test_pack_dir / "tool_starters"

    for d in [packs_dir, test_pack_dir, rules_dir, memory_dir, tools_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Create test files
    with open(rules_dir / "01-test-rule.md", "w") as f:
        f.write("# Test Rule\n\nThis is a test rule.")
    
    with open(memory_dir / "test-memory.md", "w") as f:
        f.write("# Test Memory\n\nThis is a test memory.")
    
    with open(tools_dir / "test-tool.md", "w") as f:
        f.write("# Test Tool\n\nThis is a test tool.")

    with open(test_pack_dir / "manifest.yaml", "w") as f:
        yaml.dump({"name": "test-set", "version": "1.2.3", "summary": "A test pack."}, f)
    
    # Initialize RuleManager with the test project root
    manager = RuleManager(project_root=project_root)
    # Point the manager to the mock packs directory
    manager.source_packs_dir = packs_dir
    return manager


def test_install(rule_manager, temp_dir):
    """Test the full installation workflow."""
    project_root = Path(temp_dir)
    target_dir = project_root / "target"
    target_dir.mkdir()
    
    result = rule_manager.install(
        rule_set="test-set", 
        project_dir=str(target_dir)
    )
    
    # Verify the end-to-end installation process worked
    assert result == 0
    assert (target_dir / "project_rules").exists()
    assert (target_dir / "memory").exists()
    assert (target_dir / "tools").exists()
    assert (target_dir / ".github" / "copilot-instructions.md").exists()

    # Verify .rulebook-ai structure
    rulebook_ai_dir = target_dir / ".rulebook-ai"
    assert (rulebook_ai_dir / "selection.json").is_file()
    assert (rulebook_ai_dir / "packs" / "test-set" / "manifest.yaml").is_file()
    assert (rulebook_ai_dir / "packs" / "test-set" / "file-map.json").is_file()

    with open(rulebook_ai_dir / "selection.json", "r") as f:
        selection = json.load(f)
    assert selection["packs"][0]["name"] == "test-set"
    assert selection["packs"][0]["version"] == "1.2.3"
