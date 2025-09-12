import shutil
from pathlib import Path

def main() -> int:
    """
    Syncs the canonical spec documents into the pack-authoring-guide pack.
    """
    # This script is in src/rulebook_ai/scripts, so project root is 3 levels up.
    project_root = Path(__file__).resolve().parent.parent.parent.parent
    print(f"Project root detected as: {project_root}")

    dest_dir = project_root / "src" / "rulebook_ai" / "packs" / "pack-authoring-guide" / "memory_starters" / "docs"
    if not dest_dir.is_dir():
        print(f"Error: Destination directory not found at {dest_dir}")
        return 1

    print(f"Syncing documents to {dest_dir.relative_to(project_root)}...")

    sources = {
        "pack_structure_spec.md": project_root / "memory/docs/features/manage_rules/pack_structure_spec.md",
        "platform_rules_spec.md": project_root / "memory/docs/features/manage_rules/platform_rules_spec.md",
        "pack_developer_guide.md": project_root / "memory/docs/features/community_packs/pack_developer_guide.md",
        "community_packs_spec.md": project_root / "memory/docs/features/community_packs/spec.md",
    }

    copied_count = 0
    for dest_name, src_path in sources.items():
        dest_path = dest_dir / dest_name
        if not src_path.is_file():
            print(f"  - WARNING: Source file not found, skipping: {src_path}")
            continue
        
        print(f"  - Copying: {src_path.relative_to(project_root)}")
        shutil.copy(src_path, dest_path)
        copied_count += 1

    print(f"\nSync complete. Copied {copied_count} files.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
