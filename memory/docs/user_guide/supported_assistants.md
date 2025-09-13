# Supported AI Assistants (Detailed)

This document contains detailed information about the AI coding assistants supported by `rulebook-ai`. It includes where their generated rule files are placed, whether the assistant expects a single file or a directory, and format notes.

Source of truth: `src/rulebook_ai/assistants.py`

| Assistant (display name) | Internal name | Rule path / Notes |
|---|---:|---|
| Cursor | `cursor` | `.cursor/rules` — multi-file directory. Files use the `.mdc` extension. |
| Windsurf | `windsurf` | `.windsurf/rules` — multi-file directory. Files are plain `.md`. Each file has a per-file character limit; see Windsurf docs. |
| Cline | `cline` | `.clinerules` — multi-file directory. The generator removes extensions during creation; supports flexible file layouts. |
| RooCode | `roo` | `.roo` — supports mode-based subdirectories and recursive rule loading. Recommended layout: `.roo/rules/` and `.roo/rules-{modeSlug}/`. |
| Kilo Code | `kilocode` | `.kilocode` — supports modes & subdirectories similar to RooCode. |
| Warp | `warp` | `WARP.md` — single-file rules document at repository root. |
| GitHub Copilot | `copilot` | `.github/copilot-instructions.md` — single-file instructions under `.github/`. |
| Claude Code | `claude-code` | `CLAUDE.md` — single-file rules document at repository root. |
| Codex CLI | `codex-cli` | `AGENTS.md` — single-file rules document at repository root. |
| Gemini CLI | `gemini-cli` | `.gemini/GEMINI.md` — single-file rules document under `.gemini/`. |

Notes and guidance
- To see the authoritative assistant definitions, consult `src/rulebook_ai/assistants.py`. The `SUPPORTED_ASSISTANTS` list is the single source of truth used by the CLI.
- Use `rulebook-ai project sync --assistant <name>` to generate rules for one or more assistants. Example:
  ```
  rulebook-ai project sync --assistant cursor copilot
  ```
- Use `--all` to generate rules for every assistant supported by this release:
  ```
  rulebook-ai project sync --all
  ```
- Keep detailed rule layout and loading behavior in this file so the README remains concise for users who only want a quick overview.
- When adding or removing assistants from the code, update this document and the README accordingly.

Troubleshooting tips
- If generated files are not loaded by an assistant, verify:
  1. The assistant's expected location and filename/extension (see table above).
  2. That the file size / per-file character limits (e.g., Windsurf) haven't been exceeded.
  3. That `.gitignore` or other tooling hasn't accidentally removed generated rules before testing.
