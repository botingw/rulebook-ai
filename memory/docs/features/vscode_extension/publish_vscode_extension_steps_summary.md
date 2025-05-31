# VS Code Extension — End-to-End Developer Checklist

*A concise recipe from first-time setup to Marketplace release.*

---

## 1  Environment Setup

| Tool                                   | Why                                            | Install Command                                                                    |
| -------------------------------------- | ---------------------------------------------- | ---------------------------------------------------------------------------------- |
| **nvm**                                | Manage Node versions                           | `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh \| bash` |
| **Node 22 (LTS)**                      | Build toolchain                                | `nvm install 22 && nvm alias default 22`                                           |
| **VS Code**                            | Editor / debugger                              | [https://code.visualstudio.com](https://code.visualstudio.com)                     |
| **code CLI**                           | Open VS Code from terminal & manage extensions | ⌘⇧P → **Shell Command: Install ‘code’ command in PATH**                            |
| **vsce**                               | Package & publish extensions                   | `npm i -g @vscode/vsce`                                                            |
| **yo code / @vscode/create-extension** | Scaffold a starter project                     | `npm init @vscode`                                                                 |

> **Python dependency?**
> If your extension spawns Python scripts, require users to have Python 3 on their `PATH` (or expose a `pythonPath` setting).

---

## 2  Scaffold a New Extension

```bash
mkdir hello-world-ext && cd $_
npm init @vscode             # choose “TypeScript” template
code .                       # open project in VS Code
```

Generated structure:

```
hello-world-ext/
├─ src/extension.ts
├─ out/              (compiled JS)
├─ python/           (place your mytool.py here)
├─ .vscode/launch.json
├─ package.json
└─ tsconfig.json
```

---

## 3  Daily Dev Loop

```bash
# terminal 1 – TypeScript watch compiler
npm run watch               # runs `tsc -w -p ./`

# terminal 2 (or within VS Code)
code .                      # open workspace
F5                          # Run Extension → launches “Extension Development Host”
```

* **Modify code → save** ▶ `tsc --watch` recompiles to `out/`
* Dev-Host auto-reloads; breakpoints hit immediately.

---

## 4  Accessing Bundled Assets

```ts
// extension.ts
import * as path from 'path';
export function activate(ctx) {
  const script = ctx.asAbsolutePath(path.join('python', 'mytool.py'));
  // spawn('python', [script, 'arg1']);
}
```

`context.asAbsolutePath` works both during F5 **and** after publishing.

---

## 5  Manifest Essentials (`package.json`)

```jsonc
{
  "name": "hello-world-ext",
  "displayName": "Hello World Ext",
  "publisher": "your-publisher",
  "description": "Lists AI rule sets and more.",
  "version": "0.0.1",
  "engines": { "vscode": "^1.100.0" },
  "icon": "images/icon.png",
  "categories": ["Other"],
  "activationEvents": ["*"],
  "main": "./out/extension.js",
  "repository": { "type": "git", "url": "https://github.com/you/hello-world-ext.git" },
  "license": "MIT",
  "contributes": {
    "commands": [
      { "command": "aiRuleManager.listRuleSets", "title": "AI Rule Manager: List Available Rule Sets" }
    ],
    "configuration": {
      "properties": {
        "aiRuleManager.pythonPath": {
          "type": "string",
          "default": "python",
          "description": "Path to Python interpreter."
        }
      }
    }
  },
  "scripts": {
    "watch":   "tsc -w -p ./",
    "compile": "tsc -p ./",
    "package": "npm run compile && vsce package",
    "publish": "npm run compile && vsce publish"
  },
  "files": ["out/**", "python/**", "images/**", "README.md", "LICENSE"]
}
```

---

## 6  Write & Polish README.md

* **Cover**: What the extension does, install steps, command palette usage, configuration, screenshots/GIFs.
* `vsce` blocks packaging if default template text remains.

---

## 7  Package & Local Smoke Test

```bash
npm run package                              # ⇒ hello-world-ext-0.0.1.vsix
code --install-extension hello-world-ext-0.0.1.vsix
code --disable-extensions                    # launch VS Code with only built-ins
# ↳ Run your command palette entry, verify Python script executes.
code --uninstall-extension your-publisher.hello-world-ext
```

---

## 8  Publish to Marketplace
instruction: https://code.visualstudio.com/api/working-with-extensions/publishing-extension

```bash
vsce login your-publisher     # one-time PAT auth
npm run publish               # bumps version + uploads
```

Listing appears at
`https://marketplace.visualstudio.com/items?itemName=your-publisher.hello-world-ext`

---

## 9  Maintain & Iterate

```bash
git commit -am "Add new feature"
npm version patch             # 0.0.1 → 0.0.2
npm run publish               # uploads new .vsix
```

Users receive an update prompt automatically.

---

### Quick Uninstall / Cleanup

```bash
code --uninstall-extension your-publisher.hello-world-ext
# Or from GUI: Extensions pane › ⚙️ › Uninstall
```

Happy extension hacking! 🚀
