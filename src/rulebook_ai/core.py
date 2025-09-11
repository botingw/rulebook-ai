"""Core logic for the rulebook-ai CLI."""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

import webbrowser
import yaml

from .assistants import ASSISTANT_MAP, SUPPORTED_ASSISTANTS, AssistantSpec

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SOURCE_PACKS_DIR = "packs"

TARGET_MEMORY_BANK_DIR = "memory"
TARGET_TOOLS_DIR = "tools"
TARGET_INTERNAL_STATE_DIR = ".rulebook-ai"

BUG_REPORT_URL = "https://github.com/botingw/rulebook-ai/issues"
RATINGS_REVIEWS_URL = (
    "https://github.com/botingw/rulebook-ai/wiki/Ratings-%26-Reviews-(Rulesets)"
)


# ---------------------------------------------------------------------------
# Helper data structures
# ---------------------------------------------------------------------------

@dataclass
class SelectionState:
    packs: List[Dict[str, str]]
    profiles: Dict[str, List[str]]


# ---------------------------------------------------------------------------
# RuleManager
# ---------------------------------------------------------------------------


class RuleManager:
    """Manage packs, profiles and project synchronization."""

    def __init__(self, project_root: Optional[str] = None) -> None:
        package_path = Path(__file__).parent.absolute()
        self.source_packs_dir = package_path / SOURCE_PACKS_DIR
        if not self.source_packs_dir.exists():
            dev_root = package_path.parent.parent
            self.source_packs_dir = dev_root / SOURCE_PACKS_DIR

        self.project_root = Path(project_root).absolute() if project_root else Path.cwd().absolute()

    # ------------------------------------------------------------------
    # Internal utilities
    # ------------------------------------------------------------------

    def _copy_file(self, source: Path, destination: Path) -> bool:
        destination.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(source, destination)
            return True
        except Exception as e:  # pragma: no cover - defensive programming
            print(f"Error copying {source} to {destination}: {e}")
            return False

    def _get_ordered_source_files(self, source_dir: Path, recursive: bool) -> List[Path]:
        if not source_dir.is_dir():
            return []
        pattern = "**/*" if recursive else "*"
        files = [p for p in source_dir.glob(pattern) if p.is_file() and not p.name.startswith(".")]
        return sorted(files)

    def _copy_tree_non_destructive(self, src: Path, dest: Path, project_root: Path) -> List[str]:
        """Copy tree from src to dest without overwriting existing files.

        Returns a list of relative file paths that were created.
        """

        created: List[str] = []
        if not src.is_dir():
            return created

        dest.mkdir(parents=True, exist_ok=True)
        for item in src.iterdir():
            dest_item = dest / item.name
            if item.is_dir():
                created.extend(self._copy_tree_non_destructive(item, dest_item, project_root))
            elif not dest_item.exists():
                if self._copy_file(item, dest_item):
                    created.append(str(dest_item.relative_to(project_root)))
        return created

    def _strategy_flatten_and_number(self, source: Path, dest: Path, extension: Optional[str]) -> int:
        dest.mkdir(parents=True, exist_ok=True)
        files = self._get_ordered_source_files(source, True)
        next_num = 1
        for src in files:
            stem = re.sub(r"^\d+-", "", src.stem)
            new_ext = extension if extension is not None else ""
            name = f"{next_num:02d}-{stem}{new_ext}"
            if self._copy_file(src, dest / name):
                next_num += 1
        return len(files)

    def _strategy_preserve_hierarchy(self, source: Path, dest: Path) -> int:
        dest.mkdir(parents=True, exist_ok=True)
        files = self._get_ordered_source_files(source, True)
        for src in files:
            self._copy_file(src, dest / src.relative_to(source))
        return len(files)

    def _strategy_concatenate_files(self, source: Path, dest_file: Path) -> None:
        files = self._get_ordered_source_files(source, True)
        if not files:
            return
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        with dest_file.open("w", encoding="utf-8") as f:
            for i, src in enumerate(files):
                f.write(f"# Rule: {src.name}\n\n")
                f.write(src.read_text(encoding="utf-8"))
                if i < len(files) - 1:
                    f.write("\n\n---\n\n")

    def _generate_for_assistant(self, spec: AssistantSpec, source_dir: Path, target_root: Path) -> None:
        target_path = target_root / spec.rule_path
        if not spec.is_multi_file:
            self._strategy_concatenate_files(source_dir, target_path / spec.filename)
            print(f"  -> Generated {spec.display_name} instructions at {target_path / spec.filename}")
            return

        if spec.has_modes:
            total = 0
            for sub in source_dir.iterdir():
                if not sub.is_dir() or sub.name.startswith("."):
                    continue
                mode_name = re.sub(r"^\d+-", "", sub.name)
                count = self._strategy_preserve_hierarchy(sub, target_path / mode_name)
                if count:
                    print(f"  -> Generated {count} {spec.display_name} '{mode_name}' rules in {target_path / mode_name}")
                    total += count
            if not total:
                print(f"  -> No rules found to generate for {spec.display_name}")
            return

        count = (
            self._strategy_preserve_hierarchy(source_dir, target_path)
            if spec.supports_subdirectories
            else self._strategy_flatten_and_number(source_dir, target_path, spec.file_extension)
        )
        if count:
            print(f"  -> Generated {count} {spec.display_name} rule files in {target_path}")

    # ------------------------------------------------------------------
    # Selection and manifest helpers
    # ------------------------------------------------------------------

    def _selection_path(self, project_root: Path) -> Path:
        return project_root / TARGET_INTERNAL_STATE_DIR / "selection.json"

    def _load_selection(self, project_root: Path) -> SelectionState:
        path = self._selection_path(project_root)
        if not path.exists():
            return SelectionState(packs=[], profiles={})
        data = json.loads(path.read_text())
        return SelectionState(packs=data.get("packs", []), profiles=data.get("profiles", {}))

    def _save_selection(self, project_root: Path, state: SelectionState) -> None:
        path = self._selection_path(project_root)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as f:
            json.dump({"packs": state.packs, "profiles": state.profiles}, f, indent=2)

    def _file_manifest_path(self, project_root: Path) -> Path:
        return project_root / TARGET_INTERNAL_STATE_DIR / "file_manifest.json"

    def _load_file_manifest(self, project_root: Path) -> Dict[str, str]:
        path = self._file_manifest_path(project_root)
        if path.exists():
            return json.loads(path.read_text())
        return {}

    def _save_file_manifest(self, project_root: Path, manifest: Dict[str, str]) -> None:
        path = self._file_manifest_path(project_root)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as f:
            json.dump(manifest, f, indent=2)

    def _sync_status_path(self, project_root: Path) -> Path:
        return project_root / TARGET_INTERNAL_STATE_DIR / "sync_status.json"

    def _load_sync_status(self, project_root: Path) -> Dict[str, dict]:
        path = self._sync_status_path(project_root)
        if path.exists():
            return json.loads(path.read_text())
        return {}

    def _save_sync_status(self, project_root: Path, data: Dict[str, dict]) -> None:
        path = self._sync_status_path(project_root)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as f:
            json.dump(data, f, indent=2)

    # ------------------------------------------------------------------
    # Pack commands
    # ------------------------------------------------------------------

    def _builtin_packs(self) -> List[Dict[str, str]]:
        if not self.source_packs_dir.is_dir():
            return []
        packs = []
        for pack_dir in sorted(
            [p for p in self.source_packs_dir.iterdir() if p.is_dir() and not p.name.startswith(".")],
            key=lambda p: p.name,
        ):
            manifest_path = pack_dir / "manifest.yaml"
            version = "unknown"
            summary = ""
            if manifest_path.exists():
                manifest = yaml.safe_load(manifest_path.read_text()) or {}
                version = manifest.get("version", "unknown")
                summary = manifest.get("summary", "")
            packs.append({"name": pack_dir.name, "version": version, "summary": summary})
        return packs

    def list_packs(self) -> None:
        builtins = self._builtin_packs()
        from . import community_packs

        index = community_packs.load_index_cache().get("packs", [])

        print("Available packs:")
        for entry in sorted(
            [
                {**b, "source": "built-in"} for b in builtins
            ]
            + [
                {"name": p.get("name"), "description": p.get("description"), "source": "community"}
                for p in index
            ],
            key=lambda e: e["name"],
        ):
            if entry["source"] == "built-in":
                print(
                    f"  - {entry['name']} (built-in, v{entry['version']}) - {entry['summary']}"
                )
            else:
                print(
                    f"  - {entry['name']} (community) - {entry['description']}"
                )

        print(f"\nFor ratings and reviews of these packs, visit {RATINGS_REVIEWS_URL}")

    def add_pack(self, name: str, project_dir: Optional[str] = None) -> int:
        project_root = Path(project_dir).absolute() if project_dir else self.project_root

        if "/" in name:
            from . import community_packs

            return community_packs.add_pack_from_slug(
                name,
                project_root,
                self.source_packs_dir,
                self._load_selection,
                self._save_selection,
            )

        source = self.source_packs_dir / name
        if not source.is_dir():
            from . import community_packs

            result = community_packs.add_pack_from_index(
                name,
                project_root,
                self.source_packs_dir,
                self._load_selection,
                self._save_selection,
            )
            if result != 0:
                print(f"Pack '{name}' not found.")
                self.list_packs()
            return result

        dest_dir = project_root / TARGET_INTERNAL_STATE_DIR / "packs" / name
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        dest_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, dest_dir)

        # Update selection.json
        selection = self._load_selection(project_root)
        manifest_file = dest_dir / "manifest.yaml"
        version = "0.0.0"
        if manifest_file.exists():
            manifest = yaml.safe_load(manifest_file.read_text()) or {}
            version = manifest.get("version", "0.0.0")
        if not any(p["name"] == name for p in selection.packs):
            selection.packs.append({"name": name, "version": version})
        self._save_selection(project_root, selection)

        print(f"Added pack '{name}'. Run 'project sync' to apply changes.")
        return 0

    def update_community_index(self) -> int:
        from . import community_packs

        return community_packs.update_index_cache()

    def remove_pack(self, name: str, project_dir: Optional[str] = None) -> int:
        project_root = Path(project_dir).absolute() if project_dir else self.project_root
        dest_dir = project_root / TARGET_INTERNAL_STATE_DIR / "packs" / name
        if not dest_dir.exists():
            print(f"Pack '{name}' is not installed.")
            return 1

        shutil.rmtree(dest_dir)

        selection = self._load_selection(project_root)
        selection.packs = [p for p in selection.packs if p["name"] != name]
        for profile, packs in list(selection.profiles.items()):
            if name in packs:
                packs.remove(name)
                selection.profiles[profile] = packs
        self._save_selection(project_root, selection)

        print(f"Removed pack '{name}'. Remember to run 'project sync' to update rules.")
        return 0

    def packs_status(self, project_dir: Optional[str] = None) -> int:
        project_root = Path(project_dir).absolute() if project_dir else self.project_root
        selection = self._load_selection(project_root)
        if not selection.packs:
            print("No packs are configured.")
            return 0

        print("Pack library:")
        for idx, pack in enumerate(selection.packs, 1):
            version = pack.get("version", "unknown")
            print(f"  {idx}. {pack['name']} (v{version})")

        if selection.profiles:
            print("\nProfiles:")
            for profile, packs in selection.profiles.items():
                print(f"  - {profile}: {', '.join(packs)}")
        return 0

    # ------------------------------------------------------------------
    # Profile commands
    # ------------------------------------------------------------------

    def create_profile(self, name: str, project_dir: Optional[str] = None) -> int:
        project_root = Path(project_dir).absolute() if project_dir else self.project_root
        selection = self._load_selection(project_root)
        if name in selection.profiles:
            print(f"Profile '{name}' already exists.")
            return 1
        selection.profiles[name] = []
        self._save_selection(project_root, selection)
        print(f"Created profile '{name}'.")
        return 0

    def delete_profile(self, name: str, project_dir: Optional[str] = None) -> int:
        project_root = Path(project_dir).absolute() if project_dir else self.project_root
        selection = self._load_selection(project_root)
        if name not in selection.profiles:
            print(f"Profile '{name}' does not exist.")
            return 1
        del selection.profiles[name]
        self._save_selection(project_root, selection)
        print(f"Deleted profile '{name}'.")
        return 0

    def add_pack_to_profile(self, pack: str, profile: str, project_dir: Optional[str] = None) -> int:
        project_root = Path(project_dir).absolute() if project_dir else self.project_root
        selection = self._load_selection(project_root)
        if pack not in [p["name"] for p in selection.packs]:
            print(f"Pack '{pack}' is not in the library.")
            return 1
        if profile not in selection.profiles:
            print(f"Profile '{profile}' does not exist.")
            return 1
        if pack not in selection.profiles[profile]:
            selection.profiles[profile].append(pack)
        self._save_selection(project_root, selection)
        print(f"Added pack '{pack}' to profile '{profile}'.")
        return 0

    def remove_pack_from_profile(self, pack: str, profile: str, project_dir: Optional[str] = None) -> int:
        project_root = Path(project_dir).absolute() if project_dir else self.project_root
        selection = self._load_selection(project_root)
        if profile not in selection.profiles or pack not in selection.profiles[profile]:
            print(f"Pack '{pack}' is not in profile '{profile}'.")
            return 1
        selection.profiles[profile].remove(pack)
        self._save_selection(project_root, selection)
        print(f"Removed pack '{pack}' from profile '{profile}'.")
        return 0

    def list_profiles(self, project_dir: Optional[str] = None) -> int:
        project_root = Path(project_dir).absolute() if project_dir else self.project_root
        selection = self._load_selection(project_root)
        if not selection.profiles:
            print("No profiles defined.")
            return 0
        for name, packs in selection.profiles.items():
            print(f"{name}: {', '.join(packs)}")
        return 0

    # ------------------------------------------------------------------
    # Project commands
    # ------------------------------------------------------------------

    def project_sync(
        self,
        assistants: Optional[List[str]] = None,
        profile: Optional[str] = None,
        packs: Optional[List[str]] = None,
        project_dir: Optional[str] = None,
    ) -> int:
        project_root = Path(project_dir).absolute() if project_dir else self.project_root
        selection = self._load_selection(project_root)

        if profile and packs:
            print("Cannot specify both --profile and --pack flags.")
            return 1

        if profile:
            pack_list = selection.profiles.get(profile, [])
            mode = {"mode": "profile", "profile": profile}
        elif packs:
            pack_list = packs
            mode = {"mode": "pack", "packs": pack_list}
        else:
            pack_list = [p["name"] for p in selection.packs]
            mode = {"mode": "all", "packs": pack_list}

        # Copy rules from packs into staging area
        state_dir = project_root / TARGET_INTERNAL_STATE_DIR
        rules_root = state_dir / "project_rules"
        if rules_root.exists():
            shutil.rmtree(rules_root)
        rules_root.mkdir(parents=True, exist_ok=True)
        for pack_name in pack_list:
            pack_rules = state_dir / "packs" / pack_name / "rules"
            self._copy_tree_non_destructive(pack_rules, rules_root, project_root)

        # Copy memory/tool starters
        file_manifest = self._load_file_manifest(project_root)
        for pack_name in pack_list:
            pack_dir = state_dir / "packs" / pack_name
            starters = [
                ("memory_starters", TARGET_MEMORY_BANK_DIR),
                ("tool_starters", TARGET_TOOLS_DIR),
            ]
            for starter_subdir, target in starters:
                created = self._copy_tree_non_destructive(
                    pack_dir / starter_subdir, project_root / target, project_root
                )
                for rel in created:
                    file_manifest[rel] = pack_name
        self._save_file_manifest(project_root, file_manifest)

        # Generate rules for assistants
        names_to_sync = assistants or [a.name for a in SUPPORTED_ASSISTANTS]
        for name in names_to_sync:
            spec = ASSISTANT_MAP.get(name)
            if not spec:
                continue
            path_to_clean = project_root / spec.clean_path
            if path_to_clean.is_dir():
                shutil.rmtree(path_to_clean)
            elif path_to_clean.is_file():
                path_to_clean.unlink()
            self._generate_for_assistant(spec, rules_root, project_root)

        # Update sync status
        status = self._load_sync_status(project_root)
        timestamp = datetime.now(timezone.utc).isoformat()
        for name in names_to_sync:
            status[name] = {"timestamp": timestamp, **mode, "packs": pack_list, "pack_count": len(pack_list)}
        self._save_sync_status(project_root, status)

        print("Sync complete.")
        return 0

    def project_status(self, project_dir: Optional[str] = None) -> int:
        project_root = Path(project_dir).absolute() if project_dir else self.project_root
        status = self._load_sync_status(project_root)
        if not status:
            print("No sync status found.")
            return 0
        print("Project Sync Status:")
        for assistant, info in status.items():
            ts = info.get("timestamp", "unknown")
            mode = info.get("mode", "all")
            line = f"  - {assistant}: {ts} ({mode})"
            if mode == "profile":
                line += f" profile={info.get('profile')}"
            elif mode == "pack":
                line += f" packs={len(info.get('packs', []))}"
            else:
                line += f" packs={len(info.get('packs', []))}"
            print(line)
        return 0

    def project_clean_rules(self, project_dir: Optional[str] = None) -> int:
        project_root = Path(project_dir).absolute() if project_dir else self.project_root
        # remove generated assistant rules
        for spec in SUPPORTED_ASSISTANTS:
            path = project_root / spec.clean_path
            if path.is_file():
                path.unlink()
                parent = path.parent
                if parent != project_root and not any(parent.iterdir()):
                    parent.rmdir()
            elif path.is_dir():
                shutil.rmtree(path)
        # remove internal state dir
        state_dir = project_root / TARGET_INTERNAL_STATE_DIR
        if state_dir.exists():
            shutil.rmtree(state_dir)
            print(f"- Removed: {state_dir}")
        return 0

    def project_clean(self, project_dir: Optional[str] = None) -> int:
        project_root = Path(project_dir).absolute() if project_dir else self.project_root
        self.project_clean_rules(str(project_root))
        for name in [TARGET_MEMORY_BANK_DIR, TARGET_TOOLS_DIR]:
            path = project_root / name
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)
        return 0

    def project_clean_context(
        self,
        project_dir: Optional[str] = None,
        action: Optional[str] = None,
        force: bool = False,
    ) -> int:
        project_root = Path(project_dir).absolute() if project_dir else self.project_root
        selection = self._load_selection(project_root)
        installed = {p["name"] for p in selection.packs}
        manifest = self._load_file_manifest(project_root)
        orphans = {p: pack for p, pack in manifest.items() if pack not in installed}
        if not orphans:
            print("No orphaned context files found.")
            return 0

        if not force:
            print("Orphaned context files:")
            for rel in orphans:
                print(f"  - {rel}")
            if not action:
                resp = input("Delete these files? [y/N]: ").strip().lower()
                action = "delete" if resp == "y" else "keep"
            else:
                resp = input(f"Proceed to {action} these files? [y/N]: ").strip().lower()
                if resp != "y":
                    print("Cleanup cancelled by user.")
                    return 0
        else:
            if not action:
                action = "keep"

        for rel in list(orphans.keys()):
            full_path = project_root / rel
            if action == "delete" and full_path.exists():
                if full_path.is_file():
                    full_path.unlink()
                    parent = full_path.parent
                    roots = {
                        project_root / TARGET_MEMORY_BANK_DIR,
                        project_root / TARGET_TOOLS_DIR,
                        project_root,
                    }
                    while parent not in roots and not any(parent.iterdir()):
                        parent.rmdir()
                        parent = parent.parent
                elif full_path.is_dir():
                    shutil.rmtree(full_path)
            manifest.pop(rel, None)

        self._save_file_manifest(project_root, manifest)
        print("Context cleanup complete.")
        return 0

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def report_bug(self) -> int:
        print(f"To report a bug, please visit {BUG_REPORT_URL}")
        try:  # pragma: no cover - best effort
            webbrowser.open(BUG_REPORT_URL)
        except Exception:
            pass
        return 0

    def rate_ruleset(self) -> int:
        print(f"For ratings and reviews, please visit {RATINGS_REVIEWS_URL}")
        try:  # pragma: no cover
            webbrowser.open(RATINGS_REVIEWS_URL)
        except Exception:
            pass
        return 0

