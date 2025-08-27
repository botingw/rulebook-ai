"""Unit tests for the rulebook_ai.core.RuleManager class."""

import pytest
from pathlib import Path

# Import RuleManager using standard import - testing installed package
from rulebook_ai.core import RuleManager


@pytest.fixture
def rule_manager(mock_rule_manager_env):
    """Create a RuleManager instance for testing."""
    # Initialize RuleManager with the test project root
    manager = RuleManager(project_root=mock_rule_manager_env)
    return manager


def test_list_rules(rule_manager):
    """Test the list_rules method."""
    rule_sets = rule_manager.list_rules()
    assert "test-set" in rule_sets


def test_get_ordered_source_files(rule_manager, temp_dir):
    """Test the get_ordered_source_files method."""
    project_root = Path(temp_dir)
    test_dir = project_root / "test_dir"
    test_dir.mkdir()
    
    # Create some test files
    with open(test_dir / "01-first.md", "w") as f:
        f.write("First file")
    with open(test_dir / "02-second.md", "w") as f:
        f.write("Second file")
    
    files = rule_manager.get_ordered_source_files(test_dir)
    assert len(files) == 2
    assert "first" in str(files[0])
    assert "second" in str(files[1])


def test_copy_file(rule_manager, temp_dir):
    """Test the copy_file method."""
    project_root = Path(temp_dir)
    source_file = project_root / "source.txt"
    dest_file = project_root / "subdir" / "dest.txt"
    
    with open(source_file, "w") as f:
        f.write("Test content")
    
    result = rule_manager.copy_file(source_file, dest_file)
    assert result is True
    assert dest_file.exists()
    assert dest_file.read_text() == "Test content"


def test_copy_and_number_files_with_extensions(rule_manager, temp_dir):
    """Test copy_and_number_files with different extension modes."""
    project_root = Path(temp_dir)
    source_dir = project_root / "source"
    dest_dir = project_root / "dest"
    source_dir.mkdir()
    dest_dir.mkdir()
    
    # Create test files
    (source_dir / "test1.md").write_text("Test 1")
    (source_dir / "test2.md").write_text("Test 2")
    
    # Test add_mdc mode (for Cursor)
    count = rule_manager.copy_and_number_files(source_dir, dest_dir, extension_mode='add_mdc')
    assert count == 2
    assert (dest_dir / "01-test1.mdc").exists()
    assert (dest_dir / "02-test2.mdc").exists()


def test_install_assistant_rules_creates_directories(rule_manager, temp_dir):
    """Test that _install_assistant_rules creates the correct directories."""
    project_root = Path(temp_dir)
    source_dir = project_root / "source"
    source_dir.mkdir()
    
    # Create test rule files
    (source_dir / "test-rule.md").write_text("Test rule content")
    
    # Test cursor installation
    rule_manager._install_assistant_rules(source_dir, project_root, ['cursor'])
    assert (project_root / ".cursor" / "rules").exists()
    assert (project_root / ".cursor" / "rules" / "01-test-rule.mdc").exists()
    
    # Test windsurf installation
    rule_manager._install_assistant_rules(source_dir, project_root, ['windsurf'])
    assert (project_root / ".windsurf" / "rules").exists()
    assert (project_root / ".windsurf" / "rules" / "01-test-rule.md").exists()
    
    # Test cline installation
    rule_manager._install_assistant_rules(source_dir, project_root, ['cline'])
    assert (project_root / ".clinerules").exists()
    assert (project_root / ".clinerules" / "01-test-rule").exists()


def test_assistant_specific_file_extensions(rule_manager, temp_dir):
    """Test that different assistants get correct file extensions."""
    project_root = Path(temp_dir)
    source_dir = project_root / "source"
    source_dir.mkdir()
    
    (source_dir / "rule.md").write_text("Test content")
    
    # Test each assistant type
    rule_manager._install_cursor_rules(source_dir, project_root)
    assert (project_root / ".cursor" / "rules" / "01-rule.mdc").exists()
    
    rule_manager._install_windsurf_rules(source_dir, project_root)
    assert (project_root / ".windsurf" / "rules" / "01-rule.md").exists()
    
    rule_manager._install_cline_rules(source_dir, project_root)
    assert (project_root / ".clinerules" / "01-rule").exists()  # no extension
    
    rule_manager._install_roo_rules(source_dir, project_root)
    assert (project_root / ".roo" / "rules").exists()
