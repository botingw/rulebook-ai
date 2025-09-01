**Source:** https://kilocode.ai/docs/advanced-usage/custom-rules

Kilo Code’s custom rules feature lets you define project-specific or global guidelines that the AI agent will follow whenever it interacts with your code base. These rules act as guardrails for formatting, security and coding standards, ensuring consistent behaviour across projects or on a per-project basis.

---

### Overview

-   **Purpose** – Rules allow you to enforce coding standards, restrict access to sensitive files, and tailor the AI’s behaviour to your project’s needs. The structured nature of Markdown helps the model parse your rules effectively.
-   **Types** – Kilo Code supports two kinds of rules:
    -   **Project Rules:** apply only to the current workspace.
    -   **Global Rules:** apply across all projects and workspaces.

---

### Rule Location

#### Project Rules

Project-specific rules should be placed in the `.kilocode/rules/` directory of your repository. Each rule can be its own file (e.g. `formatting.md`, `restricted_files.md`) and is written in Markdown. Kilo Code also supports a legacy single-file fallback (`.roorules`, `.clinerules`, `.kilocoderules`) for backward compatibility.

#### Global Rules

Global rules live in a `~/.kilocode/rules/` directory in your home folder. Files placed here apply to every project you open in Kilo Code, making it easy to enforce personal or team-wide conventions.

#### Mode-Specific Rules

You can also define rules that only apply to a particular mode. Kilo Code checks for a `.kilocode/rules-<mode>/` directory first; if it doesn’t exist or is empty, it falls back to a `.kilocoderules-<mode>` file. Mode-specific rules override general project or global rules when both are present.

---

### Rule Loading Order

When multiple rules exist, they are loaded in this priority order:

1.  Global rules (`~/.kilocode/rules/`)
2.  Project rules (`.kilocode/rules/` in your repository)
3.  Legacy fallback files (`.roorules`, `.clinerules`, `.kilocoderules`)

For mode-specific rules, Kilo Code first reads the `.kilocode/rules-<mode>/` directory, then falls back to `.kilocoderules-<mode>` if necessary. Project rules take precedence over global rules when both define the same directive.

---

### Creating Custom Rules

You can create rules either through the built-in UI or manually in the file system:

-   **UI Approach** – Open the rules management interface from the Kilo Code panel to view active rules, toggle them on/off, or create new ones.
-   **File Approach** – Manually create the `.kilocode/rules/` directory (for project rules) or `~/.kilocode/rules/` (for global rules) and add Markdown files containing your guidelines. The files are automatically loaded on save.

---

### Example Rules

-   **Table Formatting** – Instruct the AI to append an exclamation mark to every table column header.
-   **Restricted File Access** – List sensitive files (e.g. `.env` or `credentials.json`) that must not be read.

---

### Best Practices

-   **Be Specific** – Clearly define the scope and intent of each rule.
-   **Organize Using Categories** – Use headers and separate files to group related rules.
-   **Include Examples** – Provide example behaviour to clarify expectations.
-   **Keep It Simple** – Concise, easy-to-understand rules are more likely to be followed.
-   **Update Regularly** – Revise rules as your project evolves.
