#!/usr/bin/env python3

import os
import shutil
import argparse
import re

# --- Constants based on the NEW design document ---
SOURCE_RULE_SETS_DIR = "rule_sets"
SOURCE_MEMORY_STARTERS_DIR = "memory_starters"
SOURCE_TOOL_STARTERS_DIR = "tool_starters"

TARGET_PROJECT_RULES_DIR = "project_rules"
TARGET_MEMORY_BANK_DIR = "memory" # Updated name from design doc
TARGET_TOOLS_DIR = "tools"

DEFAULT_RULE_SET = "light-spec"
PROJECT_FRAMEWORK_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# New constant for GitHub Copilot instructions
TARGET_GITHUB_COPILOT_DIR = ".github"
TARGET_COPILOT_INSTRUCTIONS_FILE = "copilot-instructions.md"

# Constants for env.example and requirements.txt
SOURCE_ENV_EXAMPLE_FILE = "env.example"
SOURCE_REQUIREMENTS_TXT_FILE = "requirements.txt"


# --- Helper Functions ---
# (copy_file, get_ordered_source_files, copy_tree_non_destructive,
#  copy_and_number_files, copy_and_restructure_roocode,
#  concatenate_ordered_files remain the same as your last working version)
# Ensure concatenate_ordered_files creates parent directories if they don't exist.
# Let's assume it does, or update it if needed:

def copy_file(source, destination):
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    # print(f"Copying {source} -> {destination}")
    try:
        shutil.copy2(source, destination) 
    except Exception as e:
        print(f"Error copying {source} to {destination}: {e}")
        return False
    return True

def get_ordered_source_files(source_dir_path):
    all_source_files = []
    if not os.path.isdir(source_dir_path):
        print(f"Error: Source directory '{source_dir_path}' not found or is not a directory.")
        return []
    for root, dirs, files in os.walk(source_dir_path, topdown=True):
        dirs.sort()
        files.sort()
        for filename in files:
            if filename.startswith('.'): continue
            source_path = os.path.join(root, filename)
            if os.path.isfile(source_path):
                 all_source_files.append(source_path)
    all_source_files.sort()
    return all_source_files

def copy_tree_non_destructive(src_dir, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    new_items_copied_count = 0
    if not os.path.isdir(src_dir):
        print(f"Warning: Source directory for non-destructive copy not found: {src_dir}")
        return 0
    for item_name in os.listdir(src_dir):
        s_item = os.path.join(src_dir, item_name)
        d_item = os.path.join(dest_dir, item_name)
        if os.path.isdir(s_item):
            if not os.path.exists(d_item):
                shutil.copytree(s_item, d_item)
                new_items_copied_count += 1 
            else: 
                new_items_copied_count += copy_tree_non_destructive(s_item, d_item)
        else: 
            if not os.path.exists(d_item):
                if copy_file(s_item, d_item):
                    new_items_copied_count += 1
    return new_items_copied_count


def copy_and_number_files(source_dir, dest_dir, extension_mode='keep'):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    all_source_files = get_ordered_source_files(source_dir)
    if not all_source_files:
        print(f"Info: No source files found in '{source_dir}' to process for numbering.")
        return
    existing_files_count = 0
    if os.path.exists(dest_dir):
        for f_name in os.listdir(dest_dir):
            if os.path.isfile(os.path.join(dest_dir, f_name)) and re.match(r"^\d+-", f_name):
                 existing_files_count += 1
    next_num = existing_files_count + 1
    for source_path in all_source_files:
        base_filename = os.path.basename(source_path)
        filename_no_prefix = re.sub(r"^\d+-", "", base_filename)
        filename_stem, _ = os.path.splitext(filename_no_prefix)
        if extension_mode == 'remove':
            processed_filename = filename_stem
        elif extension_mode == 'add_mdc':
            processed_filename = filename_stem + ".mdc"
        elif extension_mode == 'add_md': # Explicitly handle 'add_md'
            processed_filename = filename_stem + ".md"
        else: # Default is 'keep'
            processed_filename = filename_no_prefix
        new_filename = "{:02d}-{}".format(next_num, processed_filename)
        dest_path = os.path.join(dest_dir, new_filename)
        copy_file(source_path, dest_path)
        next_num += 1

def copy_and_restructure_roocode(source_dir, dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    # os.makedirs(dest_dir, exist_ok=True) # copytree will create dest_dir
    try:
        shutil.copytree(source_dir, dest_dir)
    except Exception as e:
        print(f"Error during initial copytree for RooCode from {source_dir} to {dest_dir}: {e}")
        return
    dirs_to_rename = []
    for root, dirs, _ in os.walk(dest_dir, topdown=False):
         for dir_name in dirs:
             if re.match(r"^\d+-", dir_name):
                 dirs_to_rename.append(os.path.join(root, dir_name))
    dirs_to_rename.sort(key=len, reverse=True)
    for old_dir_path in dirs_to_rename:
        if not os.path.isdir(old_dir_path): continue
        dir_name = os.path.basename(old_dir_path)
        parent_dir = os.path.dirname(old_dir_path)
        new_dir_name = re.sub(r"^\d+-", "", dir_name)
        new_dir_path = os.path.join(parent_dir, new_dir_name)
        if os.path.exists(new_dir_path) and old_dir_path != new_dir_path :
             print(f"Warning (RooCode): Target directory '{new_dir_path}' already exists. Skipping rename for '{old_dir_path}'.")
             continue
        try:
            if old_dir_path != new_dir_path: os.rename(old_dir_path, new_dir_path)
        except OSError as e:
            print(f"Error renaming directory for RooCode {old_dir_path} to {new_dir_path}: {e}")
    for root, _, files in os.walk(dest_dir):
        for filename in files:
            if filename.startswith('.'): continue
            base_name, ext = os.path.splitext(filename)
            if ext: 
                old_file_path = os.path.join(root, filename)
                new_file_path = os.path.join(root, base_name)
                if os.path.exists(new_file_path) and old_file_path != new_file_path:
                    print(f"Warning (RooCode): Target file '{new_file_path}' already exists. Skipping rename for '{old_file_path}'.")
                    continue
                try:
                    if old_file_path != new_file_path: os.rename(old_file_path, new_file_path)
                except OSError as e:
                     print(f"Error renaming file for RooCode {old_file_path} to {new_file_path}: {e}")

def concatenate_ordered_files(source_dir, dest_file_path):
    all_source_files = get_ordered_source_files(source_dir)
    # Ensure parent directory for the destination file exists
    os.makedirs(os.path.dirname(dest_file_path), exist_ok=True) # Ensure parent dir for file exists
    
    if not all_source_files:
        print(f"Info: No source files found in '{source_dir}' to concatenate for '{dest_file_path}'. Creating empty file.")
        with open(dest_file_path, 'w', encoding='utf-8') as dest_f:
            pass 
        return

    try:
        with open(dest_file_path, 'w', encoding='utf-8') as dest_f:
            for i, source_path in enumerate(all_source_files):
                try:
                    with open(source_path, 'r', encoding='utf-8') as source_f:
                        content = source_f.read()
                        dest_f.write(content)
                        if i < len(all_source_files) - 1:
                             separator = f"\n\n# --- Appended from: {os.path.basename(source_path)} ---\n\n"
                             dest_f.write(separator)
                        elif not content.endswith('\n'):
                             dest_f.write('\n')
                except Exception as e:
                    print(f"Error reading file {source_path} during concatenation: {e}")
                    continue 
    except Exception as e:
        print(f"Error writing to destination file {dest_file_path}: {e}")

# --- Command Handlers ---
# ... (handle_install remains largely the same, ensure print messages are accurate) ...
def handle_install(args):
    target_repo_path = os.path.abspath(args.target_repo_path)
    rule_set_name = args.rule_set

    source_rules_set_dir = os.path.join(PROJECT_FRAMEWORK_ROOT, SOURCE_RULE_SETS_DIR, rule_set_name)
    source_memory_starters_dir = os.path.join(PROJECT_FRAMEWORK_ROOT, SOURCE_MEMORY_STARTERS_DIR)
    source_tool_starters_dir = os.path.join(PROJECT_FRAMEWORK_ROOT, SOURCE_TOOL_STARTERS_DIR)

    target_project_rules_dir = os.path.join(target_repo_path, TARGET_PROJECT_RULES_DIR)
    target_memory_bank_dir = os.path.join(target_repo_path, TARGET_MEMORY_BANK_DIR)
    target_tools_dir = os.path.join(target_repo_path, TARGET_TOOLS_DIR)

    print(f"--- Installing framework to {target_repo_path} ---")
    print(f"Using rule set: {rule_set_name}")
    # ... (rest of print statements for target dirs)

    # 1. Install Project Rules
    print(f"\nStep 1: Copying rule set '{rule_set_name}' to '{TARGET_PROJECT_RULES_DIR}/'...")
    if not os.path.isdir(source_rules_set_dir):
        print(f"Error: Source rule set directory not found: {source_rules_set_dir}")
        return 1
    if os.path.exists(target_project_rules_dir):
        print(f"Warning: Rule source directory '{target_project_rules_dir}' already exists. It will be replaced.")
        try:
            shutil.rmtree(target_project_rules_dir)
        except Exception as e:
            print(f"Error removing existing directory '{target_project_rules_dir}': {e}")
            return 1
    try:
        shutil.copytree(source_rules_set_dir, target_project_rules_dir)
        print(f"Successfully copied rule templates to '{target_project_rules_dir}'")
    except Exception as e:
        print(f"Error copying rule templates from '{source_rules_set_dir}' to '{target_project_rules_dir}': {e}")
        return 1

    # 2. Install Memory Bank Starters
    print(f"\nStep 2: Copying memory bank starters to '{TARGET_MEMORY_BANK_DIR}/'...")
    if not os.path.isdir(source_memory_starters_dir):
         print(f"Warning: Source memory starters directory not found: {source_memory_starters_dir}. Skipping memory bank setup.")
    else:
        copied_count = copy_tree_non_destructive(source_memory_starters_dir, target_memory_bank_dir)
        if copied_count > 0: print(f"Successfully copied {copied_count} new items to '{target_memory_bank_dir}'.")
        else: print(f"No new memory starter items to copy to '{target_memory_bank_dir}'. Existing files preserved.")

    # 3. Install Tool Starters
    print(f"\nStep 3: Copying tool starters to '{TARGET_TOOLS_DIR}/'...")
    if not os.path.isdir(source_tool_starters_dir):
        print(f"Warning: Source tool starters directory not found: {source_tool_starters_dir}. Skipping tools setup.")
    else:
        copied_count = copy_tree_non_destructive(source_tool_starters_dir, target_tools_dir)
        if copied_count > 0: print(f"Successfully copied {copied_count} new items to '{target_tools_dir}'.")
        else: print(f"No new tool starter items to copy to '{target_tools_dir}'. Existing files preserved.")

    # 4. Copy env.example
    source_env_example_file = os.path.join(PROJECT_FRAMEWORK_ROOT, SOURCE_ENV_EXAMPLE_FILE)
    target_env_example_file = os.path.join(target_repo_path, SOURCE_ENV_EXAMPLE_FILE)
    print(f"\nStep 4: Copying '{SOURCE_ENV_EXAMPLE_FILE}' to target repository root...")
    if os.path.isfile(source_env_example_file):
        if not os.path.exists(target_env_example_file):
            if copy_file(source_env_example_file, target_env_example_file):
                print(f"Successfully copied '{SOURCE_ENV_EXAMPLE_FILE}'.")
        else:
            print(f"'{SOURCE_ENV_EXAMPLE_FILE}' already exists in target. Skipping.")
    else:
        print(f"Warning: Source '{SOURCE_ENV_EXAMPLE_FILE}' not found at '{source_env_example_file}'. Skipping.")

    # 5. Copy requirements.txt
    source_requirements_txt_file = os.path.join(PROJECT_FRAMEWORK_ROOT, SOURCE_REQUIREMENTS_TXT_FILE)
    target_requirements_txt_file = os.path.join(target_repo_path, SOURCE_REQUIREMENTS_TXT_FILE)
    print(f"\nStep 5: Copying '{SOURCE_REQUIREMENTS_TXT_FILE}' to target repository root...")
    if os.path.isfile(source_requirements_txt_file):
        if not os.path.exists(target_requirements_txt_file):
            if copy_file(source_requirements_txt_file, target_requirements_txt_file):
                print(f"Successfully copied '{SOURCE_REQUIREMENTS_TXT_FILE}'.")
        else:
            print(f"'{SOURCE_REQUIREMENTS_TXT_FILE}' already exists in target. Skipping.")
    else:
        print(f"Warning: Source '{SOURCE_REQUIREMENTS_TXT_FILE}' not found at '{source_requirements_txt_file}'. Skipping.")

    # 6. Run initial SYNC
    print(f"\nStep 6: Running initial sync...")
    sync_args = argparse.Namespace(target_repo_path=args.target_repo_path)
    if handle_sync(sync_args) != 0:
        print("Error during initial sync. Please check messages above.")
        return 1

    # 5. Output messages (add .github/copilot-instructions.md to gitignore suggestion)
    print(f"\n--- Installation Complete ---")
    print(f"\nIMPORTANT:")
    print(f"1. Add the following lines to .gitignore in {target_repo_path}:")
    print(f"   .cursor/rules/")
    print(f"   .clinerules/")
    print(f"   .roo/")
    print(f"   .windsurf/")
    print(f"   {TARGET_GITHUB_COPILOT_DIR}/{TARGET_COPILOT_INSTRUCTIONS_FILE}") # New
    print(f"   # Add other generated rule directories if applicable")
    # ... (rest of output messages) ...
    print(f"\n2. Commit the following files/directories added/updated in your project:")
    print(f"   {TARGET_MEMORY_BANK_DIR}/")
    print(f"   {TARGET_TOOLS_DIR}/")
    print(f"   {SOURCE_ENV_EXAMPLE_FILE}")
    print(f"   {SOURCE_REQUIREMENTS_TXT_FILE}")
    print(f"   (The '{TARGET_PROJECT_RULES_DIR}/' directory is managed by this script: replaced by 'install', removed by 'clean-rules'.)")
    # ...
    return 0

def handle_sync(args):
    target_repo_path = os.path.abspath(args.target_repo_path)
    project_rules_dir_in_target = os.path.join(target_repo_path, TARGET_PROJECT_RULES_DIR)

    print(f"\n--- Syncing platform rules in {target_repo_path} ---")
    print(f"Using rule source from target: {project_rules_dir_in_target}")

    if not os.path.isdir(project_rules_dir_in_target):
        print(f"Error: Rule source directory '{project_rules_dir_in_target}' not found.")
        return 1

    # Define paths to generated rules in target
    cursor_dir = os.path.join(target_repo_path, ".cursor", "rules")
    cursor_parent_dir = os.path.dirname(cursor_dir)
    cline_dir = os.path.join(target_repo_path, ".clinerules")
    roo_rules_dir = os.path.join(target_repo_path, ".roo")
    # windsurf_file_path = os.path.join(target_repo_path, ".windsurfrules") # Old Windsurf path
    windsurf_rules_dir = os.path.join(target_repo_path, ".windsurf", "rules") # New Windsurf directory
    windsurf_parent_dir = os.path.join(target_repo_path, ".windsurf") # New Windsurf parent directory
    # New: GitHub Copilot instructions path
    gh_copilot_instructions_path = os.path.join(target_repo_path, TARGET_GITHUB_COPILOT_DIR, TARGET_COPILOT_INSTRUCTIONS_FILE)
    gh_copilot_parent_dir = os.path.dirname(gh_copilot_instructions_path)

    os.makedirs(cursor_parent_dir, exist_ok=True)
    os.makedirs(gh_copilot_parent_dir, exist_ok=True) # Ensure .github directory exists
    # Ensure the new Windsurf parent directory exists before attempting to remove its contents
    os.makedirs(windsurf_parent_dir, exist_ok=True)


    # Remove existing generated rules
    if os.path.exists(cursor_dir): shutil.rmtree(cursor_dir)
    if os.path.exists(cline_dir):
        if os.path.isfile(cline_dir): os.remove(cline_dir)
        elif os.path.isdir(cline_dir): shutil.rmtree(cline_dir)
    if os.path.exists(roo_rules_dir): shutil.rmtree(roo_rules_dir)
    # Remove the old Windsurf file if it exists (will deprecate in the future)
    if os.path.isfile(os.path.join(target_repo_path, ".windsurfrules")): os.remove(os.path.join(target_repo_path, ".windsurfrules"))
    # Remove the new Windsurf rules if it exists
    if os.path.exists(windsurf_rules_dir): shutil.rmtree(windsurf_rules_dir)

    if os.path.isfile(gh_copilot_instructions_path): os.remove(gh_copilot_instructions_path) # New

    # Generate new rules
    print("Generating new platform rule files...")
    print("  Processing Cursor rules...")
    copy_and_number_files(project_rules_dir_in_target, cursor_dir, extension_mode='add_mdc')
    print("  Processing CLINE rules...")
    copy_and_number_files(project_rules_dir_in_target, cline_dir, extension_mode='remove')
    print("  Processing RooCode rules...")
    copy_and_restructure_roocode(project_rules_dir_in_target, roo_rules_dir)
    print("  Processing Windsurf rules...")
    copy_and_number_files(project_rules_dir_in_target, windsurf_rules_dir, extension_mode='add_md')
    print("  Processing GitHub Copilot instructions...") # New
    concatenate_ordered_files(project_rules_dir_in_target, gh_copilot_instructions_path) # New

    print("\n--- Rule sync complete! ---")
    return 0

def handle_clean_rules(args):
    target_repo_path = os.path.abspath(args.target_repo_path)
    print(f"--- Cleaning rule-specific components from {target_repo_path} ---")

    project_rules_target_dir = os.path.join(target_repo_path, TARGET_PROJECT_RULES_DIR)
    cursor_parent_dir = os.path.join(target_repo_path, ".cursor")
    cline_dir = os.path.join(target_repo_path, ".clinerules")
    roo_rules_dir = os.path.join(target_repo_path, ".roo")
    # windsurf_file_path = os.path.join(target_repo_path, ".windsurfrules") # Old Windsurf path
    windsurf_parent_dir_path = os.path.join(target_repo_path, ".windsurf") # New Windsurf directory
    # New: GitHub Copilot instructions path and its parent if it might be removed
    gh_copilot_instructions_path = os.path.join(target_repo_path, TARGET_GITHUB_COPILOT_DIR, TARGET_COPILOT_INSTRUCTIONS_FILE)
    gh_copilot_parent_dir_path = os.path.join(target_repo_path, TARGET_GITHUB_COPILOT_DIR)


    items_to_remove = [
        project_rules_target_dir,
        cursor_parent_dir,
        cline_dir,
        roo_rules_dir,
        # windsurf_file_path, # Remove old Windsurf file
        windsurf_parent_dir_path, # Remove new Windsurf directory
        gh_copilot_instructions_path, # New
    ]
    # Optionally, remove .github if it becomes empty and was created by us
    # For now, just remove the file. A more complex logic can remove empty parent.

    print("Targeting the following for removal (if they exist):")
    for item in items_to_remove: print(f"  - {item}")

    for item_path in items_to_remove:
        try:
            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f"Removed file: {item_path}")
            elif os.path.isdir(item_path): # project_rules, .cursor, .clinerules (if dir), .roo
                shutil.rmtree(item_path)
                print(f"Removed directory: {item_path}")
        except FileNotFoundError:
            print(f"Info: Item not found, skipping: {item_path}")
        except Exception as e:
            print(f"Error removing '{item_path}': {e}")
    
    # Attempt to remove .github directory if it's empty (and exists)
    try:
        if os.path.isdir(gh_copilot_parent_dir_path) and not os.listdir(gh_copilot_parent_dir_path):
            shutil.rmtree(gh_copilot_parent_dir_path)
            print(f"Removed empty directory: {gh_copilot_parent_dir_path}")
    except Exception as e:
        print(f"Info: Could not remove directory '{gh_copilot_parent_dir_path}' or it wasn't empty: {e}")


    print(f"\n--- Rule-specific clean operation complete. ---")
    print(f"Your '{TARGET_MEMORY_BANK_DIR}/' and '{TARGET_TOOLS_DIR}/' directories were NOT touched.")
    return 0

def handle_clean_all(args):
    target_repo_path = os.path.abspath(args.target_repo_path)
    # ... (confirmation prompt as before) ...
    try:
        confirm = input("Are you sure you want to proceed? (yes/No): ").strip().lower()
    except EOFError:
        print("Non-interactive mode detected, aborting clean-all.")
        return 1
    if confirm != 'yes':
        print("Clean operation cancelled by user.")
        return 0

    print("\nProceeding with full clean...")
    project_rules_target_dir = os.path.join(target_repo_path, TARGET_PROJECT_RULES_DIR)
    memory_bank_target_dir = os.path.join(target_repo_path, TARGET_MEMORY_BANK_DIR)
    tools_target_dir = os.path.join(target_repo_path, TARGET_TOOLS_DIR)
    cursor_parent_dir = os.path.join(target_repo_path, ".cursor")
    cline_dir = os.path.join(target_repo_path, ".clinerules")
    roo_rules_dir = os.path.join(target_repo_path, ".roo")
    # windsurf_file_path = os.path.join(target_repo_path, ".windsurfrules") # Old Windsurf path
    windsurf_dir_path = os.path.join(target_repo_path, ".windsurf") # New Windsurf directory
    gh_copilot_parent_dir_path = os.path.join(target_repo_path, TARGET_GITHUB_COPILOT_DIR) # Remove the whole .github dir
    target_env_example_file = os.path.join(target_repo_path, SOURCE_ENV_EXAMPLE_FILE)
    target_requirements_txt_file = os.path.join(target_repo_path, SOURCE_REQUIREMENTS_TXT_FILE)


    items_to_remove = [
        project_rules_target_dir, memory_bank_target_dir, tools_target_dir,
        cursor_parent_dir, cline_dir, roo_rules_dir,
        # windsurf_file_path, # Remove old Windsurf file
        windsurf_dir_path, # Remove new Windsurf directory
        gh_copilot_parent_dir_path,
        target_env_example_file,
        target_requirements_txt_file,
    ]
    # ... (loop and removal logic as before) ...
    print("Removing all framework components...")
    for item_path in items_to_remove:
        try:
            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f"Removed file: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Removed directory: {item_path}")
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error removing '{item_path}': {e}")
    print(f"\n--- Full clean operation complete. ---")
    return 0

# ... (handle_list_rules and main function including list-rules parser remain the same) ...
def handle_list_rules(args):
    source_rule_sets_main_dir = os.path.join(PROJECT_FRAMEWORK_ROOT, SOURCE_RULE_SETS_DIR)
    # ... (rest of list_rules is fine)
    print(f"--- Listing available rule sets from: {source_rule_sets_main_dir} ---")
    if not os.path.isdir(source_rule_sets_main_dir):
        print(f"Error: Source rule sets directory '{source_rule_sets_main_dir}' not found.")
        return 1
    available_rule_sets = []
    for item_name in sorted(os.listdir(source_rule_sets_main_dir)):
        item_path = os.path.join(source_rule_sets_main_dir, item_name)
        if os.path.isdir(item_path) and not item_name.startswith('.') and not item_name.startswith('_'):
            available_rule_sets.append(item_name)
    if not available_rule_sets: print("No rule sets found.")
    else:
        print("\nAvailable rule sets:")
        for rule_set_name in available_rule_sets: print(f"  - {rule_set_name}")
    print("\n--- Listing complete ---")
    return 0

def main():
    parser = argparse.ArgumentParser(
        description="Manage AI assistant rule sets, project memory, and supporting tools." # Updated description
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # Install command
    install_parser = subparsers.add_parser("install", help="Install components to a target repository.")
    install_parser.add_argument("target_repo_path", help="Path to the target repository.")
    install_parser.add_argument("--rule-set", default=DEFAULT_RULE_SET, help=f"Rule set name (default: {DEFAULT_RULE_SET}).")
    install_parser.set_defaults(func=handle_install)

    # Sync command
    sync_parser = subparsers.add_parser("sync", help="Sync platform rules from project_rules/.")
    sync_parser.add_argument("target_repo_path", help="Path to the target repository.")
    sync_parser.set_defaults(func=handle_sync)

    # Clean-rules command
    clean_rules_parser = subparsers.add_parser("clean-rules", help="Clean generated rules and project_rules/.")
    clean_rules_parser.add_argument("target_repo_path", help="Path to the target repository.")
    clean_rules_parser.set_defaults(func=handle_clean_rules)

    # Clean-all command
    clean_all_parser = subparsers.add_parser("clean-all", help="Clean ALL framework components.")
    clean_all_parser.add_argument("target_repo_path", help="Path to the target repository.")
    clean_all_parser.set_defaults(func=handle_clean_all)

    # List-rules command
    list_rules_parser = subparsers.add_parser("list-rules", help="List available rule sets.")
    list_rules_parser.set_defaults(func=handle_list_rules) # No target_repo_path needed

    args = parser.parse_args()

    exit_code = args.func(args)
    if not isinstance(exit_code, int):
        print(f"Warning: Command handler for '{args.command}' did not return an explicit integer exit code.")
        exit_code = 1 if exit_code is not None else 0
    return exit_code


if __name__ == "__main__":
    script_return_code = main()
    exit(script_return_code)
