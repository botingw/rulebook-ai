# Technical Specifications Document

## Target Platforms:
Cursor, CLINE, RooCode, Windsurf.

## Rule File Formats:
- `.mdc` (Cursor) - See `docs/literature/custom_rules_setup_cursor.md`
- `.clinerules` (CLINE) - See `docs/literature/custom_rules_setup_cline.md`
- `.roo/rules/` (RooCode - Workspace-wide) - See `docs/literature/custom_rules_setup_roo_code.md`
- `.roo/rules-{modeSlug}/` (RooCode - Mode-specific) - See `docs/literature/custom_rules_setup_roo_code.md`
- `.windsurfrules` (Windsurf) - See `docs/literature/custom_rules_setup_windsurf.md`

## Memory File Formats:
- `.md` (Core Docs)
- `.mdc` (Error/Lessons Learned)
- `.tex` (Optional Context - Literature/RFCs)

## Known Technical Issues:
1.  **Inconsistent Documentation:** The `README.md` had inconsistencies regarding CLINE/RooCode rule loading (now partially addressed).
2.  **CLINE Manual Rule Loading:** CLINE requires manual copy-pasting of mode-specific rules into settings due to lack of native support.
3.  **CLINE UI Bug:** A known UI bug in Cline can cause custom instructions pasted for one mode (e.g., Plan) to overwrite the instructions for another mode (e.g., Act), making the manual copy-paste workaround unreliable.
