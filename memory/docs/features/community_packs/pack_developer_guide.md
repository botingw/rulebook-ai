# Rulebook-AI Pack Developer Guide

A Rulebook-AI Pack is a self-contained directory that bundles rules, starter files, and metadata. The purpose of this guide is to provide a specification so clear that a developer or an AI assistant can read it and correctly structure a rule pack that is universally compatible with `rulebook-ai`.

### Pack Structure

A valid pack must adhere to the following structure. This example shows a comprehensive layout that correctly targets all supported assistant types.

```
my-awesome-pack/
├── manifest.yaml           # (Required) Metadata for the pack.
├── README.md               # (Required) Description, usage, and philosophy of the pack.
├── rules/                  # (Required) The "universal source" for AI assistant rules.
│   ├── 01-rules/           # Maps to the default 'rules' folder for mode-based assistants.
│   │   ├── 00-meta.md
│   │   └── 01-principles.md
│   ├── 02-rules-architect/ # Maps to the 'rules-architect' folder.
│   │   └── 01-planning.md
│   └── 03-rules-code/      # Maps to the 'rules-code' folder.
│       └── 01-coding.md
├── memory_starters/        # (Optional) Starter files for the user's `memory/` directory.
│   └── docs/
│       └── new-feature-template.md
└── tool_starters/          # (Optional) Starter scripts for the user's `tools/` directory.
    └── my-custom-script.py
```

### `manifest.yaml` (Required)

This file contains essential metadata for the pack.

**Required Fields:**
*   `name` (string): A globally unique, machine-friendly name for the pack (e.g., `my-awesome-pack`).
*   `version` (string): The version of the pack, preferably using Semantic Versioning (e.g., `1.0.0`).
*   `summary` (string): A brief, one-sentence description of the pack's purpose.

The `name` field becomes the installation directory inside `.rulebook-ai/packs/<name>`. To avoid conflicts, choose a name that is not used by built-in packs or other community packs. The CLI aborts installation if an existing pack with the same `name` comes from a different source.

### Directory Specifications

*   **`rules/` (Required)**
    This is the most important directory. Its structure is designed to be a "universal source" that can generate rules for all supported AI assistants. The `sync` command uses a single, consistent logic to process this directory.

    **Flexibility:** You are not required to provide all types of subdirectories. A pack can contain only general rules (e.g., a `01-rules` folder), only mode-specific rules (e.g., `02-rules-code`), or a combination of both. The `sync` command will simply process the directories that it finds, giving you full control over which assistant types your pack is optimized for.

    **How the `sync` Command Interprets This Structure:**

    1.  **For Mode-Based Assistants (e.g., Roo Code, Kilo Code):**
        *   The `sync` command iterates through each subdirectory within the source pack's `rules/` folder (e.g., `01-rules`, `02-rules-architect`).
        *   For each subdirectory, it strips the numeric prefix (e.g., `01-`) to get the target directory name (e.g., `rules` or `rules-architect`).
        *   It then copies the contents of the source subdirectory into the corresponding target directory for the assistant (e.g., from `01-rules/` to `.roo/rules/`, and from `02-rules-architect/` to `.roo/rules-architect/`).

    2.  **For Multi-File, Non-Mode Assistants (e.g., Cline, Cursor):**
        *   The command performs a deep, recursive search to find all rule files within `rules/` and sorts them alphabetically by their full path. This is why numeric prefixes on folders and files are essential.
        *   It then copies the files to the single target directory (e.g., `.cursor/rules/`), renaming each file with a simple, incrementing numeric prefix (`01-`, `02-`, `03-`, etc.) to enforce the final loading order required by the assistant.

    3.  **For Single-File Assistants (e.g., GitHub Copilot, Warp):**
        *   It follows the same file discovery and sorting process as for multi-file assistants.
        *   Instead of copying, it concatenates the content of all files, in the correct sorted order, into a single output file (e.g., `copilot-instructions.md`).

    ### Authoring Considerations: Cross-Assistant Compatibility
    The "universal source" structure is powerful, but it's crucial to understand how your rules will be applied across different types of assistants.

    A key takeaway is that **all rules within the `rules/` directory are applied to non-mode assistants**, regardless of which subdirectory they are in.

    **Consider this scenario:**
    *   You have a general rule in `01-rules/01-principles.md`.
    *   You have a mode-specific rule in `02-rules-code/01-coding-workflow.md`.

    Here is how they will be treated:

    *   **For Roo Code (Mode-Based):**
        *   `01-principles.md` will be applied as a general rule.
        *   `01-coding-workflow.md` will be applied *only* when the "code" mode is active.

    *   **For Cursor (Multi-File, Non-Mode):**
        *   Both `01-principles.md` and `01-coding-workflow.md` will be copied into the `.cursor/rules/` directory and will be active at all times.

    *   **For Gemini (Single-File):**
        *   The content of both `01-principles.md` and `01-coding-workflow.md` will be concatenated into `GEMINI.md` and will be active at all times.

    **Guidance for Pack Authors:**

    *   If you are creating a rule that should *only* apply to a specific mode in an assistant like Roo Code, be aware that it will still be included in the general context for other assistants like Cursor or Gemini.
    *   Design your rules to be as general as possible. If a rule must be strictly limited to a mode, you might need to use phrasing within the rule itself, such as: *"If you are operating in 'code' mode, follow these specific instructions..."* This ensures the rule is safely ignored by assistants that don't have modes.
    *   When converting an existing ruleset, decide which assistants you intend to support. If you only target mode-based assistants, this is less of a concern. If you want universal compatibility, you must review all rules to ensure they don't cause conflicts when flattened into a single context.

    **Best Practices for Pack Authors:**
    *   **Use Numeric Prefixes:** Always use `NN-` prefixes on directories and files within `rules/` to ensure a predictable alphabetical sort order. This is the master control for rule ordering across all assistant types.
    *   **Name Directories for Mapping:** The name of a subdirectory after its prefix (e.g., `rules`, `rules-code`) directly determines the target folder for mode-based assistants. Ensure these match the target assistant's requirements.

*   **`memory_starters/` & `tool_starters/` (Optional)**
    *   These directories contain starter files. When a user runs `project sync`, their contents are copied into the user's project `memory/` and `tools/` directories, respectively. The CLI will **never overwrite** a file that already exists in the user's project.