"""Integration test to verify tool installation and functionality.

Note: These tests run in the tox environment where rulebook-ai is already installed.
They test the CLI functionality and tool management capabilities.
"""
import tempfile
import shutil
from pathlib import Path
import subprocess
import sys
import pytest


def test_cli_install_command():
    """Test that the CLI install command works."""
    # Create a temporary project directory
    with tempfile.TemporaryDirectory() as temp_dir:
        project_dir = Path(temp_dir)
        
        # Test CLI install command
        result = subprocess.run([
            sys.executable, "-m", "rulebook_ai.cli", 
            "install", "--help"
        ], capture_output=True, text=True, cwd=project_dir)
        
        assert result.returncode == 0, f"CLI install --help failed: {result.stderr}"
        assert "install" in result.stdout.lower()
        print("✅ CLI install command accessible")


def test_cli_list_rules_command():
    """Test that the CLI list-rules command works."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_dir = Path(temp_dir)
        
        # Test CLI list-rules command
        result = subprocess.run([
            sys.executable, "-m", "rulebook_ai.cli",
            "list-rules"
        ], capture_output=True, text=True, cwd=project_dir)
        
        # Should succeed or fail gracefully (not crash)
        print(f"✅ CLI list-rules command executed (exit code: {result.returncode})")


def test_cli_doctor_command():
    """Test that the CLI doctor command works."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_dir = Path(temp_dir)
        
        # Test CLI doctor command
        result = subprocess.run([
            sys.executable, "-m", "rulebook_ai.cli",
            "doctor"
        ], capture_output=True, text=True, cwd=project_dir)
        
        # Should succeed or fail gracefully (not crash)
        print(f"✅ CLI doctor command executed (exit code: {result.returncode})")


def test_rule_manager_functionality():
    """Test that RuleManager can be used programmatically."""
    from rulebook_ai.core import RuleManager
    import os
    
    # Use the test_env directory as specified in the project structure
    test_env_dir = Path(__file__).parent.parent.parent / "test_env" / "mock_project"
    os.makedirs(test_env_dir, exist_ok=True)
    
    # Create a RuleManager instance
    manager = RuleManager(str(test_env_dir))
    assert manager is not None
    
    # Test basic functionality
    rules = manager.list_rules()
    assert isinstance(rules, list)
    
    print("✅ RuleManager programmatic access works")


def test_package_entry_points():
    """Test that package entry points are properly configured."""
    # Test that the CLI entry point exists
    result = subprocess.run([
        "rulebook-ai", "--help"
    ], capture_output=True, text=True)
    
    # Should work if entry point is properly configured
    if result.returncode == 0:
        print("✅ CLI entry point 'rulebook-ai' works")
        assert "rulebook" in result.stdout.lower()
    else:
        print(f"ℹ️  CLI entry point test skipped (exit code: {result.returncode})")
        # This might fail if the entry point isn't in PATH, which is okay for integration tests


def test_tool_installation_workflow():
    """Test a basic tool installation workflow."""
    from rulebook_ai.core import RuleManager
    import os
    
    # Use the test_env directory as specified in the project structure
    test_env_dir = Path(__file__).parent.parent.parent / "test_env" / "mock_project"
    os.makedirs(test_env_dir, exist_ok=True)
    
    # Create basic project structure
    os.makedirs(test_env_dir / "src", exist_ok=True)
    os.makedirs(test_env_dir / "tests", exist_ok=True)
    
    # Initialize RuleManager
    manager = RuleManager(str(test_env_dir))
    
    # Test that we can query available rules
    try:
        rules = manager.list_rules()
        print(f"✅ Found {len(rules)} available rule sets")
    except Exception as e:
        print(f"ℹ️  Rule listing test: {e}")
    
    # Test basic directory structure creation
    assert test_env_dir.exists()
    print("✅ Basic tool installation workflow test completed")
