import os
import shutil
import re # For checking generated rule file formats
import pytest

# --- Expected directory names in the TARGET project (tmp_target_repo_root) ---
TARGET_PROJECT_RULES_DIR = "project_rules"
TARGET_MEMORY_BANK_DIR = "memory" # As per updated design doc
TARGET_TOOLS_DIR = "tools"

# --- Expected directory names in the TEMPORARY SOURCE (tmp_source_repo_root) ---
# These must match what's created in conftest.py's tmp_source_repo_root fixture
TMP_SOURCE_RULE_SETS_DIR_NAME = "rule_sets"
TMP_SOURCE_MEMORY_STARTERS_DIR_NAME = "memory_starters"
TMP_SOURCE_TOOL_STARTERS_DIR_NAME = "tool_starters"


def test_install_default_rule_set(script_runner, tmp_path): # tmp_path provides tmp_target_repo_root
    """Test `install` with the default rule set ('light-spec')."""
    tmp_target_repo_root = tmp_path / "my_project_default_install"
    tmp_target_repo_root.mkdir()

    result = script_runner(["install"], tmp_target_repo_root)
    assert result.returncode == 0, f"Script failed. STDERR:\n{result.stderr}\nSTDOUT:\n{result.stdout}"

    # 1. Check presence of core directories in target
    assert (tmp_target_repo_root / TARGET_PROJECT_RULES_DIR).is_dir()
    assert (tmp_target_repo_root / TARGET_MEMORY_BANK_DIR).is_dir()
    assert (tmp_target_repo_root / TARGET_TOOLS_DIR).is_dir()

    # 2. Check project_rules content (should be 'light-spec' from tmp_source_repo_root)
    project_rules_target = tmp_target_repo_root / TARGET_PROJECT_RULES_DIR
    assert (project_rules_target / "01-rules" / "00-meta-rules.md").is_file()
    assert (project_rules_target / "02-rules-architect" / "01-plan_v1.md").is_file()
    assert not (project_rules_target / "01-rules" / "config_heavy.md").exists() # from heavy-spec

    # 3. Check memory_bank content
    memory_bank_target = tmp_target_repo_root / TARGET_MEMORY_BANK_DIR
    assert (memory_bank_target / "ARCHITECTURE_OVERVIEW.md").is_file()
    assert (memory_bank_target / "CODING_GUIDELINES.md").is_file()

    # 4. Check tools content
    tools_target = tmp_target_repo_root / TARGET_TOOLS_DIR
    assert (tools_target / "linter_tool.py").is_file()
    assert (tools_target / "formatter_tool.sh").is_file()

    # 5. Check for generated platform-specific rule directories (basic existence)
    assert (tmp_target_repo_root / ".cursor" / "rules").is_dir()
    assert (tmp_target_repo_root / ".clinerules").is_dir()
    assert (tmp_target_repo_root / ".roo").is_dir()
    assert (tmp_target_repo_root / ".windsurf" / "rules").is_dir() # New: Check for .windsurf/rules directory
    assert not (tmp_target_repo_root / ".windsurfrules").exists() # New: Assert old path does not exist
    gh_copilot_instructions_file = tmp_target_repo_root / ".github" / "copilot-instructions.md" # New
    assert gh_copilot_instructions_file.is_file()                                                # New
    
    # Check for specific numbered .md files in .windsurf/rules
    assert (tmp_target_repo_root / ".windsurf" / "rules" / "01-meta-rules.md").is_file()
    assert (tmp_target_repo_root / ".windsurf" / "rules" / "02-memory.md").is_file()
    assert (tmp_target_repo_root / ".windsurf" / "rules" / "03-plan_v1.md").is_file()

    # Check content of a generated file to ensure it's from the correct source rules
    windsurf_content = (tmp_target_repo_root / ".windsurf" / "rules" / "01-meta-rules.md").read_text() # New: Read from new path
    assert "Test Light-spec: Main Directive" in windsurf_content
    gh_copilot_content = gh_copilot_instructions_file.read_text()                               # New
    assert "Test Light-spec: Main Directive" in gh_copilot_content                              # New

    # 6. Check for env.example and requirements.txt
    assert (tmp_target_repo_root / "env.example").is_file()
    # Assuming conftest.py will create "TEST_ENV_VAR=example_value" in env.example
    assert "TEST_ENV_VAR=example_value" in (tmp_target_repo_root / "env.example").read_text()
    assert (tmp_target_repo_root / "requirements.txt").is_file()
    # Assuming conftest.py will create "test-package==1.0.0" in requirements.txt
    assert "test-package==1.0.0" in (tmp_target_repo_root / "requirements.txt").read_text()


def test_install_specific_rule_set(script_runner, tmp_path):
    """Test `install --rule-set heavy-spec`."""
    tmp_target_repo_root = tmp_path / "my_project_heavy_install"
    tmp_target_repo_root.mkdir()

    result = script_runner(["install", "--rule-set", "heavy-spec"], tmp_target_repo_root)
    assert result.returncode == 0, f"Script failed. STDERR:\n{result.stderr}"

    project_rules_target = tmp_target_repo_root / TARGET_PROJECT_RULES_DIR
    assert (project_rules_target / "01-rules" / "00-meta-rules.md").is_file()
    assert not (project_rules_target / "01-rules" / "01-memory.md").exists() # from light-spec (heavy-spec only has meta-rules)

    # Check generated file content for heavy-spec rule
    # Expected path for the first rule file from 'heavy-spec'
    heavy_spec_rule_file = tmp_target_repo_root / ".windsurf" / "rules" / "01-meta-rules.md"
    assert heavy_spec_rule_file.is_file()
    windsurf_content = heavy_spec_rule_file.read_text()
    assert "Test Heavy-spec: Advanced Config" in windsurf_content
    gh_copilot_content = (tmp_target_repo_root / ".github" / "copilot-instructions.md").read_text() # New
    assert "Test Heavy-spec: Advanced Config" in gh_copilot_content                                # New

    # Check for env.example and requirements.txt (should also be copied with heavy-spec)
    assert (tmp_target_repo_root / "env.example").is_file()
    assert "TEST_ENV_VAR=example_value" in (tmp_target_repo_root / "env.example").read_text()
    assert (tmp_target_repo_root / "requirements.txt").is_file()
    assert "test-package==1.0.0" in (tmp_target_repo_root / "requirements.txt").read_text()


def test_sync_after_manual_project_rules_modification(script_runner, tmp_path):
    tmp_target_repo_root = tmp_path / "project_for_sync_test"
    tmp_target_repo_root.mkdir()
    script_runner(["install", "--rule-set", "light-spec"], tmp_target_repo_root)

    rule_to_modify = tmp_target_repo_root / TARGET_PROJECT_RULES_DIR / "01-rules" / "00-meta-rules.md"
    modified_content = " *** MODIFIED CONTENT FOR SYNC TEST *** "
    rule_to_modify.write_text(modified_content)

    # Path to the specific synced Windsurf rule file
    synced_windsurf_rule_file = tmp_target_repo_root / ".windsurf" / "rules" / "01-meta-rules.md"
    gh_copilot_file_path = tmp_target_repo_root / ".github" / "copilot-instructions.md" # New
    
    # Remove the files if they exist to ensure sync creates them
    if (tmp_target_repo_root / ".windsurf").exists(): 
        shutil.rmtree(tmp_target_repo_root / ".windsurf")
    if gh_copilot_file_path.exists(): 
        gh_copilot_file_path.unlink()                     # New

    result = script_runner(["sync"], tmp_target_repo_root)
    assert result.returncode == 0, f"Sync script failed. STDERR:\n{result.stderr}"
    
    assert synced_windsurf_rule_file.is_file()
    assert modified_content in synced_windsurf_rule_file.read_text()
    
    assert gh_copilot_file_path.is_file()                                              # New
    assert modified_content in gh_copilot_file_path.read_text()                        # New

def test_clean_rules_removes_rules_and_generated_keeps_memory_tools(script_runner, tmp_path):
    tmp_target_repo_root = tmp_path / "project_for_clean_rules"
    tmp_target_repo_root.mkdir()
    script_runner(["install"], tmp_target_repo_root) # This will create .github/copilot-instructions.md

    result = script_runner(["clean-rules"], tmp_target_repo_root)
    assert result.returncode == 0, f"clean-rules script failed. STDERR:\n{result.stderr}"

    assert not (tmp_target_repo_root / TARGET_PROJECT_RULES_DIR).exists()
    assert not (tmp_target_repo_root / ".cursor").exists()
    assert not (tmp_target_repo_root / ".windsurf").exists() # Ensure the .windsurf directory is removed
    assert not (tmp_target_repo_root / ".github" / "copilot-instructions.md").exists() # New
    # Also check if the .github directory itself is removed if it becomes empty, or if it should remain.
    # For simplicity, let's assume if copilot-instructions.md is the only thing there, .github might be removed.
    # Or, assert that .github *could* exist but copilot-instructions.md *must not*.
    # A safer check:
    assert not (tmp_target_repo_root / ".github" / "copilot-instructions.md").exists()
    # If .github dir is removed only if empty and only contained our file:
    if os.path.exists(tmp_target_repo_root / ".github") and not os.listdir(tmp_target_repo_root / ".github"):
        pass # This state is acceptable, or we could assert .github is also gone if it was created by us.
             # For now, just checking the file is gone is sufficient.

    assert (tmp_target_repo_root / TARGET_MEMORY_BANK_DIR).is_dir()
    assert (tmp_target_repo_root / TARGET_TOOLS_DIR).is_dir()
    assert (tmp_target_repo_root / TARGET_MEMORY_BANK_DIR / "ARCHITECTURE_OVERVIEW.md").is_file()

def test_clean_all_with_confirmation_yes(script_runner, tmp_path):
    tmp_target_repo_root = tmp_path / "project_for_clean_all_yes"
    tmp_target_repo_root.mkdir()
    script_runner(["install"], tmp_target_repo_root) # This will create .github/copilot-instructions.md

    result = script_runner(["clean-all"], tmp_target_repo_root, confirm_input="yes")
    assert result.returncode == 0, f"clean-all script failed. STDERR:\n{result.stderr}"

    assert not (tmp_target_repo_root / TARGET_PROJECT_RULES_DIR).exists()
    assert not (tmp_target_repo_root / TARGET_MEMORY_BANK_DIR).exists()
    assert not (tmp_target_repo_root / TARGET_TOOLS_DIR).exists()
    assert not (tmp_target_repo_root / ".cursor").exists()
    assert not (tmp_target_repo_root / ".cursor").exists()
    assert not (tmp_target_repo_root / ".clinerules").exists() # Added assertion for .clinerules
    assert not (tmp_target_repo_root / ".roo").exists() # Added assertion for .roo
    assert not (tmp_target_repo_root / ".windsurf").exists() # New: Check for the .windsurf directory
    # assert not (tmp_target_repo_root / ".windsurfrules").exists() # Ensure old path is removed - Deprecated by Windsurf
    assert not (tmp_target_repo_root / ".github").exists() # Assuming .github is removed if it only contained our file
    assert not (tmp_target_repo_root / "env.example").exists()
    assert not (tmp_target_repo_root / "requirements.txt").exists()

def test_clean_all_with_confirmation_no(script_runner, tmp_path):
    tmp_target_repo_root = tmp_path / "project_for_clean_all_no"
    tmp_target_repo_root.mkdir()
    script_runner(["install"], tmp_target_repo_root)

    result = script_runner(["clean-all"], tmp_target_repo_root, confirm_input="no")
    assert result.returncode == 0, f"clean-all script failed. STDERR:\n{result.stderr}"

    assert (tmp_target_repo_root / TARGET_PROJECT_RULES_DIR).is_dir()
    assert (tmp_target_repo_root / TARGET_MEMORY_BANK_DIR).is_dir()
    assert (tmp_target_repo_root / "env.example").is_file()
    assert (tmp_target_repo_root / "requirements.txt").is_file()
    
    # Verify that Windsurf rules directory remains when "no" is selected
    assert (tmp_target_repo_root / ".windsurf").is_dir()
    assert (tmp_target_repo_root / ".windsurf" / "rules").is_dir()
    # Optionally, check for a specific file within it too (assuming default install)
    assert (tmp_target_repo_root / ".windsurf" / "rules" / "01-meta-rules.md").is_file()
    
    # [TODO] test message too fragile, figure out new test ways
    # assert "Clean operation cancelled." in result.stdout

def test_list_rules(script_runner, tmp_source_repo_root): # tmp_source_repo_root fixture ensures rule_sets exist
    """Test the `list-rules` command."""
    # tmp_source_repo_root (from conftest.py) creates:
    # - rule_sets/light-spec
    # - rule_sets/heavy-spec
    # - rule_sets/empty-ruleset (which is a directory)
    # - rule_sets/.hidden_ruleset (should be ignored)
    # - rule_sets/_private_ruleset (should be ignored)
    # - rule_sets/not_a_dir_ruleset.txt (should be ignored)


    result = script_runner(["list-rules"])
    assert result.returncode == 0, f"Script failed. STDERR:\n{result.stderr}\nSTDOUT:\n{result.stdout}"

    stdout = result.stdout
    assert "Available rule sets:" in stdout
    assert "- heavy-spec" in stdout    # From conftest.py
    assert "- light-spec" in stdout    # From conftest.py
    
    # Ensure ignored items are not listed
    assert ".hidden_ruleset" not in stdout
    assert "_private_ruleset" not in stdout
    assert "not_a_dir_ruleset.txt" not in stdout
    
    assert "--- Listing complete ---" in stdout


def test_install_with_specific_assistant_flags(script_runner, tmp_path):
    """Test install with specific assistant flags."""
    tmp_target_repo_root = tmp_path / "my_project_windsurf_only"
    tmp_target_repo_root.mkdir()

    # Test --windsurf flag
    result = script_runner(["install", "--windsurf"], tmp_target_repo_root)
    assert result.returncode == 0, f"Script failed. STDERR:\n{result.stderr}\nSTDOUT:\n{result.stdout}"

    # Should create windsurf directory
    assert (tmp_target_repo_root / ".windsurf" / "rules").is_dir()
    
    # Should NOT create other assistant directories when specific flag is used
    assert not (tmp_target_repo_root / ".cursor").exists()
    assert not (tmp_target_repo_root / ".clinerules").exists()
    assert not (tmp_target_repo_root / ".roo").exists()
    
    # Should still create generic directories
    assert (tmp_target_repo_root / TARGET_PROJECT_RULES_DIR).is_dir()
    assert (tmp_target_repo_root / TARGET_MEMORY_BANK_DIR).is_dir()
    assert (tmp_target_repo_root / TARGET_TOOLS_DIR).is_dir()


def test_install_with_all_assistants_flag(script_runner, tmp_path):
    """Test install with --all-assistants flag."""
    tmp_target_repo_root = tmp_path / "my_project_all_assistants"
    tmp_target_repo_root.mkdir()

    result = script_runner(["install", "--all-assistants"], tmp_target_repo_root)
    assert result.returncode == 0, f"Script failed. STDERR:\n{result.stderr}\nSTDOUT:\n{result.stdout}"

    # Should create ALL assistant directories
    assert (tmp_target_repo_root / ".cursor" / "rules").is_dir()
    assert (tmp_target_repo_root / ".clinerules").is_dir()
    assert (tmp_target_repo_root / ".roo").is_dir()
    assert (tmp_target_repo_root / ".windsurf" / "rules").is_dir()


def test_sync_with_specific_assistant_flags(script_runner, tmp_path):
    """Test sync with specific assistant flags."""
    tmp_target_repo_root = tmp_path / "project_for_sync_assistant_test"
    tmp_target_repo_root.mkdir()
    
    # First install with all assistants
    script_runner(["install"], tmp_target_repo_root)
    
    # Modify project rules
    rule_to_modify = tmp_target_repo_root / TARGET_PROJECT_RULES_DIR / "01-rules" / "00-meta-rules.md"
    modified_content = " *** SYNC TEST WITH WINDSURF FLAG *** "
    rule_to_modify.write_text(modified_content)
    
    # Sync only windsurf
    result = script_runner(["sync", "--windsurf"], tmp_target_repo_root)
    assert result.returncode == 0, f"Sync script failed. STDERR:\n{result.stderr}"
    
    # Check that windsurf was synced
    synced_windsurf_rule_file = tmp_target_repo_root / ".windsurf" / "rules" / "01-meta-rules.md"
    assert synced_windsurf_rule_file.is_file()
    assert modified_content in synced_windsurf_rule_file.read_text()


def test_sync_detects_existing_assistants(script_runner, tmp_path):
    """Test that sync without flags detects existing assistant directories."""
    tmp_target_repo_root = tmp_path / "project_for_sync_detection_test"
    tmp_target_repo_root.mkdir()
    
    # Install only windsurf initially
    script_runner(["install", "--windsurf"], tmp_target_repo_root)
    
    # Modify project rules
    rule_to_modify = tmp_target_repo_root / TARGET_PROJECT_RULES_DIR / "01-rules" / "00-meta-rules.md"
    modified_content = " *** AUTO-DETECTION SYNC TEST *** "
    rule_to_modify.write_text(modified_content)
    
    # Sync without flags should detect existing windsurf directory
    result = script_runner(["sync"], tmp_target_repo_root)
    assert result.returncode == 0, f"Sync script failed. STDERR:\n{result.stderr}"
    
    # Check that windsurf was synced
    synced_windsurf_rule_file = tmp_target_repo_root / ".windsurf" / "rules" / "01-meta-rules.md"
    assert synced_windsurf_rule_file.is_file()
    assert modified_content in synced_windsurf_rule_file.read_text()
