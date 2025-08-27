# Manage Rules VS Code Extension – Design Spec (v0.0.1‑alpha)

> **Goal:** provide a minimal GUI wrapper for `manage_rules.py` so users can run core commands inside VS Code without ever leaving the editor.  This 0.0.1‑alpha release assumes exactly **one open folder** (the workspace root) and executes every command in an Integrated Terminal to keep logs wide and support interactive prompts.

---

## 1 • Objectives

|  ID   | Objective                                                                | MVP Decision                                                              |
| ----- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------- |
|  O‑1  | Enable common tasks (install, sync, clean‑rules, clean‑all, list‑rules). | Provide sidebar shortcuts.                                                |
|  O‑2  | Support any new backend command rapidly.                                 | Include **Run Custom CLI…** entry so users can type arguments themselves. |
|  O‑3  | Handle interactive prompts (`y/n`, etc.).                                | Always launch Python inside VS Code **Integrated Terminal**.              |
|  O‑4  | Keep UI surface tiny.                                                    | Logs stay in terminal; sidebar shows only six static items.               |
|  O‑5  | Avoid multi‑root complexity.                                             | Only the first workspace folder is used; quit if none.                    |

---

## 2 • Extension Layout

```
manage-rules-vscode/
├─ src/
│   ├─ extension.ts         # activation & command registration
│   ├─ utils.ts             # helpers (confirm, openTerm, getRuleSets)
│   └─ sidebarProvider.ts   # static TreeView (6 items)
├─ package.json             # contributes: commands, view
├─ README.md                # usage & limitations (auto‑generated later)
└─ icon.png                 # activity‑bar icon (optional)
```

### 2.1 Main files

| File                   | Responsibility                                                                                                      |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **extension.ts**       | • Determine `root` folder.<br>• Register six commands.<br>• Wire sidebar provider.                                  |
| **utils.ts**           | • `confirmModal(message)`<br>• `openTerminalAndRun(cmd, cwd)`<br>• `getRuleSets(root)` – synchronous parsing helper |
| **sidebarProvider.ts** | Returns six static `TreeItem`s that trigger commands.                                                               |

---

## 3 • Command Reference & Flow

| Command              | UI Path                     | Flow (happy path)                                                                                                                      |
| -------------------- | --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Install Rule Set** | Sidebar → *Install*         | 1) `getRuleSets(root)` → QuickPick.<br>2) Confirm modal.<br>3) `openTerm("python3 manage_rules.py install . --rule-set <name>", root)` |
| **Sync Rule Set**    | Sidebar → *Sync*            | Confirm → `openTerm("python3 manage_rules.py sync .", root)`                                                                           |
| **Clean Rules**      | Sidebar → *Clean Rules*     | Warn → `openTerm("python3 manage_rules.py clean-rules .", root)`                                                                       |
| **Clean All**        | Sidebar → *Clean All*       | Big warn → `openTerm("python3 manage_rules.py clean-all .", root)`                                                                     |
| **List Rules**       | Sidebar → *List Available*  | `getRuleSets(root)` → `window.showInformationMessage`                                                                                  |
| **Run Custom CLI…**  | Sidebar → *Run Custom CLI…* | InputBox → `openTerm("python3 manage_rules.py " + args, root)`                                                                         |

> **All terminals** are created with `{ name: "Manage Rules", cwd: root }` and shown immediately. Logs + interactive prompts appear there.

---

## 4 • `getRuleSets()` Parsing Logic

```ts
export function getRuleSets(root: string): string[] {
  const out = spawnSync("python3", ["manage_rules.py", "list-rules"], {
    cwd: root,
    encoding: "utf8"
  });
  if (out.status !== 0) throw new Error(out.stderr);

  const names: string[] = [];
  let inBlock = false;
  for (const line of out.stdout.split(/\r?\n/)) {
    if (/Available rule sets:/i.test(line)) { inBlock = true; continue; }
    if (/---\s*Listing complete/.test(line)) break;
    const m = line.match(/^\s*-\s*([A-Za-z0-9_\-]+)/);
    if (inBlock && m) names.push(m[1]);
  }
  if (!names.length) throw new Error("No rule names parsed");
  return names;
}
```

*Works on sample output:*  `heavy-spec`, `light-spec`, `medium-spec`, `no_memory_interation_rules`, `tool_starters`.

---

## 5 • UI Mock‑ups (ASCII)

### 5.1 Activity Bar & Sidebar

```
[◆] Manage Rules  ← icon
  • Install Rule Set
  • Sync Rule Set
  • Clean Rules
  • Clean All
  • List Available Rule Sets
  • Run Custom CLI…
```

### 5.2 Example Terminal Session (Install)

```
▶ python3 manage_rules.py install . --rule-set light-spec
Copying rule set 'light-spec' …
✔ Done in 2.4 s
```

---

## 6 • Settings (JSON)

```jsonc
{
  "manageRules.pythonPath": "python3"   // override if necessary
}
```

Multi‑root support and script path customization **deferred** to a future tag.

---

## 7 • Assumptions & Limitations

1. **Single workspace root** – only `workspaceFolders[0]` is used.  Users must open the target folder itself.
2. **`manage_rules.py` present in ROOT** – extension calls it directly from the root; else `Run Custom CLI…` can pass a path.
3. **Standard `list-rules` format** – relies on the header/footer pattern shown above.
4. **No Webview, no OutputChannel** – all logs in Integrated Terminal.
5. **No background validation** – script errors are displayed raw in the terminal.

---

## 8 • Future Ideas (post‑0.0.1)

1. Multi‑root picker.
2. Webview with richer progress & file previews.
3. Automatic `.gitignore` updates after install.
4. Setting: custom path to `manage_rules.py`.
5. Telemetry (opt‑in) to record failures/success for UX tuning.

---

## 9 • Architecture

### Overview

1. **VS Code Host (Node 18 LTS)** – loads the extension bundle and exposes the `vscode` API.
2. **Extension Entry – `extension.ts`** – detects workspace root, registers commands, delegates UI events, and spawns Integrated Terminals for Python commands.
3. **Sidebar Provider – `sidebarProvider.ts`** – supplies a static TreeView with six leaf actions that raise the relevant commands.
4. **Utilities – `utils.ts`** – houses synchronous rule‑set parsing (`getRuleSets`), modal confirmation helpers, and the `openTerminalAndRun` helper.
5. **Integrated Terminal** – runs `python3 manage_rules.py …` inside the workspace root, capturing wide logs and interactive prompts.
6. **Backend Script – `manage_rules.py`** – performs install/sync/clean file operations and emits stdout used by the extension (e.g., for rule listing).

### Component Workflows

Below are step‑by‑step call flows illustrating **how each TypeScript module interacts** during a typical command execution.

#### 9.1 `sidebarProvider.ts`

```
[User click TreeItem] ─▶ vscode executes associated command ID
```

*Static mapping—no logic beyond emitting the command.*

#### 9.2 `extension.ts`

```
(command handler)                        
  │
  ├─ (1) Reads `root = workspaceFolders[0]`            
  │
  ├─ (2) If command == Install:
  │       ├─ calls utils.getRuleSets(root)
  │       ├─ awaits vscode.window.showQuickPick(ruleNames)
  │       ├─ awaits utils.confirmModal()
  │       └─ utils.openTerminalAndRun("python3 manage_rules.py install . --rule-set <name>", root)
  │
  ├─ (3) If command == Sync / Clean / ... – similar pattern (skip rule list)
  │
  └─ returns immediately (terminal continues independently)
```

#### 9.3 `utils.getRuleSets()`

```
spawnSync("python3 manage_rules.py list-rules", cwd=root)
  │
  ├─ parse stdout (regex on "- <name>")
  └─ return string[] of names (or throw)
```

#### 9.4 `utils.openTerminalAndRun()`

```
createTerminal({ name:"Manage Rules", cwd })
  │
  ├─ term.show()
  └─ term.sendText(<command>)   ← interactive session begins
```

*The Node process hosting the extension does **not** await completion; user can close/re‑run freely.*

#### 9.5 Integrated Terminal ↔ `manage_rules.py`

```
python3 manage_rules.py <subcommand>
  │
  ├─ prompts (y/n) → user input
  ├─ performs filesystem operations under cwd
  └─ writes progress / errors to stdout/stderr
```

### Sequence Example – *Clean All*

```
User clicks "Clean All" ▶ command registered in extension.ts
  └─ utils.confirmModal("delete EVERYTHING?") ✔
        └─ utils.openTerminalAndRun("python3 manage_rules.py clean-all .", root)
              └─ Integrated Terminal shows prompt ▶ user types "y"
                    └─ manage_rules.py deletes directories, prints summary
```

---

### 9.6 Component Relationship Map

The table and diagram below clarify **how each module depends on, or calls, the others** at runtime.

| Caller →                              | Called ↴                                                    | Purpose                                                         | Sync/Async                              |
| ------------------------------------- | ----------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------- |
| `sidebarProvider.ts` (TreeItem click) | VS Code `commands.executeCommand`                           | Dispatches the command ID linked to the clicked item.           | **Sync** – immediate return             |
| `extension.ts` (command handler)      | `utils.getRuleSets`                                         | Retrieve rule names when needed.                                | **Sync** – uses `spawnSync`             |
| `extension.ts`                        | VS Code window APIs – `showQuickPick`, `showWarningMessage` | Gathers user input / confirmations.                             | **Async** (Promise)                     |
| `extension.ts`                        | `utils.openTerminalAndRun`                                  | Spawns terminal & sends Python command.                         | **Sync** (fire‑and‑forget)              |
| `utils.openTerminalAndRun`            | VS Code `window.createTerminal`                             | Creates & shows terminal.                                       | **Sync**                                |
| Integrated Terminal                   | `manage_rules.py` (Python)                                  | Executes business logic; interacts with user for extra prompts. | **Runtime** – outside extension process |
| `manage_rules.py`                     | Filesystem under workspace root                             | Reads/writes rule folders, memory, tools.                       | OS‑level sync                           |

