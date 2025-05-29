# VS Code Extension: Testing and Publishing Guide

This guide provides instructions on how to test and publish the VS Code extension for managing AI assistant rules.

## 1. Local Testing and Debugging

VS Code provides a dedicated environment for running and debugging extensions locally without publishing them.

### 1.1 Running the Extension

1.  Open the extension project folder in VS Code.
2.  Go to the Run and Debug view (Ctrl+Shift+D or Cmd+Shift+D).
3.  Select the "Run Extension" configuration from the dropdown.
4.  Click the green play button or press F5.

This will open a new VS Code window called the "Extension Development Host". This window runs a standard VS Code instance with your extension loaded and active. You can now test your extension's features as a user would experience them.

Any `console.log` statements in your extension code will appear in the Debug Console of the original VS Code window (the one where you pressed F5).

### 1.2 Debugging the Extension

While the Extension Development Host window is open:

1.  Set breakpoints in your extension's TypeScript/JavaScript code by clicking in the gutter next to the line numbers.
2.  Interact with your extension in the Extension Development Host window (e.g., trigger a command).
3.  Execution will pause at your breakpoints, allowing you to inspect variables, step through code, and understand the flow.
4.  Use the Debug Console to evaluate expressions and check the state of your variables.

### 1.3 Testing Commands

Test the commands you've implemented by:

*   Opening the Command Palette (Ctrl+Shift+P or Cmd+Shift+P) and searching for your extension's commands (e.g., "Manage Rules: Install", "Manage Rules: Sync").
*   If you've implemented a GUI (like a sidebar view), interact with the buttons and input fields in that view.

### 1.4 Testing File System Interactions

When testing commands that interact with the file system (`install`, `sync`, `clean-rules`, `clean-all`), use a temporary or test project folder as the `target_repo_path` in the Extension Development Host window. **Avoid running these commands on critical projects during local development unless you are certain of their safety.**

## 2. Automated Testing

VS Code has a test framework for extensions, allowing you to write and run automated tests.

1.  Tests are typically written in TypeScript/JavaScript and are located in a `src/test` directory.
2.  The test suite runs your extension in a special instance of VS Code and executes test cases.
3.  To run tests:
    *   Go to the Run and Debug view.
    *   Select the "Extension Tests" configuration.
    *   Click the green play button or press F5.
4.  Test results will appear in the Debug Console.

Write tests for:
*   Command registration and execution.
*   Interactions with the VS Code API (e.g., showing messages, accessing workspace files).
*   Parsing of configuration settings.
*   (Potentially) Interactions with the `manage_rules.py` script (though you might mock file system operations or the script execution itself in unit tests).

## 3. Publishing the Extension

Once your extension is tested and ready, you can package and publish it to the VS Code Marketplace.

### 3.1 Prerequisites

*   Install `vsce` (Visual Studio Code Extension manager), the command-line tool for packaging and publishing extensions:
```
bash
    npm install -g vsce
    
```
*   Get a Personal Access Token (PAT) from Azure DevOps with permission to "Acquire" and "Manage" extensions. See the official VS Code documentation for detailed steps on obtaining a PAT.

### 3.2 Packaging the Extension

1.  Navigate to your extension project directory in the terminal.
2.  Run the `vsce package` command:
```
bash
    vsce package
    
```
3.  This command creates a `.vsix` file (your packaged extension) in your project root.

### 3.3 Publishing the Extension

1.  Run the `vsce publish` command:
```
bash
    vsce publish
    
```
2.  If this is your first time publishing this extension, you will likely be prompted to log in using your Azure DevOps PAT.
```
bash
    vsce publish -p <your_personal_access_token>
    
```
3.  Subsequent publishes can often be done without the `-p` flag if your login details are saved.
4.  `vsce` will increment the version number in your `package.json`, upload the `.vsix` file, and publish it to the Marketplace.

### 3.4 Updating the Extension

To publish an update:

1.  Make your code changes.
2.  Update the `version` in your `package.json` according to semantic versioning (e.g., `vsce publish` will increment the patch version by default).
3.  Run `vsce publish` again.

Your updated extension will be available on the Marketplace, and users with the extension installed will receive the update automatically (or be prompted to update, depending on their settings).

---

**References:**

*   [VS Code Extension Development documentation](https://code.visualstudio.com/api)
*   [Testing Extensions](https://code.visualstudio.com/api/working-with-extensions/testing-extension)
*   [Publishing Extensions](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)
*   [vsce command-line tool](https://github.com/microsoft/vsce)