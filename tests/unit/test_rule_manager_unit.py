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

def test_copy_tree_non_destructive_with_map(rule_manager, tmp_path):
    """
    Verify that the non-destructive copy only adds new files, does not
    overwrite existing ones, and returns a correct map of copied files.
    """
    source_dir = tmp_path / "source"
    dest_dir = tmp_path / "dest"
    source_dir.mkdir()
    dest_dir.mkdir()

    # Source files
    (source_dir / "new_file.txt").write_text("New")
    (source_dir / "existing_file.txt").write_text("Source Version")

    # Destination files
    (dest_dir / "existing_file.txt").write_text("Original Version")
    (dest_dir / "other_file.txt").write_text("Other")

    # Execute the copy
    copied_files = rule_manager._copy_tree_non_destructive_with_map(source_dir, dest_dir, tmp_path)

    # Verify the returned map
    assert len(copied_files) == 1
    assert copied_files[0] == "dest/new_file.txt"

    # Verify destination contents
    assert (dest_dir / "new_file.txt").is_file()
    assert (dest_dir / "new_file.txt").read_text() == "New"
    
    assert (dest_dir / "existing_file.txt").read_text() == "Original Version"
    assert (dest_dir / "other_file.txt").read_text() == "Other"

def test_generate_for_assistant_mode_based(rule_manager, tmp_path):
    """
    Verify that the generation logic for mode-based assistants (Roo, Kilo)
    correctly creates mode-specific subdirectories.
    """
    source_dir = tmp_path / "project_rules"
    source_dir.mkdir()
    (source_dir / "01-rules").mkdir()
    (source_dir / "01-rules" / "general.md").write_text("General Rule")
    (source_dir / "02-code-mode").mkdir()
    (source_dir / "02-code-mode" / "code.md").write_text("Code Rule")

    target_root = tmp_path / "target_project"
    target_root.mkdir()

    # Get the kilocode spec from the source of truth
    from rulebook_ai.assistants import ASSISTANT_MAP
    kilocode_spec = ASSISTANT_MAP['kilocode']

    # Execute the generation
    rule_manager._generate_for_assistant(kilocode_spec, source_dir, target_root)

    # Verify the output directories and files
    kilocode_root = target_root / ".kilocode"
    assert (kilocode_root / "rules" / "general.md").is_file()
    assert (kilocode_root / "rules" / "general.md").read_text() == "General Rule"
    assert (kilocode_root / "code-mode" / "code.md").is_file()
    assert (kilocode_root / "code-mode" / "code.md").read_text() == "Code Rule"