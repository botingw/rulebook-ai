#!/usr/bin/env python3

import os
import shutil
import argparse
import re

# --- Constants based on the NEW design document ---
# These define the names of the source directories within your project structure,
# relative to the project root.
SOURCE_RULE_SETS_DIR = "rule_sets"
SOURCE_MEMORY_STARTERS_DIR = "memory_starters"
SOURCE_TOOL_STARTERS_DIR = "tool_starters"

# These define the fixed names for directories created in the TARGET repository
TARGET_PROJECT_RULES_DIR = "project_rules"
TARGET_MEMORY_BANK_DIR = "memory"
TARGET_TOOLS_DIR = "tools"

# Default rule set if --rule-set is not provided for the install command
DEFAULT_RULE_SET = "light-spec"

# Project root of this framework repository (where rule_sets/, etc., are located)
# This assumes manage_rules.py is in a subdirectory like 'src/'
PROJECT_FRAMEWORK_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# --- Helper Functions ---
def copy_file(source, destination):
    """Copies a file from source to destination, creating parent dirs."""
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    print(f"Copying {source} -> {destination}")
    try:
        shutil.copy2(source, destination) # copy2 preserves metadata
    except Exception as e:
        print(f"Error copying {source} to {destination}: {e}")
        # Optional: re-raise or return a status
        return False
    return True

def get_ordered_source_files(source_dir_path): # Renamed arg
    """
    Walks the source directory and returns a sorted list of full file paths,
    respecting numerical prefixes on directories and files.
    """
    all_source_files = []
    # print(f"Scanning source directory for ordered files: {source_dir_path}") # Less verbose for now
    if not os.path.isdir(source_dir_path):
        print(f"Error: Source directory '{source_dir_path}' not found or is not a directory.")
        return []

    for root, dirs, files in os.walk(source_dir_path, topdown=True):
        dirs.sort()
        files.sort()
        for filename in files:
            if filename.startswith('.'): # Ignore hidden files
                continue
            source_path = os.path.join(root, filename)
            if os.path.isfile(source_path):
                 all_source_files.append(source_path)
    all_source_files.sort()
    # print(f"Found {len(all_source_files)} files in specified order.")
    return all_source_files

def copy_tree_non_destructive(src_dir, dest_dir):
    """
    Copies directory tree from src to dest.
    If dest_dir exists, only copies files/subdirs from src that are not in dest.
    Does not overwrite existing files in dest. Creates dest_dir if not exists.
    Returns number of new items copied.
    """
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
                # print(f"Copying new directory tree {s_item} -> {d_item}")
                shutil.copytree(s_item, d_item)
                new_items_copied_count += 1 # Count this as one new item (the dir itself)
            else: # If subdir exists in dest, recurse
                # print(f"Destination subdirectory {d_item} exists, checking for new files within...")
                new_items_copied_count += copy_tree_non_destructive(s_item, d_item)
        else: # It's a file
            if not os.path.exists(d_item):
                if copy_file(s_item, d_item):
                    new_items_copied_count += 1
    return new_items_copied_count


def copy_and_number_files(source_dir, dest_dir, extension_mode='keep'):
    if not os.path.exists(dest_dir):
        # print(f"Creating destination directory: {dest_dir}") # Less verbose
        os.makedirs(dest_dir)
    # else:
        # print(f"Destination directory exists: {dest_dir}") # Less verbose

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

    # print(f"Starting numbering at: {next_num:02d} for flattened files. Mode: '{extension_mode}'")

    for source_path in all_source_files:
        base_filename = os.path.basename(source_path)
        filename_no_prefix = re.sub(r"^\d+-", "", base_filename)
        filename_stem, _ = os.path.splitext(filename_no_prefix)

        if extension_mode == 'remove':
            processed_filename = filename_stem
        elif extension_mode == 'add_mdc':
            processed_filename = filename_stem + ".mdc"
        else: # 'keep'
             processed_filename = filename_no_prefix

        new_filename = "{:02d}-{}".format(next_num, processed_filename)
        dest_path = os.path.join(dest_dir, new_filename)
        copy_file(source_path, dest_path)
        next_num += 1

def copy_and_restructure_roocode(source_dir, dest_dir):
    # print(f"Copying tree structure from {source_dir} to {dest_dir} for RooCode") # Less verbose
    if os.path.exists(dest_dir):
        # print(f"Removing existing destination directory for RooCode: {dest_dir}") # Less verbose
        shutil.rmtree(dest_dir)

    try:
        shutil.copytree(source_dir, dest_dir) # Copy first
        # print("Initial tree copy for RooCode complete.") # Less verbose
    except Exception as e:
        print(f"Error during initial copytree for RooCode from {source_dir} to {dest_dir}: {e}")
        return

    dirs_to_rename = []
    for root, dirs, _ in os.walk(dest_dir, topdown=False): # topdown=False for renaming parent after child
         for dir_name in dirs:
             if re.match(r"^\d+-", dir_name):
                 dirs_to_rename.append(os.path.join(root, dir_name))
    dirs_to_rename.sort(key=len, reverse=True) # Rename deeper paths first
    for old_dir_path in dirs_to_rename:
        if not os.path.isdir(old_dir_path): continue
        dir_name = os.path.basename(old_dir_path)
        parent_dir = os.path.dirname(old_dir_path)
        new_dir_name = re.sub(r"^\d+-", "", dir_name)
        new_dir_path = os.path.join(parent_dir, new_dir_name)
        if os.path.exists(new_dir_path) and old_dir_path != new_dir_path : # Avoid collision if new_dir_name is same
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
            if ext: # If there's an extension, remove it
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
    if not all_source_files:
        print(f"Info: No source files found in '{source_dir}' to concatenate.")
        # Create an empty dest_file_path or handle as an error? Design doc implies it's okay.
        # Let's ensure the file is created, possibly empty, to avoid later FileNotFoundError.
        os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
        with open(dest_file_path, 'w', encoding='utf-8') as dest_f: # Create empty file
            pass 
        return

    # print(f"Concatenating {len(all_source_files)} files into: {dest_file_path}") # Less verbose
    os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)

    try:
        with open(dest_file_path, 'w', encoding='utf-8') as dest_f:
            for i, source_path in enumerate(all_source_files):
                # print(f"Appending content from: {source_path}") # Less verbose
                try:
                    with open(source_path, 'r', encoding='utf-8') as source_f:
                        content = source_f.read()
                        dest_f.write(content)
                        if i < len(all_source_files) - 1:
                             separator = f"\n\n# --- Appended from: {os.path.basename(source_path)} ---\n\n"
                             dest_f.write(separator)
                        elif not content.endswith('\n'): # Ensure last file ends with newline
                             dest_f.write('\n')
                except Exception as e:
                    print(f"Error reading file {source_path} during concatenation: {e}")
                    continue # Skip this file
        # print(f"Successfully created concatenated file: {dest_file_path}") # Less verbose
    except Exception as e:
        print(f"Error writing to destination file {dest_file_path}: {e}")


# --- Command Handlers ---

def handle_install(args):
    target_repo_path = os.path.abspath(args.target_repo_path)
    rule_set_name = args.rule_set # From new --rule-set argument

    # Source paths within the framework repository
    source_rules_set_dir = os.path.join(PROJECT_FRAMEWORK_ROOT, SOURCE_RULE_SETS_DIR, rule_set_name)
    source_memory_starters_dir = os.path.join(PROJECT_FRAMEWORK_ROOT, SOURCE_MEMORY_STARTERS_DIR)
    source_tool_starters_dir = os.path.join(PROJECT_FRAMEWORK_ROOT, SOURCE_TOOL_STARTERS_DIR)

    # Target paths in the user's project
    target_project_rules_dir = os.path.join(target_repo_path, TARGET_PROJECT_RULES_DIR)
    target_memory_bank_dir = os.path.join(target_repo_path, TARGET_MEMORY_BANK_DIR)
    target_tools_dir = os.path.join(target_repo_path, TARGET_TOOLS_DIR)

    print(f"--- Installing framework to {target_repo_path} ---")
    print(f"Using rule set: {rule_set_name}")
    print(f"Target Project Rules Dir: {target_project_rules_dir}")
    print(f"Target Memory Bank Dir: {target_memory_bank_dir}")
    print(f"Target Tools Dir: {target_tools_dir}")

    # 1. Install Project Rules (overwrite if exists)
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

    # 2. Install Memory Bank Starters (non-destructive)
    print(f"\nStep 2: Copying memory bank starters to '{TARGET_MEMORY_BANK_DIR}/'...")
    if not os.path.isdir(source_memory_starters_dir):
         print(f"Warning: Source memory starters directory not found: {source_memory_starters_dir}. Skipping memory bank setup.")
    else:
        copied_count = copy_tree_non_destructive(source_memory_starters_dir, target_memory_bank_dir)
        if copied_count > 0:
            print(f"Successfully copied {copied_count} new items to '{target_memory_bank_dir}'.")
        else:
            print(f"No new memory starter items to copy to '{target_memory_bank_dir}'. Existing files preserved.")

    # 3. Install Tool Starters (non-destructive)
    print(f"\nStep 3: Copying tool starters to '{TARGET_TOOLS_DIR}/'...")
    if not os.path.isdir(source_tool_starters_dir):
        print(f"Warning: Source tool starters directory not found: {source_tool_starters_dir}. Skipping tools setup.")
    else:
        copied_count = copy_tree_non_destructive(source_tool_starters_dir, target_tools_dir)
        if copied_count > 0:
            print(f"Successfully copied {copied_count} new items to '{target_tools_dir}'.")
        else:
            print(f"No new tool starter items to copy to '{target_tools_dir}'. Existing files preserved.")


    # 4. Run initial SYNC
    print(f"\nStep 4: Running initial sync...")
    sync_args = argparse.Namespace(target_repo_path=args.target_repo_path)
    if handle_sync(sync_args) != 0:
        print("Error during initial sync. Please check messages above.")
        return 1

    # 5. Output messages
    print(f"\n--- Installation Complete ---")
    print(f"\nIMPORTANT:")
    print(f"1. Add the following lines to .gitignore in {target_repo_path}:")
    print(f"   .cursor/rules/")
    print(f"   .clinerules/")
    print(f"   .roo/")
    print(f"   .windsurfrules")
    print(f"   # Add other generated rule directories if applicable")
    print(f"\n2. Commit the following directories added/updated in your project:")
    print(f"   {TARGET_MEMORY_BANK_DIR}/")
    print(f"   {TARGET_TOOLS_DIR}/")
    print(f"   (The '{TARGET_PROJECT_RULES_DIR}/' directory is managed by this script: replaced by 'install', removed by 'clean-rules'.)")
    print(f"\n3. REMINDER: Ensure your rule files (in '{TARGET_PROJECT_RULES_DIR}/') reference memory files")
    print(f"   using paths relative to the project root, starting with '{TARGET_MEMORY_BANK_DIR}/',")
    print(f"   e.g., '{TARGET_MEMORY_BANK_DIR}/docs/your_doc.md'")
    print(f"\n4. REMINDER: Ensure your rule files (in '{TARGET_PROJECT_RULES_DIR}/') reference tools")
    print(f"   using paths relative to the project root, starting with '{TARGET_TOOLS_DIR}/',")
    print(f"   e.g., 'python {TARGET_TOOLS_DIR}/your_script.py'")
    return 0


def handle_sync(args):
    target_repo_path = os.path.abspath(args.target_repo_path)
    # Source for sync is ALWAYS TARGET_PROJECT_RULES_DIR in the target repo
    project_rules_dir_in_target = os.path.join(target_repo_path, TARGET_PROJECT_RULES_DIR)

    print(f"\n--- Syncing platform rules in {target_repo_path} ---")
    print(f"Using rule source from target: {project_rules_dir_in_target}")

    if not os.path.isdir(project_rules_dir_in_target):
        print(f"Error: Rule source directory '{project_rules_dir_in_target}' not found in target repository.")
        print("Cannot sync. Run the 'install' command first or ensure the directory exists.")
        return 1

    # Define paths to generated rules in target
    cursor_dir = os.path.join(target_repo_path, ".cursor", "rules")
    cursor_parent_dir = os.path.dirname(cursor_dir)
    cline_dir = os.path.join(target_repo_path, ".clinerules")
    roo_rules_dir = os.path.join(target_repo_path, ".roo")
    windsurf_file_path = os.path.join(target_repo_path, ".windsurfrules")

    os.makedirs(cursor_parent_dir, exist_ok=True) # Ensure .cursor parent exists

    # Remove existing generated rules
    # print("Removing existing generated platform rule files/directories...") # Less verbose
    if os.path.exists(cursor_dir): shutil.rmtree(cursor_dir)
    if os.path.exists(cline_dir):
        if os.path.isfile(cline_dir): os.remove(cline_dir)
        elif os.path.isdir(cline_dir): shutil.rmtree(cline_dir)
    if os.path.exists(roo_rules_dir): shutil.rmtree(roo_rules_dir)
    if os.path.isfile(windsurf_file_path): os.remove(windsurf_file_path)

    # Generate new rules
    print("Generating new platform rule files...")
    print("  Processing Cursor rules...")
    copy_and_number_files(project_rules_dir_in_target, cursor_dir, extension_mode='add_mdc')
    print("  Processing CLINE rules...")
    copy_and_number_files(project_rules_dir_in_target, cline_dir, extension_mode='remove')
    print("  Processing RooCode rules...")
    copy_and_restructure_roocode(project_rules_dir_in_target, roo_rules_dir)
    print("  Processing Windsurf rules...")
    concatenate_ordered_files(project_rules_dir_in_target, windsurf_file_path)

    print("\n--- Rule sync complete! ---")
    return 0

def handle_clean_rules(args):
    target_repo_path = os.path.abspath(args.target_repo_path)
    print(f"--- Cleaning rule-specific components from {target_repo_path} ---")

    project_rules_target_dir = os.path.join(target_repo_path, TARGET_PROJECT_RULES_DIR)
    cursor_parent_dir = os.path.join(target_repo_path, ".cursor")
    cline_dir = os.path.join(target_repo_path, ".clinerules")
    roo_rules_dir = os.path.join(target_repo_path, ".roo")
    windsurf_file_path = os.path.join(target_repo_path, ".windsurfrules")

    items_to_remove = [
        project_rules_target_dir,
        cursor_parent_dir,
        cline_dir,
        roo_rules_dir,
        windsurf_file_path,
    ]
    print("Targeting the following for removal (if they exist):")
    for item in items_to_remove: print(f"  - {item}")

    for item_path in items_to_remove:
        try:
            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f"Removed file: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Removed directory: {item_path}")
        except FileNotFoundError:
            print(f"Info: Item not found, skipping: {item_path}")
        except Exception as e:
            print(f"Error removing '{item_path}': {e}")
            # Optionally return 1 here if any error is critical

    print(f"\n--- Rule-specific clean operation complete. ---")
    print(f"Your '{TARGET_MEMORY_BANK_DIR}/' and '{TARGET_TOOLS_DIR}/' directories were NOT touched.")
    return 0

def handle_clean_all(args):
    target_repo_path = os.path.abspath(args.target_repo_path)
    
    print(f"--- Preparing to clean ALL framework components from: {target_repo_path} ---")
    print("\nWARNING: This will remove ALL framework components, including:")
    print(f"  - Generated rule directories (.cursor/, .clinerules/, .roo/, .windsurfrules)")
    print(f"  - The '{TARGET_PROJECT_RULES_DIR}/' directory.")
    print(f"  - The '{TARGET_MEMORY_BANK_DIR}/' directory (potentially containing your customizations).")
    print(f"  - The '{TARGET_TOOLS_DIR}/' directory (potentially containing your customizations).")
    
    try:
        confirm = input("Are you sure you want to proceed? (yes/No): ").strip().lower()
    except EOFError: # Handle non-interactive environments if needed
        print("Non-interactive mode detected, aborting clean-all. Use with caution if automated.")
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
    windsurf_file_path = os.path.join(target_repo_path, ".windsurfrules")

    items_to_remove = [
        project_rules_target_dir, memory_bank_target_dir, tools_target_dir,
        cursor_parent_dir, cline_dir, roo_rules_dir, windsurf_file_path,
    ]
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


def handle_list_rules(args):
    source_rule_sets_main_dir = os.path.join(PROJECT_FRAMEWORK_ROOT, SOURCE_RULE_SETS_DIR)
    print(f"--- Listing available rule sets from: {source_rule_sets_main_dir} ---")

    if not os.path.isdir(source_rule_sets_main_dir):
        print(f"Error: Source rule sets directory '{source_rule_sets_main_dir}' not found.")
        return 1

    available_rule_sets = []
    for item_name in sorted(os.listdir(source_rule_sets_main_dir)):
        item_path = os.path.join(source_rule_sets_main_dir, item_name)
        if os.path.isdir(item_path):
            # Ignore directories starting with '.' or '_' (e.g., .git, __pycache__)
            if not item_name.startswith('.') and not item_name.startswith('_'):
                available_rule_sets.append(item_name)
    
    if not available_rule_sets:
        print("No rule sets found.")
    else:
        print("\nAvailable rule sets:")
        for rule_set_name in available_rule_sets:
            print(f"  - {rule_set_name}")
    
    print("\n--- Listing complete ---")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Manage AI assistant rule sets, project memory banks, and supporting tools."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # Install command
    install_parser = subparsers.add_parser(
        "install",
        help="Install rule sets, memory bank starters, and tool starters to a target repository."
    )
    install_parser.add_argument("target_repo_path", help="Path to the target repository.")
    install_parser.add_argument(
        "--rule-set",
        default=DEFAULT_RULE_SET,
        help=f"Name of the rule set in '{SOURCE_RULE_SETS_DIR}/' (default: {DEFAULT_RULE_SET})."
    )
    install_parser.set_defaults(func=handle_install)

    # Sync command
    sync_parser = subparsers.add_parser(
        "sync",
        help=f"Sync platform rules from '{TARGET_PROJECT_RULES_DIR}/' in the target repository."
    )
    sync_parser.add_argument("target_repo_path", help="Path to the target repository.")
    sync_parser.set_defaults(func=handle_sync)

    # Clean-rules command
    clean_rules_parser = subparsers.add_parser(
        "clean-rules",
        help=f"Clean generated rules and '{TARGET_PROJECT_RULES_DIR}/' from a target repository."
    )
    clean_rules_parser.add_argument("target_repo_path", help="Path to the target repository.")
    clean_rules_parser.set_defaults(func=handle_clean_rules)

    # Clean-all command
    clean_all_parser = subparsers.add_parser(
        "clean-all",
        help="Clean ALL framework components (rules, memory, tools) from a target repository."
    )
    clean_all_parser.add_argument("target_repo_path", help="Path to the target repository.")
    clean_all_parser.set_defaults(func=handle_clean_all)

    # List-rules command
    list_rules_parser = subparsers.add_parser(
        "list-rules",
        help="List all available rule sets that can be installed."
    )
    list_rules_parser.set_defaults(func=handle_list_rules)

    args = parser.parse_args()
    
    exit_code = args.func(args)
    if not isinstance(exit_code, int): # Ensure a numeric exit code
        print(f"Warning: Command handler for '{args.command}' did not return an explicit integer exit code.")
        exit_code = 1 if exit_code is not None else 0 # Default to 0 if None, 1 otherwise
    return exit_code


if __name__ == "__main__":
    script_return_code = main()
    exit(script_return_code)
