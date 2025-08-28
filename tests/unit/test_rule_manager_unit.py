"""Unit tests for the rulebook_ai.core.RuleManager class."""

import pytest
from pathlib import Path
from rulebook_ai.core import RuleManager

@pytest.fixture
def rule_manager(tmp_path):
    """Create a RuleManager instance with a temporary project root."""
    # The project_root for RuleManager doesn't strictly matter for these
    # unit tests as we pass absolute paths, but it's good practice.
    return RuleManager(project_root=str(tmp_path))

def test_strategy_flatten_and_number(rule_manager, tmp_path):
    """
    Verify that the flatten strategy correctly takes a nested source,
    finds all files, and creates a flat, numbered list in the destination.
    """
    source_dir = tmp_path / "source"
    dest_dir = tmp_path / "dest"
    source_dir.mkdir()
    (source_dir / "sub").mkdir()

    # Create nested source files
    (source_dir / "a.md").write_text("Content A")
    (source_dir / "sub" / "b.txt").write_text("Content B")
    (source_dir / "c.md").write_text("Content C")

    # Execute the strategy
    count = rule_manager._strategy_flatten_and_number(source_dir, dest_dir, ".out")
    assert count == 3

    # Verify the flattened and numbered output
    files = sorted(list(dest_dir.iterdir()))
    assert len(files) == 3
    
    assert files[0].name == "01-a.out"
    assert files[0].read_text() == "Content A"
    
    assert files[1].name == "02-c.out"
    assert files[1].read_text() == "Content C"

    assert files[2].name == "03-b.out"
    assert files[2].read_text() == "Content B"

def test_strategy_preserve_hierarchy(rule_manager, tmp_path):
    """
    Verify that the preserve hierarchy strategy correctly copies a nested
    directory structure from source to destination.
    """
    source_dir = tmp_path / "source"
    dest_dir = tmp_path / "dest"
    source_dir.mkdir()
    (source_dir / "sub").mkdir()

    # Create nested source files
    (source_dir / "a.md").write_text("Content A")
    (source_dir / "sub" / "b.txt").write_text("Content B")

    # Execute the strategy
    count = rule_manager._strategy_preserve_hierarchy(source_dir, dest_dir)
    assert count == 2

    # Verify the preserved structure
    assert (dest_dir / "a.md").is_file()
    assert (dest_dir / "a.md").read_text() == "Content A"
    assert (dest_dir / "sub" / "b.txt").is_file()
    assert (dest_dir / "sub" / "b.txt").read_text() == "Content B"

def test_strategy_concatenate_files(rule_manager, tmp_path):
    """
    Verify that the concatenate strategy correctly combines multiple source
    files into a single destination file.
    """
    source_dir = tmp_path / "source"
    dest_file = tmp_path / "dest" / "combined.md"
    source_dir.mkdir()
    (source_dir / "sub").mkdir()

    # Create nested source files
    (source_dir / "01-a.md").write_text("Content A")
    (source_dir / "sub" / "02-b.txt").write_text("Content B")

    # Execute the strategy
    rule_manager._strategy_concatenate_files(source_dir, dest_file)

    # Verify the concatenated output
    assert dest_file.is_file()
    content = dest_file.read_text()
    
    assert "# Rule: 01-a.md" in content
    assert "Content A" in content
    assert "---" in content
    assert "# Rule: 02-b.txt" in content
    assert "Content B" in content