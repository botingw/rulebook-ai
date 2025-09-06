import os
import shutil
import json
import re # For checking generated rule file formats
import pytest

# --- Expected directory names in the TARGET project (tmp_target_repo_root) ---
TARGET_PROJECT_RULES_DIR = "project_rules"
TARGET_MEMORY_BANK_DIR = "memory"
TARGET_TOOLS_DIR = "tools"

def test_install_default_rule_set(script_runner, tmp_path):
    """Test `install` with the default rule set ('light-spec')."""
    tmp_target_repo_root = tmp_path / "my_project_default_install"
    tmp_target_repo_root.mkdir()

    result = script_runner(["install"], tmp_target_repo_root)
    assert result.returncode == 0, f"Script failed. STDERR:\n{result.stderr}\nSTDOUT:\n{result.stdout}"

    # 1. Check presence of core directories in target
    assert (tmp_target_repo_root / TARGET_PROJECT_RULES_DIR).is_dir()
    assert (tmp_target_repo_root / TARGET_MEMORY_BANK_DIR).is_dir()
    assert (tmp_target_repo_root / TARGET_TOOLS_DIR).is_dir()

    # 2. Check project_rules content (should be 'light-spec' from the actual package)
    project_rules_target = tmp_target_repo_root / TARGET_PROJECT_RULES_DIR
    assert (project_rules_target / "01-rules" / "00-meta-rules.md").is_file()
    assert (project_rules_target / "02-rules-architect" / "01-plan_v1.md").is_file()

    # 3. Check memory_bank content (from actual package)
    memory_bank_target = tmp_target_repo_root / TARGET_MEMORY_BANK_DIR
    assert (memory_bank_target / "docs" / "architecture_template.md").is_file()
    assert (memory_bank_target / "tasks" / "active_context_template.md").is_file()

    # 4. Check tools content (from actual package)
    tools_target = tmp_target_repo_root / TARGET_TOOLS_DIR
    assert (tools_target / "llm_api.py").is_file()
    assert (tools_target / "web_scraper.py").is_file()

    # 5. Check for generated platform-specific rule directories
    assert (tmp_target_repo_root / ".cursor" / "rules").is_dir()
    assert (tmp_target_repo_root / ".clinerules").is_dir()
    # Check mode-based assistants for multiple modes and a file within a mode
    assert (tmp_target_repo_root / ".roo" / "rules").is_dir()
    assert (tmp_target_repo_root / ".roo" / "rules-architect").is_dir()
    assert (tmp_target_repo_root / ".roo" / "rules" / "00-meta-rules.md").is_file()
    assert (tmp_target_repo_root / ".kilocode" / "rules").is_dir()
    assert (tmp_target_repo_root / ".kilocode" / "rules-architect").is_dir()
    assert (tmp_target_repo_root / ".kilocode" / "rules" / "00-meta-rules.md").is_file()
    assert (tmp_target_repo_root / ".windsurf" / "rules").is_dir()
    assert (tmp_target_repo_root / "WARP.md").is_file()
    gh_copilot_instructions_file = tmp_target_repo_root / ".github" / "copilot-instructions.md"
    assert gh_copilot_instructions_file.is_file()
    assert (tmp_target_repo_root / "CLAUDE.md").is_file()
    assert (tmp_target_repo_root / "AGENTS.md").is_file()
    assert (tmp_target_repo_root / ".gemini" / "GEMINI.md").is_file()

    # Check content of a generated file to ensure it's from the correct source rules
    expected_content = "Meta-Rules for AI Assistant Interaction"
    gh_copilot_content = gh_copilot_instructions_file.read_text()
    assert expected_content in gh_copilot_content
    claude_content = (tmp_target_repo_root / "CLAUDE.md").read_text()
    assert expected_content in claude_content
    warp_content = (tmp_target_repo_root / "WARP.md").read_text()
    assert expected_content in warp_content

    # 6. Check for .rulebook-ai directory and its contents
    rulebook_ai_dir = tmp_target_repo_root / ".rulebook-ai"
    assert rulebook_ai_dir.is_dir()

    # 7. Check for selection.json
    selection_file = rulebook_ai_dir / "selection.json"
    assert selection_file.is_file()
    with open(selection_file, 'r') as f:
        selection = json.load(f)
    assert selection["packs"][0]["name"] == "light-spec"

    # 8. Check for copied pack source
    copied_pack_dir = rulebook_ai_dir / "packs" / "light-spec"
    assert copied_pack_dir.is_dir()
    assert (copied_pack_dir / "manifest.yaml").is_file()

    # 9. Check for file-map.json
    file_map_file = copied_pack_dir / "file-map.json"
    assert file_map_file.is_file()
    with open(file_map_file, 'r') as f:
        file_map = json.load(f)
    assert len(file_map["files"]) > 0
    assert "memory/docs/architecture_template.md" in file_map["files"]





def test_install_specific_rule_set(script_runner, tmp_path):
    """Test `install --rule-set heavy-spec`."""
    tmp_target_repo_root = tmp_path / "my_project_heavy_install"
    tmp_target_repo_root.mkdir()

    result = script_runner(["install", "--rule-set", "heavy-spec"], tmp_target_repo_root)
    assert result.returncode == 0, f"Script failed. STDERR:\n{result.stderr}"

    project_rules_target = tmp_target_repo_root / TARGET_PROJECT_RULES_DIR
    assert (project_rules_target / "01-rules" / "00-meta-rules.md").is_file()
    assert (project_rules_target / "01-rules" / "01-memory.md").is_file()

    gh_copilot_content = (tmp_target_repo_root / ".github" / "copilot-instructions.md").read_text()
    assert "Meta-Rules for AI Assistant Interaction" in gh_copilot_content
    assert (tmp_target_repo_root / "CLAUDE.md").is_file()
    assert (tmp_target_repo_root / "AGENTS.md").is_file()
    assert (tmp_target_repo_root / ".gemini" / "GEMINI.md").is_file()
    assert (tmp_target_repo_root / "WARP.md").is_file()
    assert (tmp_target_repo_root / ".kilocode" / "rules").is_dir()

    # Check for .rulebook-ai directory and its contents
    rulebook_ai_dir = tmp_target_repo_root / ".rulebook-ai"
    assert rulebook_ai_dir.is_dir()
    selection_file = rulebook_ai_dir / "selection.json"
    assert selection_file.is_file()
    with open(selection_file, 'r') as f:
        selection = json.load(f)
    assert selection["packs"][0]["name"] == "heavy-spec"
    copied_pack_dir = rulebook_ai_dir / "packs" / "heavy-spec"
    assert copied_pack_dir.is_dir()
    assert (copied_pack_dir / "manifest.yaml").is_file()
    file_map_file = copied_pack_dir / "file-map.json"
    assert file_map_file.is_file()


def test_sync_after_manual_project_rules_modification(script_runner, tmp_path):
    tmp_target_repo_root = tmp_path / "project_for_sync_test"
    tmp_target_repo_root.mkdir()
    install_result = script_runner(["install", "--rule-set", "light-spec"], tmp_target_repo_root)
    assert install_result.returncode == 0, f"Setup install failed: {install_result.stderr}"

    # Modify a rule in the first mode ('rules')
    rule_to_modify_1 = tmp_target_repo_root / TARGET_PROJECT_RULES_DIR / "01-rules" / "00-meta-rules.md"
    assert rule_to_modify_1.is_file()
    modified_content_1 = " *** MODIFIED CONTENT 1 FOR SYNC TEST *** "
    rule_to_modify_1.write_text(modified_content_1)

    # Modify a rule in the second mode ('rules-architect')
    rule_to_modify_2 = tmp_target_repo_root / TARGET_PROJECT_RULES_DIR / "02-rules-architect" / "01-plan_v1.md"
    assert rule_to_modify_2.is_file()
    modified_content_2 = " *** MODIFIED CONTENT 2 FOR SYNC TEST *** "
    rule_to_modify_2.write_text(modified_content_2)

    result = script_runner(["sync"], tmp_target_repo_root)
    assert result.returncode == 0, f"Sync script failed. STDERR:\n{result.stderr}"
    
    # --- Assertions for concatenated files ---
    gh_copilot_file_path = tmp_target_repo_root / ".github" / "copilot-instructions.md"
    claude_path = tmp_target_repo_root / "CLAUDE.md"
    codex_path = tmp_target_repo_root / "AGENTS.md"
    gemini_path = tmp_target_repo_root / ".gemini" / "GEMINI.md"
    warp_path = tmp_target_repo_root / "WARP.md"
    
    for path in [gh_copilot_file_path, claude_path, codex_path, gemini_path, warp_path]:
        assert path.is_file()
        content = path.read_text()
        assert modified_content_1 in content
        assert modified_content_2 in content

    # --- Assertions for first modified rule in mode-based assistants ---
    roo_path_1 = tmp_target_repo_root / ".roo" / "rules" / "00-meta-rules.md"
    kilocode_path_1 = tmp_target_repo_root / ".kilocode" / "rules" / "00-meta-rules.md"
    assert roo_path_1.is_file()
    assert kilocode_path_1.is_file()
    assert modified_content_1 in roo_path_1.read_text()
    assert modified_content_1 in kilocode_path_1.read_text()

    # --- Assertions for second modified rule in mode-based assistants ---
    roo_path_2 = tmp_target_repo_root / ".roo" / "rules-architect" / "01-plan_v1.md"
    kilocode_path_2 = tmp_target_repo_root / ".kilocode" / "rules-architect" / "01-plan_v1.md"
    assert roo_path_2.is_file()
    assert kilocode_path_2.is_file()
    assert modified_content_2 in roo_path_2.read_text()
    assert modified_content_2 in kilocode_path_2.read_text()


def test_clean_rules_removes_rules_and_generated_keeps_memory_tools(script_runner, tmp_path):
    tmp_target_repo_root = tmp_path / "project_for_clean_rules"
    tmp_target_repo_root.mkdir()
    install_result = script_runner(["install"], tmp_target_repo_root)
    assert install_result.returncode == 0, f"Setup install failed: {install_result.stderr}"

    result = script_runner(["clean-rules"], tmp_target_repo_root)
    assert result.returncode == 0, f"clean-rules script failed. STDERR:\n{result.stderr}"

    assert not (tmp_target_repo_root / TARGET_PROJECT_RULES_DIR).exists()
    assert not (tmp_target_repo_root / ".cursor").exists()
    assert not (tmp_target_repo_root / ".windsurf").exists()
    assert not (tmp_target_repo_root / ".clinerules").exists()
    assert not (tmp_target_repo_root / ".roo").exists()
    assert not (tmp_target_repo_root / ".kilocode").exists()
    assert not (tmp_target_repo_root / "WARP.md").exists()
    assert not (tmp_target_repo_root / ".github").exists()
    assert not (tmp_target_repo_root / "CLAUDE.md").exists()
    assert not (tmp_target_repo_root / "AGENTS.md").exists()
    assert not (tmp_target_repo_root / ".gemini").exists()

    assert (tmp_target_repo_root / TARGET_MEMORY_BANK_DIR).is_dir()
    assert (tmp_target_repo_root / TARGET_TOOLS_DIR).is_dir()
    assert (tmp_target_repo_root / TARGET_MEMORY_BANK_DIR / "docs" / "architecture_template.md").is_file()


def test_clean_all_with_confirmation_yes(script_runner, tmp_path):
    tmp_target_repo_root = tmp_path / "project_for_clean_all_yes"
    tmp_target_repo_root.mkdir()
    install_result = script_runner(["install"], tmp_target_repo_root)
    assert install_result.returncode == 0, f"Setup install failed: {install_result.stderr}"

    result = script_runner(["clean-all"], tmp_target_repo_root, confirm_input="yes")
    assert result.returncode == 0, f"clean-all script failed. STDERR:\n{result.stderr}"

    assert not (tmp_target_repo_root / TARGET_PROJECT_RULES_DIR).exists()
    assert not (tmp_target_repo_root / TARGET_MEMORY_BANK_DIR).exists()
    assert not (tmp_target_repo_root / TARGET_TOOLS_DIR).exists()
    assert not (tmp_target_repo_root / ".cursor").exists()
    assert not (tmp_target_repo_root / ".clinerules").exists()
    assert not (tmp_target_repo_root / ".roo").exists()
    assert not (tmp_target_repo_root / ".kilocode").exists()
    assert not (tmp_target_repo_root / "WARP.md").exists()
    assert not (tmp_target_repo_root / ".windsurf").exists()
    assert not (tmp_target_repo_root / ".github").exists()
    assert not (tmp_target_repo_root / "CLAUDE.md").exists()
    assert not (tmp_target_repo_root / "AGENTS.md").exists()
    assert not (tmp_target_repo_root / ".gemini").exists()


def test_clean_all_with_confirmation_no(script_runner, tmp_path):
    tmp_target_repo_root = tmp_path / "project_for_clean_all_no"
    tmp_target_repo_root.mkdir()
    install_result = script_runner(["install"], tmp_target_repo_root)
    assert install_result.returncode == 0, f"Setup install failed: {install_result.stderr}"

    result = script_runner(["clean-all"], tmp_target_repo_root, confirm_input="no")
    assert result.returncode == 0, f"clean-all script failed. STDERR:\n{result.stderr}"

    assert (tmp_target_repo_root / TARGET_PROJECT_RULES_DIR).is_dir()
    assert (tmp_target_repo_root / TARGET_MEMORY_BANK_DIR).is_dir()
    assert (tmp_target_repo_root / ".windsurf" / "rules").is_dir()
    assert (tmp_target_repo_root / "CLAUDE.md").is_file()
    assert (tmp_target_repo_root / "AGENTS.md").is_file()
    assert (tmp_target_repo_root / ".gemini" / "GEMINI.md").is_file()
    assert (tmp_target_repo_root / "WARP.md").is_file()
    assert "Clean-all operation cancelled by user." in result.stdout


def test_list_packs(script_runner):
    """Test the `list-packs` command."""
    result = script_runner(["list-packs"])
    assert result.returncode == 0, f"Script failed. STDERR:\n{result.stderr}\nSTDOUT:\n{result.stdout}"

    stdout = result.stdout
    assert "Available packs:" in stdout
    assert "- heavy-spec" in stdout
    assert "- light-spec" in stdout
    assert "https://github.com/botingw/rulebook-ai/wiki/Ratings-%26-Reviews-(Rulesets)" in stdout
    

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
    assert not (tmp_target_repo_root / ".kilocode").exists()
    assert not (tmp_target_repo_root / "WARP.md").exists()
    assert not (tmp_target_repo_root / ".github").exists()
    assert not (tmp_target_repo_root / "CLAUDE.md").exists()
    assert not (tmp_target_repo_root / "AGENTS.md").exists()
    assert not (tmp_target_repo_root / ".gemini").exists()
    # Should still create generic directories
    assert (tmp_target_repo_root / TARGET_PROJECT_RULES_DIR).is_dir()
    assert (tmp_target_repo_root / TARGET_MEMORY_BANK_DIR).is_dir()
    assert (tmp_target_repo_root / TARGET_TOOLS_DIR).is_dir()


def test_install_with_all_assistants_flag(script_runner, tmp_path):
    """Test install with --all-assistants flag."""
    tmp_target_repo_root = tmp_path / "my_project_all_assistants"
    tmp_target_repo_root.mkdir()

    result = script_runner(["install", "--all"], tmp_target_repo_root)
    assert result.returncode == 0, f"Script failed. STDERR:\n{result.stderr}\nSTDOUT:\n{result.stdout}"

    # Should create ALL assistant directories
    assert (tmp_target_repo_root / ".cursor" / "rules").is_dir()
    assert (tmp_target_repo_root / ".clinerules").is_dir()
    assert (tmp_target_repo_root / ".roo" / "rules").is_dir()
    assert (tmp_target_repo_root / ".kilocode" / "rules").is_dir()
    assert (tmp_target_repo_root / ".windsurf" / "rules").is_dir()
    assert (tmp_target_repo_root / "WARP.md").is_file()
    assert (tmp_target_repo_root / ".github" / "copilot-instructions.md").is_file()
    assert (tmp_target_repo_root / "CLAUDE.md").is_file()
    assert (tmp_target_repo_root / "AGENTS.md").is_file()
    assert (tmp_target_repo_root / ".gemini" / "GEMINI.md").is_file()


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
    
    # Sync without flags should now sync ALL assistants, not just existing ones
    result = script_runner(["sync"], tmp_target_repo_root)
    assert result.returncode == 0, f"Sync script failed. STDERR:\n{result.stderr}"
    
    # Check that windsurf was synced
    synced_windsurf_rule_file = tmp_target_repo_root / ".windsurf" / "rules" / "01-meta-rules.md"
    assert synced_windsurf_rule_file.is_file()
    assert modified_content in synced_windsurf_rule_file.read_text()

    # Check that another assistant (e.g., cursor) was ALSO synced
    synced_cursor_rule_file = tmp_target_repo_root / ".cursor" / "rules" / "01-meta-rules.mdc"
    assert synced_cursor_rule_file.is_file()
    assert modified_content in synced_cursor_rule_file.read_text()
    claude_file = tmp_target_repo_root / "CLAUDE.md"
    assert claude_file.is_file()
    assert modified_content in claude_file.read_text()


def test_bug_report_command(script_runner):
    """Verify the bug-report command opens the issue tracker URL."""
    result = script_runner(["bug-report"])
    assert result.returncode == 0, f"Command failed. STDERR:\n{result.stderr}"
    assert "https://github.com/botingw/rulebook-ai/issues" in result.stdout


def test_rate_ruleset_command(script_runner):
    """Verify the rate-ruleset command opens the ratings page URL."""
    result = script_runner(["rate-ruleset"])
    assert result.returncode == 0, f"Command failed. STDERR:\n{result.stderr}"
    assert (
        "https://github.com/botingw/rulebook-ai/wiki/Ratings-%26-Reviews-(Rulesets)"
        in result.stdout
    )
