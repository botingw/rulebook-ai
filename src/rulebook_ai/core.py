"""
Core functionality for rulebook-ai rule management.

This module provides the core functionality for managing AI rulebooks,
separated from the CLI interface for better modularity and testing.
"""

import os
import shutil
import re
from pathlib import Path
from typing import List, Optional

from .assistants import AssistantSpec, SUPPORTED_ASSISTANTS, ASSISTANT_MAP

# --- Constants ---
SOURCE_RULE_SETS_DIR = "rule_sets"
SOURCE_MEMORY_STARTERS_DIR = "memory_starters"
SOURCE_TOOL_STARTERS_DIR = "tool_starters"

TARGET_PROJECT_RULES_DIR = "project_rules"
TARGET_MEMORY_BANK_DIR = "memory"
TARGET_TOOLS_DIR = "tools"

DEFAULT_RULE_SET = "light-spec"

SOURCE_ENV_EXAMPLE_FILE = ".env.example"
SOURCE_REQUIREMENTS_TXT_FILE = "requirements.txt"


class RuleManager:
    """Manages the installation and synchronization of AI rules and related files."""

    def __init__(self, project_root: Optional[str] = None) -> None:
        self.package_path = Path(__file__).parent.absolute()
        self.source_rules_dir = self.package_path / SOURCE_RULE_SETS_DIR
        self.source_memory_dir = self.package_path / SOURCE_MEMORY_STARTERS_DIR
        self.source_tools_dir = self.package_path / SOURCE_TOOL_STARTERS_DIR
        
        # Handle development environment structure
        if not self.source_rules_dir.exists():
            dev_root = self.package_path.parent.parent
            self.source_rules_dir = dev_root / SOURCE_RULE_SETS_DIR
            self.source_memory_dir = dev_root / SOURCE_MEMORY_STARTERS_DIR
            self.source_tools_dir = dev_root / SOURCE_TOOL_STARTERS_DIR
        
        self.project_root = Path(project_root).absolute() if project_root else Path.cwd().absolute()

    # --- Private File Operation Helpers ---

    def _copy_file(self, source: Path, destination: Path) -> bool:
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            return True
        except Exception as e:
            print(f"Error copying {source} to {destination}: {e}")
            return False

    def _get_ordered_source_files(self, source_dir_path: Path, recursive: bool) -> List[Path]:
        if not source_dir_path.is_dir():
            return []
        pattern = "**/*" if recursive else "*"
        all_files = [p for p in source_dir_path.glob(pattern) if p.is_file() and not p.name.startswith('.')]
        return sorted(all_files)

    def _copy_tree_non_destructive(self, src_dir: Path, dest_dir: Path) -> int:
        dest_dir.mkdir(parents=True, exist_ok=True)
        count = 0
        if not src_dir.is_dir():
            return 0
        for item in src_dir.iterdir():
            dest_item = dest_dir / item.name
            if item.is_dir():
                if not dest_item.exists():
                    shutil.copytree(item, dest_item)
                    count += 1
                else:
                    count += self._copy_tree_non_destructive(item, dest_item)
            elif not dest_item.exists() and self._copy_file(item, dest_item):
                count += 1
        return count

    # --- Private Rule Generation Strategies ---

    def _strategy_flatten_and_number(self, source_dir: Path, dest_dir: Path, extension: Optional[str]) -> int:
        dest_dir.mkdir(parents=True, exist_ok=True)
        all_source_files = self._get_ordered_source_files(source_dir, recursive=True)
        if not all_source_files:
            return 0
        
        next_num = 1
        for source_path in all_source_files:
            stem = re.sub(r"^\d+-", "", source_path.stem)
            new_extension = extension if extension is not None else ''
            new_filename = f"{next_num:02d}-{stem}{new_extension}"
            if self._copy_file(source_path, dest_dir / new_filename):
                next_num += 1
        return len(all_source_files)

    def _strategy_preserve_hierarchy(self, source_dir: Path, dest_dir: Path) -> int:
        dest_dir.mkdir(parents=True, exist_ok=True)
        all_source_files = self._get_ordered_source_files(source_dir, recursive=True)
        if not all_source_files:
            return 0
        for source_path in all_source_files:
            dest_path = dest_dir / source_path.relative_to(source_dir)
            self._copy_file(source_path, dest_path)
        return len(all_source_files)

    def _strategy_concatenate_files(self, source_dir: Path, dest_file: Path) -> None:
        all_source_files = self._get_ordered_source_files(source_dir, recursive=True)
        if not all_source_files:
            return
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_file, 'w', encoding='utf-8') as output_file:
            for i, source_path in enumerate(all_source_files):
                output_file.write(f"# Rule: {source_path.name}\n\n")
                output_file.write(source_path.read_text(encoding='utf-8'))
                if i < len(all_source_files) - 1:
                    output_file.write("\n\n---\n\n")

    # --- Private Generic Generation Engine ---

    def _generate_for_assistant(self, spec: AssistantSpec, source_dir: Path, target_root: Path):
        target_path = target_root / spec.rule_path
        
        if not spec.is_multi_file:
            dest_file = target_path / spec.filename
            self._strategy_concatenate_files(source_dir, dest_file)
            print(f"  -> Generated {spec.display_name} instructions at {dest_file}")
            return

        count = 0
        if not spec.supports_subdirectories:
            count = self._strategy_flatten_and_number(source_dir, target_path, spec.file_extension)
        else:
            count = self._strategy_preserve_hierarchy(source_dir, target_path)
        
        if count > 0:
            print(f"  -> Generated {count} {spec.display_name} rule files in {target_path}")

    # --- Public Command Methods ---

    def install(self, rule_set: str = DEFAULT_RULE_SET, project_dir: Optional[str] = None,
                clean_first: bool = False, assistants: Optional[List[str]] = None) -> int:
        target_root = Path(project_dir).absolute() if project_dir else self.project_root
        target_rules_dir = target_root / TARGET_PROJECT_RULES_DIR
        rule_set_source_dir = self.source_rules_dir / rule_set

        if clean_first:
            self.clean_rules(str(target_root))

        if not rule_set_source_dir.is_dir():
            print(f"Error: Rule set '{rule_set}' not found.")
            self.list_rules()
            return 1

        print(f"Installing framework components from rule set '{rule_set}'...")
        # 1. Copy rule set (destructive)
        if target_rules_dir.exists():
            shutil.rmtree(target_rules_dir)
        shutil.copytree(rule_set_source_dir, target_rules_dir)
        print(f"- Copied rule set to '{target_rules_dir}'")

        # 2. Copy memory and tools (non-destructive)
        for starter, target in [(self.source_memory_dir, TARGET_MEMORY_BANK_DIR), (self.source_tools_dir, TARGET_TOOLS_DIR)]:
            count = self._copy_tree_non_destructive(starter, target_root / target)
            if count > 0:
                print(f"- Copied {count} files to '{target_root / target}'")

        # 3. Copy env and requirements (non-destructive)
        for filename in [SOURCE_ENV_EXAMPLE_FILE, SOURCE_REQUIREMENTS_TXT_FILE]:
            source_file = self.source_rules_dir.parent / filename
            if source_file.is_file() and not (target_root / filename).exists():
                self._copy_file(source_file, target_root / filename)
                print(f"- Created '{target_root / filename}'")
            
        # 4. Per spec, run the sync logic
        print("\nRunning initial synchronization...")
        self.sync(str(target_root), assistants)
                
        print(f"\nInstallation complete.")
        return 0

    def sync(self, project_dir: Optional[str] = None, assistants: Optional[List[str]] = None) -> int:
        target_root = Path(project_dir).absolute() if project_dir else self.project_root
        source_rules_dir = target_root / TARGET_PROJECT_RULES_DIR
        
        if not source_rules_dir.is_dir():
            print(f"Error: '{source_rules_dir}' does not exist. Run 'install' first.")
            return 1
            
        names_to_sync = assistants
        if names_to_sync is None:
            # Per the design spec, sync with no flags defaults to all assistants
            names_to_sync = [a.name for a in SUPPORTED_ASSISTANTS]

        if not names_to_sync:
            print("No assistants selected to sync. Use --[assistant] or --all to specify.")
            return 0
        
        print(f"Syncing rules from '{source_rules_dir}' for: {', '.join(names_to_sync)}")
        for name in names_to_sync:
            spec = ASSISTANT_MAP.get(name)
            if not spec: continue

            # 1. Clean the existing rules for the assistant
            path_to_clean = target_root / spec.clean_path
            if path_to_clean.is_dir():
                shutil.rmtree(path_to_clean)
            elif path_to_clean.is_file():
                path_to_clean.unlink()

            # 2. Regenerate the rules from project_rules/
            self._generate_for_assistant(spec, source_rules_dir, target_root)
            
        print("\nSync complete.")
        return 0

    def clean_rules(self, project_dir: Optional[str] = None) -> int:
        target_root = Path(project_dir).absolute() if project_dir else self.project_root
        print("Cleaning rule-related files and directories...")
        
        # 1. Remove the project_rules directory
        rules_dir = target_root / TARGET_PROJECT_RULES_DIR
        if rules_dir.exists():
            shutil.rmtree(rules_dir)
            print(f"- Removed: {rules_dir}")
            
        # 2. Remove all generated assistant rules (data-driven)
        for spec in SUPPORTED_ASSISTANTS:
            path_to_clean = target_root / spec.clean_path
            if path_to_clean.is_file() and path_to_clean.exists():
                path_to_clean.unlink()
                print(f"- Removed: {path_to_clean}")
                # Attempt to remove parent if it's an empty .github dir
                if spec.name == 'copilot':
                    try:
                        if not any(path_to_clean.parent.iterdir()):
                            path_to_clean.parent.rmdir()
                            print(f"- Removed empty directory: {path_to_clean.parent}")
                    except OSError:
                        pass # Ignore if not empty or other error
            elif path_to_clean.is_dir() and path_to_clean.exists():
                shutil.rmtree(path_to_clean)
                print(f"- Removed: {path_to_clean}")
            
        print("\nRule cleaning complete.")
        return 0

    def clean_all(self, project_dir: Optional[str] = None) -> int:
        target_root = Path(project_dir).absolute() if project_dir else self.project_root
        
        # 1. Run clean_rules first
        self.clean_rules(str(target_root))
        
        # 2. Remove the remaining framework directories and files
        print("\nCleaning all remaining framework components...")
        for item in [TARGET_MEMORY_BANK_DIR, TARGET_TOOLS_DIR, SOURCE_ENV_EXAMPLE_FILE, SOURCE_REQUIREMENTS_TXT_FILE]:
            item_path = target_root / item
            if item_path.is_file() and item_path.exists():
                item_path.unlink()
                print(f"- Removed: {item_path}")
            elif item_path.is_dir() and item_path.exists():
                shutil.rmtree(item_path)
                print(f"- Removed: {item_path}")
        
        print("\nFull cleaning complete.")
        return 0

    def list_rules(self) -> None:
        if not self.source_rules_dir.is_dir():
            print(f"Error: Rules directory {self.source_rules_dir} not found.")
            return
        print("Available rule sets:")
        for p in sorted([p.name for p in self.source_rules_dir.iterdir() if p.is_dir() and not p.name.startswith('.')]):
            print(f"  - {p}")
