from pathlib import Path
import sys

from rulebook_ai.community_packs import validate_pack_structure


def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    name, manifest = validate_pack_structure(target)
    print(f"validated pack '{name}' version {manifest['version']}")


if __name__ == "__main__":
    main()
