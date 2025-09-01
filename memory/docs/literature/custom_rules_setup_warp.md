# Warp Rules

**Source:** https://docs.warp.dev/knowledge-and-collaboration/rules

Warp’s Rules feature lets you create reusable guidelines that inform how Warp’s agents respond to your prompts. Rules help tailor responses to match coding standards, project conventions and personal preferences, making AI interactions smarter and more consistent.

---

### Rule Types

Warp supports two kinds of rules:

-   **Global Rules** – Apply across all projects and contexts. They’re ideal for coding standards, workspace-wide guidelines, and tool configurations you want applied everywhere.
-   **Project-Scoped Rules** – Live in your codebase and apply automatically when working within that project. They are stored in a `WARP.md` file located in the root of your repository or in a subdirectory for more targeted guidance. Warp automatically applies the root `WARP.md` and the `WARP.md` in the current directory; it makes a best-effort attempt to include rules from other subdirectories when you edit files there.

---

### Example Project Structure

```
project/
  api/
    WARP.md      # API-specific rules
  ui/
    WARP.md      # UI-specific rules
  WARP.md        # Project-wide rules
```