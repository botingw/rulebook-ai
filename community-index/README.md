# Rulebook AI Community Index

This repository publishes `packs.json`, a curated list of community-maintained rule packs for the `rulebook-ai` CLI.

## Usage

1. Fork this repository.
2. Add your pack to `packs.json` with `name`, `username`, `repo`, optional `path`, `description`, and optional `commit` fields.
3. Run `python scripts/validate_index.py` to verify your entry.
4. Submit a pull request.

The GitHub Actions workflow will automatically validate new entries.
