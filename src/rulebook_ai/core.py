"""
Core functionality for rulebook-ai rule management.

This module provides the core functionality for managing AI rulebooks,
separated from the CLI interface for better modularity and testing.
"""

import os
import shutil
import re
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any

# --- Constants ---
SOURCE_RULE_SETS_DIR = "rule_sets"
SOURCE_MEMORY_STARTERS_DIR = "memory_starters"
SOURCE_TOOL_STARTERS_DIR = "tool_starters"

TARGET_PROJECT_RULES_DIR = "project_rules"
TARGET_MEMORY_BANK_DIR = "memory"
TARGET_TOOLS_DIR = "tools"

DEFAULT_RULE_SET = "light-spec"
TARGET_GITHUB_COPILOT_DIR = ".github"
TARGET_COPILOT_INSTRUCTIONS_FILE = "copilot-instructions.md"

# Assistant-specific directories
TARGET_CURSOR_DIR = ".cursor/rules"
TARGET_WINDSURF_DIR = ".windsurf/rules"
TARGET_CLINE_DIR = ".clinerules"
TARGET_ROO_DIR = ".roo/rules"

SOURCE_ENV_EXAMPLE_FILE = ".env.example"
SOURCE_REQUIREMENTS_TXT_FILE = "requirements.txt"


class RuleManager:
    """Manages the installation and synchronization of AI rules and related files."""

    def __init__(self, project_root: Optional[str] = None) -> None:
        """
        Initialize the RuleManager with project paths.
        
        Args:
            project_root: Root directory of the target project. If None, uses the current directory.
        """
        # Determine package path (where our package is installed)
        self.package_path = Path(__file__).parent.absolute()
        
        # Determine source paths (within our package)
        self.source_rules_dir = self.package_path / SOURCE_RULE_SETS_DIR
        self.source_memory_dir = self.package_path / SOURCE_MEMORY_STARTERS_DIR
        self.source_tools_dir = self.package_path / SOURCE_TOOL_STARTERS_DIR
        
        # If source dirs don't exist in package, try to find them in development mode
        # This is for development convenience
        if not self.source_rules_dir.exists():
            dev_root = self.package_path.parent.parent
            self.source_rules_dir = dev_root / SOURCE_RULE_SETS_DIR
            self.source_memory_dir = dev_root / SOURCE_MEMORY_STARTERS_DIR
            self.source_tools_dir = dev_root / SOURCE_TOOL_STARTERS_DIR
        
        # Determine target project root
        if project_root is None:
            # Default to current directory
            self.project_root = Path.cwd().absolute()
        else:
            self.project_root = Path(project_root).absolute()
        
        # Target directories (within user's project)
        self.target_rules_dir = self.project_root / TARGET_PROJECT_RULES_DIR
        self.target_memory_dir = self.project_root / TARGET_MEMORY_BANK_DIR
        self.target_tools_dir = self.project_root / TARGET_TOOLS_DIR
        self.target_github_dir = self.project_root / TARGET_GITHUB_COPILOT_DIR

    def copy_file(self, source: Path, destination: Path) -> bool:
        """
        Copy a file from source to destination, creating parent directories if needed.
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Returns:
            bool: True if copy was successful, False otherwise
        """
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            return True
        except Exception as e:
            print(f"Error copying {source} to {destination}: {e}")
            return False

    def get_ordered_source_files(self, source_dir_path: Path) -> List[Path]:
        """
        Get a sorted list of all files in a directory (recursively).
        
        Args:
            source_dir_path: Directory to scan for files
            
        Returns:
            List of Path objects for files found, sorted alphabetically
        """
        if not source_dir_path.is_dir():
            print(f"Error: Source directory '{source_dir_path}' not found or is not a directory.")
            return []
            
        all_source_files = []
        for root, dirs, files in os.walk(source_dir_path):
            dirs.sort()
            files.sort()
            root_path = Path(root)
            for filename in sorted(files):
                if filename.startswith('.'):
                    continue
                    
                file_path = root_path / filename
                if file_path.is_file():
                    all_source_files.append(file_path)
                    
        return sorted(all_source_files)

    def copy_tree_non_destructive(self, src_dir: Path, dest_dir: Path) -> int:
        """
        Copy a directory tree without overwriting existing files.
        
        Args:
            src_dir: Source directory
            dest_dir: Destination directory
            
        Returns:
            int: Number of new items copied
        """
        dest_dir.mkdir(parents=True, exist_ok=True)
        new_items_copied_count = 0
        
        if not src_dir.is_dir():
            print(f"Warning: Source directory for non-destructive copy not found: {src_dir}")
            return 0
            
        for item in src_dir.iterdir():
            dest_item = dest_dir / item.name
            
            if item.is_dir():
                if not dest_item.exists():
                    shutil.copytree(item, dest_item)
                    new_items_copied_count += 1
                else:
                    new_items_copied_count += self.copy_tree_non_destructive(item, dest_item)
            else:
                if not dest_item.exists():
                    if self.copy_file(item, dest_item):
                        new_items_copied_count += 1
                        
        return new_items_copied_count

    def copy_and_number_files(self, source_dir: Path, dest_dir: Path, 
                             extension_mode: str = 'keep') -> int:
        """
        Copy files from source to destination with numeric prefixes.
        
        Args:
            source_dir: Source directory
            dest_dir: Destination directory
            extension_mode: How to handle file extensions ('keep', 'add_mdc', 'add_md', 'remove')
            
        Returns:
            int: Number of files copied
        """
        dest_dir.mkdir(parents=True, exist_ok=True)
        all_source_files = self.get_ordered_source_files(source_dir)
        
        if not all_source_files:
            print(f"Info: No source files found in '{source_dir}' to process for numbering.")
            return 0
            
        # Count existing numbered files
        existing_files_count = 0
        if dest_dir.exists():
            existing_files_count = sum(
                1 for f in dest_dir.iterdir() 
                if f.is_file() and re.match(r"^\d+-", f.name)
            )
            
        next_num = existing_files_count + 1
        files_copied = 0
        
        for source_path in all_source_files:
            base_filename = source_path.name
            filename_no_prefix = re.sub(r"^\d+-", "", base_filename)
            
            if extension_mode == 'keep':
                new_filename = f"{next_num:02d}-{filename_no_prefix}"
            elif extension_mode == 'add_mdc':
                filename_stem = source_path.stem
                filename_stem = re.sub(r"^\d+-", "", filename_stem)
                new_filename = f"{next_num:02d}-{filename_stem}.mdc"
            elif extension_mode == 'add_md':
                filename_stem = source_path.stem
                filename_stem = re.sub(r"^\d+-", "", filename_stem)
                new_filename = f"{next_num:02d}-{filename_stem}.md"
            elif extension_mode == 'remove':
                filename_stem = source_path.stem
                filename_stem = re.sub(r"^\d+-", "", filename_stem)
                new_filename = f"{next_num:02d}-{filename_stem}"
            else:
                # Default: add .md extension
                filename_stem = source_path.stem
                filename_stem = re.sub(r"^\d+-", "", filename_stem)
                new_filename = f"{next_num:02d}-{filename_stem}.md"
                
            dest_file_path = dest_dir / new_filename
            if self.copy_file(source_path, dest_file_path):
                next_num += 1
                files_copied += 1
                
        return files_copied
                
    def copy_and_restructure_roocode(self, source_dir: Path, dest_dir: Path) -> int:
        """
        Copy and restructure files for roocode format.
        
        Args:
            source_dir: Source directory 
            dest_dir: Destination directory
            
        Returns:
            int: Number of files copied
        """
        dest_dir.mkdir(parents=True, exist_ok=True)
        all_source_files = self.get_ordered_source_files(source_dir)
        
        if not all_source_files:
            print(f"Info: No source files found in '{source_dir}' for restructuring.")
            return 0
            
        files_copied = 0
        # Process each file
        for source_path in all_source_files:
            rel_path = source_path.relative_to(source_dir)
            dest_path = dest_dir / rel_path
            
            # Create intermediate directories
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy the file
            if self.copy_file(source_path, dest_path):
                files_copied += 1
                
        return files_copied

    def concatenate_ordered_files(self, source_dir: Path, dest_file_path: Path) -> None:
        """
        Concatenate all files in a directory into a single output file.
        
        Args:
            source_dir: Directory containing files to concatenate
            dest_file_path: Path for the output concatenated file
        """
        all_source_files = self.get_ordered_source_files(source_dir)
        
        if not all_source_files:
            print(f"Info: No source files found in '{source_dir}' to concatenate.")
            return
            
        # Create parent directories if they don't exist
        dest_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(dest_file_path, 'w', encoding='utf-8') as output_file:
            for source_path in all_source_files:
                try:
                    with open(source_path, 'r', encoding='utf-8') as input_file:
                        file_content = input_file.read()
                    
                    output_file.write(f"# {source_path.name}\n\n")
                    output_file.write(file_content)
                    output_file.write("\n\n")
                except Exception as e:
                    print(f"Error processing {source_path}: {e}")

    def install(self, rule_set: str = DEFAULT_RULE_SET, 
               project_dir: Optional[str] = None,
               clean_first: bool = False,
               include_copilot: bool = True,
               assistants: Optional[List[str]] = None) -> int:
        """
        Install a ruleset into a target project directory.
        
        Args:
            rule_set: Name of the rule set to install
            project_dir: Target project directory. If None, uses current project root.
            clean_first: Whether to clean existing rules before installation
            include_copilot: Whether to include GitHub Copilot instructions
            assistants: List of AI assistants to install for. If None/empty, installs generic rules only.
            
        Returns:
            int: Return code (0 for success, non-zero for error)
        """
        if project_dir is not None:
            target_root = Path(project_dir).absolute()
        else:
            target_root = self.project_root
            
        # Set target directories based on provided project directory
        target_rules_dir = target_root / TARGET_PROJECT_RULES_DIR
        target_memory_dir = target_root / TARGET_MEMORY_BANK_DIR
        target_tools_dir = target_root / TARGET_TOOLS_DIR
        target_github_dir = target_root / TARGET_GITHUB_COPILOT_DIR
        
        # Source directory for the specific rule set
        rule_set_source_dir = self.source_rules_dir / rule_set
        
        # Clean first if requested
        if clean_first:
            if target_rules_dir.exists():
                shutil.rmtree(target_rules_dir)
            if include_copilot and (target_github_dir / TARGET_COPILOT_INSTRUCTIONS_FILE).exists():
                (target_github_dir / TARGET_COPILOT_INSTRUCTIONS_FILE).unlink()
                
        # Verify the rule set exists
        if not rule_set_source_dir.is_dir():
            print(f"Error: Rule set '{rule_set}' not found in {self.source_rules_dir}")
            print("Available rule sets:")
            for rule_dir in sorted(p.name for p in self.source_rules_dir.iterdir() if p.is_dir()):
                print(f"  - {rule_dir}")
            return 1
            
        # Create target directories
        target_rules_dir.mkdir(parents=True, exist_ok=True)
        target_memory_dir.mkdir(parents=True, exist_ok=True)
        target_tools_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy rule files preserving directory structure
        print(f"Installing rule set '{rule_set}'...")
        rules_count = self.copy_tree_non_destructive(rule_set_source_dir, target_rules_dir)
        print(f"Copied {rules_count} new rule files.")
        
        # Copy memory starters non-destructively
        memory_count = self.copy_tree_non_destructive(
            self.source_memory_dir, 
            target_memory_dir
        )
        print(f"Copied {memory_count} new memory starter files.")
        
        # Copy tool starters non-destructively
        tools_count = self.copy_tree_non_destructive(
            self.source_tools_dir, 
            target_tools_dir
        )
        print(f"Copied {tools_count} new tool starter files.")
        
        # Copy .env.example if it exists
        env_example_path = self.project_root / SOURCE_ENV_EXAMPLE_FILE
        if env_example_path.exists():
            target_env_example = target_root / ".env.example"
            self.copy_file(env_example_path, target_env_example)
            print(f"Copied .env.example to {target_env_example}")
            
        # Copy GitHub Copilot instructions if requested
        if include_copilot:
            github_dir_path = target_github_dir
            github_dir_path.mkdir(parents=True, exist_ok=True)
            
            copilot_dest_path = github_dir_path / TARGET_COPILOT_INSTRUCTIONS_FILE
            if not copilot_dest_path.exists():
                # Create instructions by concatenating all rules
                self.concatenate_ordered_files(
                    target_rules_dir, 
                    copilot_dest_path
                )
                print(f"Created GitHub Copilot instructions at {copilot_dest_path}")
            else:
                print(f"GitHub Copilot instructions already exist at {copilot_dest_path}")
        
        # Install assistant-specific rules if requested
        if assistants:
            self._install_assistant_rules(rule_set_source_dir, target_root, assistants)
                
        print(f"Rule set '{rule_set}' installed successfully in {target_root}")
        return 0

    def _install_assistant_rules(self, source_dir: Path, target_root: Path, assistants: List[str]) -> None:
        """
        Install rules for specific AI assistants.
        
        Args:
            source_dir: Source directory containing the rules
            target_root: Target project root directory
            assistants: List of assistant names to install for
        """
        for assistant in assistants:
            if assistant == 'cursor':
                self._install_cursor_rules(source_dir, target_root)
            elif assistant == 'windsurf':
                self._install_windsurf_rules(source_dir, target_root)
            elif assistant == 'cline':
                self._install_cline_rules(source_dir, target_root)
            elif assistant == 'roo':
                self._install_roo_rules(source_dir, target_root)
            else:
                print(f"Warning: Unknown assistant '{assistant}' - skipping")

    def _install_cursor_rules(self, source_dir: Path, target_root: Path) -> None:
        """Install rules for Cursor AI assistant (.cursor/rules/*.mdc)."""
        target_dir = target_root / TARGET_CURSOR_DIR
        target_dir.mkdir(parents=True, exist_ok=True)
        
        count = self.copy_and_number_files(source_dir, target_dir, extension_mode='add_mdc')
        print(f"Created {count} Cursor rule files in {target_dir}")

    def _install_windsurf_rules(self, source_dir: Path, target_root: Path) -> None:
        """Install rules for Windsurf AI assistant (.windsurf/rules/*.md)."""
        target_dir = target_root / TARGET_WINDSURF_DIR
        target_dir.mkdir(parents=True, exist_ok=True)
        
        count = self.copy_and_number_files(source_dir, target_dir, extension_mode='add_md')
        print(f"Created {count} Windsurf rule files in {target_dir}")

    def _install_cline_rules(self, source_dir: Path, target_root: Path) -> None:
        """Install rules for Cline AI assistant (.clinerules/)."""
        target_dir = target_root / TARGET_CLINE_DIR
        target_dir.mkdir(parents=True, exist_ok=True)
        
        count = self.copy_and_number_files(source_dir, target_dir, extension_mode='remove')
        print(f"Created {count} Cline rule files in {target_dir}")

    def _install_roo_rules(self, source_dir: Path, target_root: Path) -> None:
        """Install rules for RooCode AI assistant (.roo/rules/)."""
        target_dir = target_root / TARGET_ROO_DIR
        target_dir.mkdir(parents=True, exist_ok=True)
        
        count = self.copy_and_restructure_roocode(source_dir, target_dir)
        print(f"Created {count} RooCode rule files in {target_dir}")

    def sync(self, rule_set: str = DEFAULT_RULE_SET,
            project_dir: Optional[str] = None,
            include_copilot: bool = True,
            assistants: Optional[List[str]] = None) -> int:
        """
        Synchronize assistant-specific rules from existing project_rules directory.
        
        This is the correct sync behavior: uses project_rules/ as source and 
        regenerates assistant-specific directories (.cursor/, .windsurf/, etc.)
        
        Args:
            rule_set: Name of the rule set (ignored - uses existing project_rules/)
            project_dir: Target project directory. If None, uses current project root.
            include_copilot: Whether to include GitHub Copilot instructions
            assistants: List of assistants to sync. If None, syncs all existing assistants.
            
        Returns:
            int: Return code (0 for success, non-zero for error)
        """
        if project_dir is not None:
            target_root = Path(project_dir).absolute()
        else:
            target_root = self.project_root
            
        # The source is the existing project_rules directory
        source_rules_dir = target_root / TARGET_PROJECT_RULES_DIR
        
        # Verify project_rules directory exists
        if not source_rules_dir.exists():
            print(f"Error: Project rules directory '{source_rules_dir}' does not exist.")
            print("Run 'install' command first to create the initial rule structure.")
            return 1
            
        print("Syncing assistant-specific rules from project_rules/...")
        
        # Determine which assistants to sync
        if assistants is None:
            # Auto-detect existing assistant directories
            assistants = []
            if (target_root / TARGET_CURSOR_DIR).exists():
                assistants.append('cursor')
            if (target_root / TARGET_WINDSURF_DIR).exists():
                assistants.append('windsurf') 
            if (target_root / TARGET_CLINE_DIR).exists():
                assistants.append('cline')
            if (target_root / TARGET_ROO_DIR).exists():
                assistants.append('roo')
                
            if not assistants:
                print("No existing assistant directories found.")
                print("Use --cursor, --windsurf, --cline, --roo, or --all-assistants to specify which to sync.")
                return 2
                
        # Remove and regenerate assistant-specific directories
        if assistants:
            self._sync_assistant_rules(source_rules_dir, target_root, assistants)
        
        # Update GitHub Copilot instructions if requested
        if include_copilot:
            target_github_dir = target_root / TARGET_GITHUB_COPILOT_DIR
            copilot_dest_path = target_github_dir / TARGET_COPILOT_INSTRUCTIONS_FILE
            if copilot_dest_path.exists():
                copilot_dest_path.unlink()
                
            target_github_dir.mkdir(parents=True, exist_ok=True)
            self.concatenate_ordered_files(source_rules_dir, copilot_dest_path)
            print(f"Updated GitHub Copilot instructions at {copilot_dest_path}")
            
        print(f"Rules synced successfully from {source_rules_dir}")
        return 0

    def _sync_assistant_rules(self, source_dir: Path, target_root: Path, assistants: List[str]) -> None:
        """
        Sync rules for specific AI assistants by removing and regenerating their directories.
        
        Args:
            source_dir: Source directory (project_rules/)
            target_root: Target project root directory
            assistants: List of assistant names to sync
        """
        for assistant in assistants:
            if assistant == 'cursor':
                self._sync_cursor_rules(source_dir, target_root)
            elif assistant == 'windsurf':
                self._sync_windsurf_rules(source_dir, target_root)
            elif assistant == 'cline':
                self._sync_cline_rules(source_dir, target_root)
            elif assistant == 'roo':
                self._sync_roo_rules(source_dir, target_root)
            else:
                print(f"Warning: Unknown assistant '{assistant}' - skipping")

    def _sync_cursor_rules(self, source_dir: Path, target_root: Path) -> None:
        """Sync rules for Cursor AI assistant (.cursor/rules/*.mdc)."""
        target_dir = target_root / TARGET_CURSOR_DIR
        if target_dir.exists():
            shutil.rmtree(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        
        count = self.copy_and_number_files(source_dir, target_dir, extension_mode='add_mdc')
        print(f"Synced {count} Cursor rule files in {target_dir}")

    def _sync_windsurf_rules(self, source_dir: Path, target_root: Path) -> None:
        """Sync rules for Windsurf AI assistant (.windsurf/rules/*.md)."""
        target_dir = target_root / TARGET_WINDSURF_DIR
        if target_dir.exists():
            shutil.rmtree(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        
        count = self.copy_and_number_files(source_dir, target_dir, extension_mode='add_md')
        print(f"Synced {count} Windsurf rule files in {target_dir}")

    def _sync_cline_rules(self, source_dir: Path, target_root: Path) -> None:
        """Sync rules for Cline AI assistant (.clinerules/)."""
        target_dir = target_root / TARGET_CLINE_DIR
        if target_dir.exists():
            shutil.rmtree(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        
        count = self.copy_and_number_files(source_dir, target_dir, extension_mode='remove')
        print(f"Synced {count} Cline rule files in {target_dir}")

    def _sync_roo_rules(self, source_dir: Path, target_root: Path) -> None:
        """Sync rules for RooCode AI assistant (.roo/rules/)."""
        target_dir = target_root / TARGET_ROO_DIR
        if target_dir.exists():
            shutil.rmtree(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        
        count = self.copy_and_restructure_roocode(source_dir, target_dir)
        print(f"Synced {count} RooCode rule files in {target_dir}")

    def clean_rules(self, project_dir: Optional[str] = None) -> int:
        """
        Clean rules from a target project directory.
        
        Args:
            project_dir: Target project directory. If None, uses current project root.
            
        Returns:
            int: Return code (0 for success, non-zero for error)
        """
        if project_dir is not None:
            target_root = Path(project_dir).absolute()
        else:
            target_root = self.project_root
            
        # Set target directories based on provided project directory
        target_rules_dir = target_root / TARGET_PROJECT_RULES_DIR
        target_github_dir = target_root / TARGET_GITHUB_COPILOT_DIR
        copilot_file = target_github_dir / TARGET_COPILOT_INSTRUCTIONS_FILE
        
        # Clean rules directory
        if target_rules_dir.exists():
            shutil.rmtree(target_rules_dir)
            print(f"Removed rules directory: {target_rules_dir}")
            
        # Clean assistant-specific directories
        assistant_dirs = [
            (target_root / TARGET_CURSOR_DIR, "Cursor"),
            (target_root / TARGET_WINDSURF_DIR, "Windsurf"), 
            (target_root / TARGET_CLINE_DIR, "Cline"),
            (target_root / TARGET_ROO_DIR, "RooCode")
        ]
        
        for dir_path, name in assistant_dirs:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"Removed {name} rules directory: {dir_path}")
            
        # Clean GitHub Copilot instructions
        if copilot_file.exists():
            copilot_file.unlink()
            print(f"Removed GitHub Copilot instructions: {copilot_file}")
            
        print("Rules cleaned successfully.")
        return 0

    def clean_all(self, project_dir: Optional[str] = None) -> int:
        """
        Clean all rulebook-ai files from a target project directory.
        
        Args:
            project_dir: Target project directory. If None, uses current project root.
            
        Returns:
            int: Return code (0 for success, non-zero for error)
        """
        if project_dir is not None:
            target_root = Path(project_dir).absolute()
        else:
            target_root = self.project_root
            
        # Set target directories based on provided project directory
        target_rules_dir = target_root / TARGET_PROJECT_RULES_DIR
        target_memory_dir = target_root / TARGET_MEMORY_BANK_DIR
        target_tools_dir = target_root / TARGET_TOOLS_DIR
        target_github_dir = target_root / TARGET_GITHUB_COPILOT_DIR
        copilot_file = target_github_dir / TARGET_COPILOT_INSTRUCTIONS_FILE
        
        # Clean all directories
        cleaned_count = 0
        
        if target_rules_dir.exists():
            shutil.rmtree(target_rules_dir)
            cleaned_count += 1
            print(f"Removed rules directory: {target_rules_dir}")
            
        if target_memory_dir.exists():
            shutil.rmtree(target_memory_dir)
            cleaned_count += 1
            print(f"Removed memory directory: {target_memory_dir}")
            
        if target_tools_dir.exists():
            shutil.rmtree(target_tools_dir)
            cleaned_count += 1
            print(f"Removed tools directory: {target_tools_dir}")
            
        if copilot_file.exists():
            copilot_file.unlink()
            cleaned_count += 1
            print(f"Removed GitHub Copilot instructions: {copilot_file}")
            
        if cleaned_count == 0:
            print("No rulebook-ai files found to clean.")
        else:
            print("All rulebook-ai files cleaned successfully.")
            
        return 0

    def list_rules(self) -> List[str]:
        """
        List all available rule sets.
        
        Returns:
            List of available rule set names
        """
        if not self.source_rules_dir.exists():
            print(f"Error: Rules directory {self.source_rules_dir} not found.")
            return []
            
        rule_sets = [
            p.name for p in self.source_rules_dir.iterdir() 
            if p.is_dir() and not p.name.startswith('.')
        ]
        
        return sorted(rule_sets)
