# Specification: Pack Structure

**1. Purpose**

Defines the required directory layout and naming rules for Rulebook-AI packs. Mapping from these source files to assistant-specific outputs is described in `platform_rules_spec.md`. For step-by-step examples, consult `../community_packs/pack_developer_guide.md`, but this specification remains the source of truth. Community contributions described in `../community_packs/spec.md` must follow this spec to avoid failures during `packs add`, `packs sync`, or `project sync`.

**2. Design Goals**

- Provide a universal, verifiable source of project-level rules across all supported assistants.
- Use zero-padded numeric prefixes to guarantee deterministic ordering regardless of filesystem or assistant behavior.
- Keep the structure minimal yet extensible so tooling can automate validation and future features while enabling future assistant mappings.

A pack is considered well-designed when it can be processed by `packs add`, `packs sync`, and `project sync` without errors, presents a clear deterministic rule sequence, and remains readable for both humans and tooling.

**3. Required Root Contents**

A valid pack **must** contain:

- `manifest.yaml` – metadata for the pack.
- `README.md` – human‑readable description.
- `rules/` – universal source directory for rule files.

Optional: `memory_starters/` and `tool_starters/` for starter files.
No other files or directories are permitted at the root unless explicitly allowed by future revisions of this spec.

**4. `manifest.yaml` Requirements**

`manifest.yaml` must include the following fields:

- `name` (string) – globally unique pack identifier. The value **must** be a slug consisting only of letters, digits, and dashes: `^[A-Za-z0-9-]+$`.
- `version` (string) – preferably Semantic Versioning.
- `summary` (string) – one‑sentence description.

Packs lacking these fields are invalid and rejected by the CLI.

**5. Rules Directory Specification**

The `rules/` directory drives rule generation for all assistants and **may only contain directories** named with numeric prefixes:

  - At least one numbered rules directory must be present. If a generic directory without `{mode}` is used, it MUST be named `01-rules` so general rules load before mode-specific ones.
  - Each direct child of `rules/` **must** be a directory named `NN-rules` or `NN-rules-{mode}`, where `NN` is a zero‑padded number (at least two digits).
  - When `{mode}` is present, it must match a supported mode for the target assistant (see `platform_rules_spec.md`). For assistants like Roo Code and Kilo Code, use directories such as `01-rules`, `02-rules-code`, and `03-rules-debug`.
  - Files are not allowed directly under `rules/`; each rules directory must contain at least one rule file, and each file must also use a zero‑padded prefix: `NN-<description>.md` (e.g., `05-directory-structure.md`).
  - Numeric prefixes for directories and files **must be unique** within their respective parent directories.
  - Tooling sorts rule files lexicographically; prefixes guarantee deterministic order for assistants that flatten or concatenate files. Missing or duplicate prefixes are treated as errors by CLI validation.

**6. Encoding and Visibility**

- All rule files must be UTF‑8 encoded text.
- Directory and file names must not begin with `.`; hidden files are ignored by `project sync`.
- Rule files **must** use the `.md` extension and contain at least one rule per file.

**7. CLI Behavior**

- `packs add` and `packs sync` validate the presence of required root items, manifest fields, and numeric prefixes for directories and files.
- During `project sync`, numeric prefixes are stripped and renamed as needed for target assistants. Files or directories without required prefixes are rejected to avoid undefined ordering.

