import pytest
import os
import shutil
import subprocess
import sys
from pathlib import Path

# --- Absolute path to the root of your ACTUAL project framework ---
FRAMEWORK_ROOT_ACTUAL = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
# Path to the ORIGINAL manage_rules.py script that will be COPIED
MANAGE_RULES_SCRIPT_ORIGINAL_PATH = os.path.join(FRAMEWORK_ROOT_ACTUAL, "src", "manage_rules.py")

# --- Directory names to be used INSIDE the temporary SOURCE framework ---
TMP_SOURCE_RULE_SETS_DIR_NAME = "rule_sets"
TMP_SOURCE_MEMORY_STARTERS_DIR_NAME = "memory_starters"
TMP_SOURCE_TOOL_STARTERS_DIR_NAME = "tool_starters"
TMP_SOURCE_SRC_DIR_NAME = "src" # For the script itself
COPIED_MANAGE_RULES_SCRIPT_NAME = "manage_rules.py"

@pytest.fixture(scope="session")
def tmp_source_repo_root(tmp_path_factory):
    """
    Creates a temporary, isolated 'source framework' directory (tmp_source_repo_root)
    that mimics the actual project structure.
    This directory will contain:
    1. 'rule_sets/', 'memory_starters/', 'tool_starters/' with dummy content.
    2. A 'src/' subdirectory.
    3. A copy of the actual manage_rules.py script placed into 'src/'.
    This entire structure is temporary and created once per test session.
    """
    source_base_dir = tmp_path_factory.mktemp("tmp_source_repo_") # This is our tmp_source_repo_root
    
    # 1. Create dummy template directories directly under tmp_source_repo_root
    # Create actual rule set directory structure to match real data
    (source_base_dir / TMP_SOURCE_RULE_SETS_DIR_NAME / "light-spec" / "01-rules").mkdir(parents=True, exist_ok=True)
    (source_base_dir / TMP_SOURCE_RULE_SETS_DIR_NAME / "light-spec" / "02-rules-architect").mkdir(parents=True, exist_ok=True)
    (source_base_dir / TMP_SOURCE_RULE_SETS_DIR_NAME / "heavy-spec" / "01-rules").mkdir(parents=True, exist_ok=True)

    # Create test files matching actual rule set structure
    (source_base_dir / TMP_SOURCE_RULE_SETS_DIR_NAME / "light-spec" / "01-rules" / "00-meta-rules.md").write_text("Test Light-spec: Main Directive")
    (source_base_dir / TMP_SOURCE_RULE_SETS_DIR_NAME / "light-spec" / "01-rules" / "01-memory.md").write_text("Test Light-spec: Memory")
    (source_base_dir / TMP_SOURCE_RULE_SETS_DIR_NAME / "light-spec" / "02-rules-architect" / "01-plan_v1.md").write_text("Test Light-spec: Python Style")
    (source_base_dir / TMP_SOURCE_RULE_SETS_DIR_NAME / "heavy-spec" / "01-rules" / "00-meta-rules.md").write_text("Test Heavy-spec: Advanced Config")
    (source_base_dir / TMP_SOURCE_RULE_SETS_DIR_NAME / "light-spec" / "03-top-level.md").write_text("Top level light rule")

    (source_base_dir / TMP_SOURCE_MEMORY_STARTERS_DIR_NAME).mkdir(parents=True, exist_ok=True)
    (source_base_dir / TMP_SOURCE_MEMORY_STARTERS_DIR_NAME / "ARCHITECTURE_OVERVIEW.md").write_text("Test Memory: Architecture Overview")
    (source_base_dir / TMP_SOURCE_MEMORY_STARTERS_DIR_NAME / "CODING_GUIDELINES.md").write_text("Test Memory: Coding Guidelines")
    (source_base_dir / TMP_SOURCE_MEMORY_STARTERS_DIR_NAME / "NEW_MEMORY_DOC.md").write_text("A new memory starter doc for testing non-destructive copy.")

    (source_base_dir / TMP_SOURCE_TOOL_STARTERS_DIR_NAME).mkdir(parents=True, exist_ok=True)
    (source_base_dir / TMP_SOURCE_TOOL_STARTERS_DIR_NAME / "linter_tool.py").write_text("print('Executing test linter tool...')")
    (source_base_dir / TMP_SOURCE_TOOL_STARTERS_DIR_NAME / "formatter_tool.sh").write_text("#!/bin/bash\necho 'Executing test formatter tool'")
    (source_base_dir / TMP_SOURCE_TOOL_STARTERS_DIR_NAME / "NEW_TOOL_SCRIPT.py").write_text("print('A new tool script for testing non-destructive copy.')")

    # Create dummy env.example and requirements.txt at the root of tmp_source_repo_root
    (source_base_dir / "env.example").write_text("TEST_ENV_VAR=example_value\n")
    (source_base_dir / "requirements.txt").write_text("test-package==1.0.0\n")

    # 2. Create the src/ subdirectory within tmp_source_repo_root
    tmp_src_dir = source_base_dir / TMP_SOURCE_SRC_DIR_NAME
    tmp_src_dir.mkdir(parents=True, exist_ok=True)

    # 3. Copy the actual manage_rules.py script into tmp_source_repo_root/src/
    assert os.path.exists(MANAGE_RULES_SCRIPT_ORIGINAL_PATH), \
        f"Original manage_rules.py not found at {MANAGE_RULES_SCRIPT_ORIGINAL_PATH}. Ensure path is correct."
    shutil.copy2(MANAGE_RULES_SCRIPT_ORIGINAL_PATH, tmp_src_dir / COPIED_MANAGE_RULES_SCRIPT_NAME)

    print(f"Created temporary source repo root for tests (with src/ subdir) at: {source_base_dir}")
    return source_base_dir


def _run_script_from_tmp_source(
        tmp_source_root_path,
        command_args_list,
        tmp_target_path=None, # Made optional
        confirm_input=None
    ):

    # Use the modern rulebook-ai CLI instead of old manage_rules.py script
    full_command = [
        "rulebook-ai",
        *command_args_list
    ]
    if tmp_target_path: # Only add target_path if it's provided
        full_command.extend(["--project-dir", str(tmp_target_path)])

    # Execute the modern rulebook-ai CLI command
    print(f"Running: {' '.join(full_command)}")
    process = subprocess.run(
        full_command,
        capture_output=True,
        text=True,
        input=(confirm_input + "\n") if confirm_input is not None else None,
        check=False 
    )
    
    print(f"STDOUT:\n{process.stdout}")
    if process.stderr:
        print(f"STDERR:\n{process.stderr}")
    return process

@pytest.fixture
def script_runner(tmp_source_repo_root):
    """Returns a function that runs the script with the given arguments."""
    def _run_script(args, tmp_target_path=None, confirm_input=None):
        return _run_script_from_tmp_source(
            tmp_source_repo_root,
            args,
            tmp_target_path,
            confirm_input
        )
    return _run_script


@pytest.fixture(scope="session")
def tools_symlink():
    """
    Create a symlink from 'tools' to 'tool_starters' in the site-packages directory.
    This allows tests to import from 'tools' while the actual code is in 'tool_starters'.
    
    This is a temporary solution until the project is fully modernized and the imports
    are updated to match the actual directory structure.
    """
    # Get the site-packages directory
    site_packages = None
    for path in sys.path:
        if "site-packages" in path:
            site_packages = Path(path)
            break
    
    if not site_packages:
        pytest.skip("Could not find site-packages directory")
    
    # Check if tools symlink already exists
    tools_link = site_packages / "tools"
    tool_starters_path = Path(FRAMEWORK_ROOT_ACTUAL) / "tool_starters"
    
    if not tools_link.exists():
        # Create symlink
        tools_link.symlink_to(tool_starters_path, target_is_directory=True)
        yield tools_link
        # Clean up
        if tools_link.exists() and tools_link.is_symlink():
            tools_link.unlink()
    else:
        # Symlink already exists, just yield it
        yield tools_link
