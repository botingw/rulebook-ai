"""Integration tests to verify package installation and basic functionality.

Note: The actual installation is handled by tox with full visibility via commands_pre.
This test verifies that the installation was successful and basic functionality works.
"""

import shutil
import subprocess

from rulebook_ai.scripts.sync_pack_docs import DESTINATION_RELATIVE, SOURCE_FILES


def test_package_import():
    """Test that the package can be imported successfully."""
    import rulebook_ai

    assert hasattr(rulebook_ai, "__version__")
    print(f"✅ Successfully imported rulebook_ai v{rulebook_ai.__version__}")


def test_core_module_import():
    """Test that core modules can be imported."""
    from rulebook_ai.core import RuleManager

    assert RuleManager is not None
    print("✅ Successfully imported RuleManager")


def test_cli_module_import():
    """Test that CLI module can be imported."""
    from rulebook_ai import cli

    assert hasattr(cli, "main")
    print("✅ Successfully imported CLI module")


def test_community_packs_module_import():
    """Test that community_packs module can be imported."""
    from rulebook_ai import community_packs

    assert hasattr(community_packs, "validate_pack_structure")
    print("✅ Successfully imported community_packs module")


def test_rule_manager_instantiation():
    """Test that RuleManager can be instantiated."""
    from rulebook_ai.core import RuleManager
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a basic RuleManager instance
        manager = RuleManager(temp_dir)
        assert manager is not None
        print("✅ Successfully instantiated RuleManager")


def test_package_structure():
    """Test that the package has expected structure."""
    import rulebook_ai
    import inspect

    # Check that main modules exist
    expected_modules = ["core", "cli", "community_packs"]

    for module_name in expected_modules:
        try:
            module = __import__(f"rulebook_ai.{module_name}", fromlist=[module_name])
            assert module is not None
            print(f"✅ Module rulebook_ai.{module_name} exists and importable")
        except ImportError as e:
            raise AssertionError(f"Failed to import rulebook_ai.{module_name}: {e}")


def test_installed_sync_docs_command(tmp_path):
    """The installed console script can sync an explicitly selected checkout."""
    project_dir = tmp_path / "rulebook-ai"
    for dest_name, source_path in SOURCE_FILES.items():
        path = project_dir / source_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {dest_name}\n", encoding="utf-8")
    destination = project_dir / DESTINATION_RELATIVE
    destination.mkdir(parents=True)

    command = shutil.which("rulebook-ai")
    assert command is not None, "tox must install the project console script"
    result = subprocess.run(
        [command, "sync-docs", "--project-dir", str(project_dir)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    for dest_name in SOURCE_FILES:
        assert (destination / dest_name).read_text(encoding="utf-8") == (f"# {dest_name}\n")
