# Context for Task 1.3: Implement a Basic Command

This document provides detailed steps for implementing the first basic command in the VS Code extension, which will execute the `manage_rules.py` script's `list-rules` command and display the output.

## 1. Define the Command in `package.json`

The `package.json` file serves as the extension's manifest. We need to declare our command here so VS Code knows about it.

Open the `package.json` file (located in your extension's root directory) and add a new entry to the `contributes.commands` array.
```
json
"contributes": {
    "commands": [
        {
            "command": "aiRuleManager.listRuleSets",
            "title": "AI Rule Manager: List Available Rule Sets"
        }
    ]
},
```
*   **`command`**: This is the unique identifier for your command. It's a good practice to prefix it with your extension's name (e.g., `yourExtensionId.yourCommandName`). We'll use `aiRuleManager.listRuleSets` as specified in the feature spec.
*   **`title`**: This is the human-readable name that will appear in the VS Code Command Palette.

## 2. Register the Command in `extension.ts`

The `extension.ts` file is the entry point for your extension. In the `activate` function, you need to register the command you defined in `package.json`. This links the command ID to a function that will be executed when the command is invoked.

Open `extension.ts` and add the following code within the `activate` function:
```
typescript
import * as vscode from 'vscode';
import { spawn } from 'child_process'; // Import spawn

export function activate(context: vscode.ExtensionContext) {

    console.log('Congratulations, your extension "ai-rule-manager" is now active!');

    let disposable = vscode.commands.registerCommand('aiRuleManager.listRuleSets', () => {
        // Command handler logic will go here
        vscode.window.showInformationMessage('Listing available rule sets...');
        executeListRulesCommand(); // Call a function to handle the execution
    });

    context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
export function deactivate() {}

// Function to execute the manage_rules.py list-rules command
function executeListRulesCommand() {
    // Implementation details below
}
```
*   We import the `vscode` module and `spawn` from `child_process`.
*   `vscode.commands.registerCommand` takes the command ID as the first argument and the command handler function as the second.
*   The handler function is an arrow function `() => { ... }`. Initially, it just shows an information message. We'll replace this with the script execution logic.
*   `context.subscriptions.push(disposable)` is important for managing the command's lifecycle.

## 3. Implement the Command Handler Logic

Now, let's write the code to execute `manage_rules.py` using `child_process.spawn` and display the output in an output channel.

We'll create a dedicated output channel for our extension.
```
typescript
import * as vscode from 'vscode';
import { spawn } from 'child_process';
import * as path from 'path'; // Import the path module

let outputChannel: vscode.OutputChannel;

export function activate(context: vscode.ExtensionContext) {

    console.log('Congratulations, your extension "ai-rule-manager" is now active!');

    // Create the output channel if it doesn't exist
    if (!outputChannel) {
        outputChannel = vscode.window.createOutputChannel('AI Rule Manager');
    }

    let disposable = vscode.commands.registerCommand('aiRuleManager.listRuleSets', () => {
        outputChannel.clear(); // Clear previous output
        outputChannel.show(); // Show the output channel
        outputChannel.appendLine('Executing manage_rules.py list-rules...');
        executeListRulesCommand(context); // Pass context to get extension path
    });

    context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
export function deactivate() {
    if (outputChannel) {
        outputChannel.dispose(); // Dispose the output channel
    }
}

// Function to execute the manage_rules.py list-rules command
function executeListRulesCommand(context: vscode.ExtensionContext) {
    // Determine the path to the bundled manage_rules.py script
    // Assuming manage_rules.py is in an 'scripts' subdirectory within the extension
    const scriptPath = context.asAbsolutePath(path.join('scripts', 'manage_rules.py'));
    const pythonPath = 'python'; // Or a configurable Python path later

    const process = spawn(pythonPath, [scriptPath, 'list-rules']);

    process.stdout.on('data', (data) => {
        outputChannel.append(data.toString());
    });

    process.stderr.on('data', (data) => {
        outputChannel.append(`Error: ${data.toString()}`);
    });

    process.on('close', (code) => {
        outputChannel.appendLine(`\nmanage_rules.py process exited with code ${code}`);
        if (code !== 0) {
            vscode.window.showErrorMessage('Failed to list rule sets. Check the output channel for details.');
        } else {
             vscode.window.showInformationMessage('Rule sets listed successfully.');
        }
    });

    process.on('error', (err) => {
        outputChannel.appendLine(`Failed to start process: ${err.message}`);
        vscode.window.showErrorMessage('Failed to execute manage_rules.py. Ensure Python is installed and accessible.');
    });
}
```
*   We declare `outputChannel` outside the `activate` function so it persists.
*   Inside `activate`, we create the output channel using `vscode.window.createOutputChannel`.
*   In the command handler, we clear the channel, show it, and append a message indicating execution has started.
*   The `executeListRulesCommand` function uses `context.asAbsolutePath` and `path.join` to construct the absolute path to the bundled `manage_rules.py` script. **Note:** You'll need to adjust the `'scripts'` part if your `manage_rules.py` is bundled in a different subdirectory within the extension.
*   `spawn(pythonPath, [scriptPath, 'list-rules'])` starts the Python process. `pythonPath` is the command to run Python (e.g., 'python', 'python3'). We pass the script path and the 'list-rules' argument as separate elements in an array.
*   `process.stdout.on('data', ...)` and `process.stderr.on('data', ...)` handle the output and errors from the Python script, appending them to our output channel.
*   `process.on('close', ...)` handles the process exiting, reporting the exit code.
*   `process.on('error', ...)` handles errors if the process fails to start (e.g., Python not found).
*   In the `deactivate` function, we dispose of the output channel to clean up resources.

By implementing these steps, you'll have a basic working command in your VS Code extension that can execute the `manage_rules.py` script and show its output to the user.