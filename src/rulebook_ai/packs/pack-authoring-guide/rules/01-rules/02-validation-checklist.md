## Validation Checklist

After the contributor assembles their pack:

1. **Verify Root Contents**: Confirm the pack root contains ONLY `manifest.yaml`, `README.md`, `rules/`, and optionally `memory_starters/` or `tool_starters/`. If any other file or directory exists, flag it as a validation failure.
2. Confirm `manifest.yaml` includes `name`, `version`, and `summary` fields.
3. Verify `rules/` contains at least one numbered subdirectory with at least one numbered rule file in each.
4. Check for UTF-8 encoding and reject hidden files or missing zero-padded prefixes.
5. Run `tools/validate_pack.py <path>` to perform local structure validation; alternatively instruct the user to execute `rulebook-ai packs add <path>`.
6. If validation reports errors, return the messages and reference `pack_structure_spec.md` or `platform_rules_spec.md` for fixes.
7. When validation installs the pack locally, remind the user to remove or reinstall it after making changes.
