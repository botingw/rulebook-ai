"""Integration test to verify package installation and basic functionality.

Note: The actual installation is handled by tox with full visibility via commands_pre.
This test verifies that the installation was successful and basic functionality works.
"""

import pytest

def test_package_import():
    """Test that the package can be imported successfully."""
    import rulebook_ai
    assert hasattr(rulebook_ai, '__version__')
    print(f"✅ Successfully imported rulebook_ai v{rulebook_ai.__version__}")


def test_core_module_import():
    """Test that core modules can be imported."""
    from rulebook_ai.core import RuleManager
    assert RuleManager is not None
    print("✅ Successfully imported RuleManager")


def test_cli_module_import():
    """Test that CLI module can be imported."""
    from rulebook_ai import cli
    assert hasattr(cli, 'main')
    print("✅ Successfully imported CLI module")


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
    expected_modules = ['core', 'cli']
    
    for module_name in expected_modules:
        try:
            module = __import__(f'rulebook_ai.{module_name}', fromlist=[module_name])
            assert module is not None
            print(f"✅ Module rulebook_ai.{module_name} exists and importable")
        except ImportError as e:
            raise AssertionError(f"Failed to import rulebook_ai.{module_name}: {e}")
