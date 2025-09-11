# Contributing

Thank you for helping grow the Rulebook AI community index!

## Adding a Pack

1. Ensure your pack repository follows the [pack developer guide](../memory/docs/features/community_packs/pack_developer_guide.md).
2. Edit `packs.json` and add an entry with:
   - `name`: globally unique pack name.
   - `username`: GitHub owner.
   - `repo`: repository name.
   - `path` (optional): path to pack root.
   - `description`: short summary.
   - `commit` (optional): specific commit or tag.
3. Run `python scripts/validate_index.py`.
4. Commit your changes and open a pull request.

## Validation

The CI workflow clones each referenced pack, checks for required files, and verifies the `manifest.yaml` `name` matches the `name` in `packs.json`.
