"""Synchronize canonical project documentation into the authoring pack."""

import argparse
import shutil
from collections.abc import Sequence
from pathlib import Path
from typing import Optional

DESTINATION_RELATIVE = Path("src/rulebook_ai/packs/pack-authoring-guide/memory_starters/docs")
SOURCE_FILES = {
    "pack_structure_spec.md": Path("memory/docs/features/manage_rules/pack_structure_spec.md"),
    "platform_rules_spec.md": Path("memory/docs/features/manage_rules/platform_rules_spec.md"),
    "pack_developer_guide.md": Path("memory/docs/features/community_packs/pack_developer_guide.md"),
    "community_packs_spec.md": Path("memory/docs/features/community_packs/spec.md"),
}


def sync_docs(project_root: Path) -> int:
    """Copy canonical docs from ``project_root`` into the authoring pack."""
    project_root = Path(project_root).expanduser().resolve()
    print(f"Project root detected as: {project_root}")

    dest_dir = project_root / DESTINATION_RELATIVE
    if not dest_dir.is_dir():
        print(f"Error: Destination directory not found at {dest_dir}")
        return 1

    print(f"Syncing documents to {dest_dir.relative_to(project_root)}...")

    sources: dict[str, Path] = {
        dest_name: project_root / source_path for dest_name, source_path in SOURCE_FILES.items()
    }
    missing = [path for path in sources.values() if not path.is_file()]
    if missing:
        print("Error: Required source files not found:")
        for path in missing:
            print(f"  - {path}")
        return 1

    for dest_name, src_path in sources.items():
        dest_path = dest_dir / dest_name
        print(f"  - Copying: {src_path.relative_to(project_root)}")
        shutil.copy2(src_path, dest_path)

    print(f"\nSync complete. Copied {len(sources)} files.")
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run the standalone documentation sync command."""
    parser = argparse.ArgumentParser(
        description="Sync canonical project docs into the pack-authoring-guide pack"
    )
    parser.add_argument(
        "--project-dir",
        "-p",
        type=Path,
        default=Path.cwd(),
        help="Rulebook-AI source checkout to update (default: current directory)",
    )
    args = parser.parse_args(argv)
    return sync_docs(args.project_dir)


if __name__ == "__main__":
    raise SystemExit(main())
