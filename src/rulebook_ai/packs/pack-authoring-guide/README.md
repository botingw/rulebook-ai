# Pack Authoring Guide

This built-in pack assists contributors in converting existing rules or documentation into a Rulebook-AI pack that conforms to the [pack_structure_spec.md](../../../../memory/docs/features/manage_rules/pack_structure_spec.md) and maps to assistant-specific outputs described in [platform_rules_spec.md](../../../../memory/docs/features/manage_rules/platform_rules_spec.md).

It provides:

- A step-by-step conversion guide.
- A validation checklist reminding you to run `rulebook-ai packs add <path>` before publishing.
- Copies of `pack_structure_spec.md`, `pack_developer_guide.md`, and `platform_rules_spec.md` for offline reference.

## Usage

1. Review the rules in `rules/01-rules/`.
2. Consult the docs inside `memory_starters/docs/`—`pack_structure_spec.md`, `pack_developer_guide.md`, and `platform_rules_spec.md`—when structuring your pack.
3. Use the script in `tool_starters/validate_pack.py` or the CLI command:
   ```
   rulebook-ai packs add <path-to-your-pack>
   ```
   to verify your pack before submitting to the community index.
