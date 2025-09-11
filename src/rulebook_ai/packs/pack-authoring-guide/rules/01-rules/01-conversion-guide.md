## Conversion Guide

When assisting a contributor to create a Rulebook-AI pack:

1. Review `pack_structure_spec.md` and `platform_rules_spec.md` in memory to confirm required directories and mode names.
2. Ask the user for their existing rule or document layout.
3. Instruct them to create `manifest.yaml`, `README.md`, and a `rules/` folder at the pack root.
4. Ensure `rules/` contains zero-padded subdirectories. General rules must be in `01-rules`; mode-specific rules use names like `02-rules-code`.
5. For each subdirectory, require at least one `NN-description.md` rule file using UTF-8 encoding and visible filenames.
6. If the user needs examples or guidance, point them to `pack_developer_guide.md` and `contribution_workflow.md` in memory.
7. Remind them optional docs or tools can be placed under `memory_starters/` or `tool_starters/` for AI reference.
   - Example rule for docs: "Consult `memory/pack_structure_spec.md` for structure requirements."
   - Example rule for tools: "Run `python tools/validate_pack.py <pack_path>` to check the pack." 
