"""
Core functionality for rulebook-ai rule management.

This module provides the core functionality for managing AI rulebooks,
separated from the CLI interface for better modularity and testing.
"""

import os
import shutil
import re
import json
import yaml
from pathlib import Path
from typing import List, Optional
import webbrowser

from .assistants import AssistantSpec, SUPPORTED_ASSISTANTS, ASSISTANT_MAP

# --- Constants ---
SOURCE_PACKS_DIR = "packs"

TARGET_PROJECT_RULES_DIR = "project_rules"
TARGET_MEMORY_BANK_DIR = "memory"
TARGET_TOOLS_DIR = "tools"
TARGET_INTERNAL_STATE_DIR = ".rulebook-ai"

DEFAULT_RULE_SET = "light-spec"

SOURCE_ENV_EXAMPLE_FILE = ".env.example"
SOURCE_REQUIREMENTS_TXT_FILE = "requirements.txt"

BUG_REPORT_URL = "https://github.com/botingw/rulebook-ai/issues"
RATINGS_REVIEWS_URL = (
    "https://github.com/botingw/rulebook-ai/wiki/Ratings-%26-Reviews-(Rulesets)"
)


class RuleManager:
    """Manages the installation and synchronization of AI rules and related files."""

    def __init__(self, project_root: Optional[str] = None) -> None:
        self.package_path = Path(__file__).parent.absolute()
        self.source_packs_dir = self.package_path / SOURCE_PACKS_DIR
        
        # Handle development environment structure
        if not self.source_packs_dir.exists():
            dev_root = self.package_path.parent.parent
            self.source_packs_dir = dev_root / SOURCE_PACKS_DIR
        
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

    def _copy_tree_non_destructive_with_map(self, src_dir: Path, dest_dir: Path, project_root: Path) -> List[str]:
        copied_files = []
        if not src_dir.is_dir():
            return []

        dest_dir.mkdir(parents=True, exist_ok=True)

        for item in src_dir.iterdir():
            dest_item = dest_dir / item.name
            if item.is_dir():
                copied_files.extend(self._copy_tree_non_destructive_with_map(item, dest_item, project_root))
            elif not dest_item.exists():
                if self._copy_file(item, dest_item):
                    copied_files.append(str(dest_item.relative_to(project_root)))
        return copied_files

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

        if spec.has_modes:
            total_files = 0
            for source_sub_dir in source_dir.iterdir():
                if not source_sub_dir.is_dir() or source_sub_dir.name.startswith('.'):
                    continue

                mode_name = re.sub(r"^\d+-", "", source_sub_dir.name)
                target_mode_dir = target_path / mode_name
                
                count = self._strategy_preserve_hierarchy(source_sub_dir, target_mode_dir)
                if count > 0:
                    print(f"  -> Generated {count} {spec.display_name} '{mode_name}' rules in {target_mode_dir}")
                    total_files += count
            
            if total_files == 0:
                print(f"  -> No rules found to generate for {spec.display_name}")
            return

        count = 0
        if spec.supports_subdirectories:
            count = self._strategy_preserve_hierarchy(source_dir, target_path)
        else:
            count = self._strategy_flatten_and_number(source_dir, target_path, spec.file_extension)
        
        if count > 0:
            print(f"  -> Generated {count} {spec.display_name} rule files in {target_path}")

    # --- Public Command Methods ---

    def install(self, rule_set: str = DEFAULT_RULE_SET, project_dir: Optional[str] = None,
                clean_first: bool = False, assistants: Optional[List[str]] = None) -> int:
        target_root = Path(project_dir).absolute() if project_dir else self.project_root

        pack_source_dir = self.source_packs_dir / rule_set

        if clean_first:
            self.clean_rules(str(target_root))

        if not pack_source_dir.is_dir():
            print(f"Error: Pack '{rule_set}' not found.")
            self.list_packs()
            return 1

        # Create .rulebook-ai directory structure
        rulebook_ai_dir = target_root / TARGET_INTERNAL_STATE_DIR
        rulebook_ai_packs_dir = rulebook_ai_dir / "packs"
        rulebook_ai_dir.mkdir(exist_ok=True)
        rulebook_ai_packs_dir.mkdir(exist_ok=True)

        # Copy pack source to .rulebook-ai/packs
        dest_pack_dir = rulebook_ai_packs_dir / rule_set
        if dest_pack_dir.exists():
            shutil.rmtree(dest_pack_dir)
        shutil.copytree(pack_source_dir, dest_pack_dir)
        print(f"- Stored pack '{rule_set}' in '{dest_pack_dir}'")

        # Update selection.json
        selection_file = rulebook_ai_dir / "selection.json"
        selection = {"packs": []}
        if selection_file.exists():
            with open(selection_file, 'r') as f:
                selection = json.load(f)

        manifest_file = dest_pack_dir / "manifest.yaml"
        if not manifest_file.exists():
            print(f"Warning: manifest.yaml not found for pack '{rule_set}'. Using version 0.0.0.")
            version = "0.0.0"
        else:
            with open(manifest_file, 'r') as f:
                manifest = yaml.safe_load(f)
                version = manifest.get("version", "0.0.0")

        # Avoid adding duplicate packs
        if not any(p['name'] == rule_set for p in selection['packs']):
            selection['packs'].append({"name": rule_set, "version": version})

        with open(selection_file, 'w') as f:
            json.dump(selection, f, indent=2)
        print(f"- Updated '{selection_file}'")


        print(f"Installing framework components from pack '{rule_set}'...")
        # 1. Copy rule set (destructive)
        target_rules_dir = target_root / TARGET_PROJECT_RULES_DIR
        rule_set_source_dir = pack_source_dir / 'rules'
        if rule_set_source_dir.is_dir():
            if target_rules_dir.exists():
                shutil.rmtree(target_rules_dir)
            shutil.copytree(rule_set_source_dir, target_rules_dir)
            print(f"- Copied rule set to '{target_rules_dir}'")

        # 2. Copy memory and tools (non-destructive) and create file map
        file_map = {"files": []}
        for starter_subdir, target_dir_name in [("memory_starters", TARGET_MEMORY_BANK_DIR), ("tool_starters", TARGET_TOOLS_DIR)]:
            starter_dir = pack_source_dir / starter_subdir
            if starter_dir.is_dir():
                target_dir = target_root / target_dir_name
                copied = self._copy_tree_non_destructive_with_map(starter_dir, target_dir, target_root)
                file_map["files"].extend(copied)

        # Save the file map
        if file_map["files"]:
            file_map_path = dest_pack_dir / "file-map.json"
            with open(file_map_path, 'w') as f:
                json.dump(file_map, f, indent=2)
            print(f"- Created file map with {len(file_map['files'])} entries in '{file_map_path}'")

        # 3. Per spec, run the sync logic
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
                # Attempt to remove empty parent directories (e.g., .github, .gemini)
                try:
                    parent = path_to_clean.parent
                    if parent != target_root and not any(parent.iterdir()):
                        parent.rmdir()
                        print(f"- Removed empty directory: {parent}")
                except OSError:
                    pass  # Ignore if not empty or other error
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
        for item in [TARGET_MEMORY_BANK_DIR, TARGET_TOOLS_DIR]:
            item_path = target_root / item
            if item_path.is_file() and item_path.exists():
                item_path.unlink()
                print(f"- Removed: {item_path}")
            elif item_path.is_dir() and item_path.exists():
                shutil.rmtree(item_path)
                print(f"- Removed: {item_path}")
        
        print("\nFull cleaning complete.")
        return 0

    def list_packs(self) -> None:
        if not self.source_packs_dir.is_dir():
            print(f"Error: Packs directory {self.source_packs_dir} not found.")
            return
        print("Available packs:")
        for p in sorted([p.name for p in self.source_packs_dir.iterdir() if p.is_dir() and not p.name.startswith('.')]):
            print(f"  - {p}")
        print(f"\nFor ratings and reviews of these rule sets, visit {RATINGS_REVIEWS_URL}")

    def report_bug(self) -> int:
        """Provide the project issue tracker URL for reporting bugs."""
        print(f"To report a bug, please visit {BUG_REPORT_URL}")
        try:
            webbrowser.open(BUG_REPORT_URL)
        except Exception:
            pass
        return 0

    def rate_ruleset(self) -> int:
        """Open the ratings and reviews wiki page for rulesets."""
        print(f"For ratings and reviews, please visit {RATINGS_REVIEWS_URL}")
        try:
            webbrowser.open(RATINGS_REVIEWS_URL)
        except Exception:
            pass
        return 0
