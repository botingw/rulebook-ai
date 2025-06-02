<!-- Badges -->
![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/YOUR-PUBLISHER.manage-rules-vscode)
![Installs](https://img.shields.io/visual-studio-marketplace/i/YOUR-PUBLISHER.manage-rules-vscode)
![License](https://img.shields.io/github/license/botingw/rulebook-ai)

# 🧩 Manage Rules – Universal **AI Coding Rules** Manager for VS Code

Bring **consistent, context-rich AI assistance** to every repo you touch—across Cursor, GitHub Copilot, CLINE, RooCode & Windsurf—without leaving VS Code.

---

### ✨ Why you’ll love it

- **One-click install** of a curated rule-set & “memory bank” that makes any AI assistant *project-aware*.
- **Works everywhere** your AI does: generates `.cursor/rules`, `.clinerules`, `.windsurf/rules`, Copilot instructions—automatically.  
- **Always in sync**: update rules once, hit **Sync**, done.  
- **Clean exits**: nuke generated files or the whole framework with **Clean Rules / Clean All**.  
- **Zero-config**: Python script is bundled; respects your workspace’s Python path if you want.  
- **Open-source & extensible**: MIT-licensed, backed by the [Rulebook-AI](https://github.com/botingw/rulebook-ai) project.

> “Finally my Cursor and Copilot follow the same playbook.” — Early adopter

---

## 🚀 Quick Start (30 sec)

1. **Open** the project folder in VS Code.  
2. Click the **Manage Rules** icon in the Activity Bar.  
3. Hit **Install Rule Set** → pick `light-spec` (or any set).  
4. Watch the integrated terminal finish; start coding with a smarter AI!

*(Need a different rule later? Use **Sync** after editing `project_rules/`.)*

---

## 📸 Live demo

> **Replace the placeholders below with your assets**

| | |
|:-:|:-:|
| ![Sidebar](media/sidebar.png) | ![Install GIF](media/install.gif) |

---

## 🔍 Commands & Settings

| Command | Palette ID | What it does |
|---------|------------|--------------|
| **Install Framework** | `Manage Rules: Install` | Copy chosen rule set + memory, then run an initial **sync**. |
| **Sync Rules** | `Manage Rules: Sync` | Regenerate platform-specific rule folders. |
| **Clean Rules** | `Manage Rules: Clean Rules` | Delete generated rule folders & `project_rules/`. |
| **Clean All** | `Manage Rules: Clean All` | Full uninstall: rules, memory, tools, env files. |
| **List Rule Sets** | `Manage Rules: List Available Rule Sets` | Peek at available rule-set names. |
| **Run Custom CLI…** | – | Type any `manage_rules.py` args yourself. |

<details>
<summary>Extension settings</summary>

| Setting | Default | Purpose |
|---------|---------|---------|
| `manageRules.pythonPath` | `python3` | Interpreter used to run the backend script. |

</details>

---

## 💡 How it works (under the hood)

The extension is a **thin Node.js wrapper** that triggers the backend `manage_rules.py` script inside VS Code’s Integrated Terminal. Six static commands in a sidebar cover all common workflows; anything else you can run via *Custom CLI*.​ 

---

## 🛣 Road-map

- Multi-root workspace support  
- Webview with progress & file preview  
- Auto-sync on rule edits  
- `.gitignore` helper for generated files  

*(Vote or file new ideas in [Discussions](https://github.com/botingw/rulebook-ai/discussions))*.

---

## 🤝 Need help or have ideas?

- Open an **Issue** in the repo  
- Drop anonymous feedback via our [Google Form](https://docs.google.com/forms/d/e/1FAIpQLSeW57QtPEWIRhHY1iOb8f5KQZTGLSeeb_PN2iZLd0Aw_pVYxw/viewform)  
- Chat with us in the GitHub **Discussions** tab  

---

> © 2025 Bo-Ting Wang · MIT License
