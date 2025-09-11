#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from rulebook_ai.community_packs import validate_pack_structure


def validate_entry(entry):
    slug = f"{entry['username']}/{entry['repo']}"
    clone_url = f"https://github.com/{slug}.git"
    commit = entry.get("commit")
    path = entry.get("path", "")
    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.run(["git", "clone", clone_url, tmpdir], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if commit:
            subprocess.run(["git", "-C", tmpdir, "checkout", commit], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pack_path = Path(tmpdir) / path
        validate_pack_structure(pack_path, expected_name=entry["name"])


def main():
    with open("packs.json") as f:
        index = json.load(f)
    errors = []
    for entry in index.get("packs", []):
        try:
            validate_entry(entry)
        except Exception as e:
            errors.append(f"{entry.get('name', '?')}: {e}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
