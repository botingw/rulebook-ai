# Context for Task 2.3: Implement Command Handlers

This task focuses on writing the JavaScript/TypeScript code in `extension.ts` that will be executed when the user triggers the various AI Rule Manager commands from the Command Palette or the sidebar GUI. These handlers will act as the bridge between the VS Code interface and the `manage_rules.py` command-line script.

## Registering Commands in `extension.ts`

Commands defined in `package.json` need to be registered in the extension's main file (`extension.ts`) so that VS Code knows which function to call when a command is invoked. This is done using `vscode.commands.registerCommand`.
```
typescript
import * as vscode from 'vscode';
import { spawn } from 'child_process';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {

    // Create an output channel for displaying script output
    let outputChannel = vscode.window.createOutputChannel("AI Rule Manager");
    context.subscriptions.push(outputChannel);

    // Register the commands
    let disposableInstall = vscode.commands.registerCommand('aiRuleManager.installFramework', () => {
        handleInstallCommand(outputChannel);
    });
    context.subscriptions.push(disposableInstall);

    let disposableSync = vscode.commands.registerCommand('aiRuleManager.syncRules', () => {
        handleSyncCommand(outputChannel);
    });
    context.subscriptions.push(disposableSync);

    let disposableCleanRules = vscode.commands.registerCommand('aiRuleManager.cleanRules', () => {
        handleCleanRulesCommand(outputChannel);
    });
    context.subscriptions.push(disposableCleanRules);

    let disposableCleanAll = vscode.commands.registerCommand('aiRuleManager.cleanAll', () => {
        handleCleanAllCommand(outputChannel);
    });
    context.subscriptions.push(disposableCleanAll);

    let disposableListRules = vscode.commands.registerCommand('aiRuleManager.listRuleSets', () => {
        handleListRulesCommand(outputChannel);
    });
    context.subscriptions.push(disposableListRules);

    // Add other initializations here
}

export function deactivate() {}

// Command handler functions will be defined below
```
In this example, we register each command ID defined in `package.json` and associate it with a corresponding handler function (`handleInstallCommand`, `handleSyncCommand`, etc.). We also create a dedicated output channel early on to display script output.

## Implementing Command Handler Functions

Each handler function will perform the following steps:

1.  Determine the path to the `manage_rules.py` script (since it's bundled, this will be relative to the extension's installation directory).
2.  Determine the target repository path (the current workspace folder).
3.  Construct the command and arguments to pass to `child_process.spawn`.
4.  Execute the script using `child_process.spawn`.
5.  Handle the script's standard output (stdout) and standard error (stderr), directing it to the output channel.
6.  Listen for the process exit event to determine success or failure.
7.  Use VS Code notification APIs (`showInformationMessage`, `showErrorMessage`) to provide user feedback.
8.  Use VS Code input APIs (`showInputBox`, `showQuickPick`) when user input is required (e.g., selecting a rule set for `install`).

Here are examples of handler functions for the core `manage_rules.py` commands:

### Helper Function to Execute Script

A helper function can encapsulate the common logic for spawning the Python process and handling output.
```
typescript
import * as vscode from 'vscode';
import { spawn, ChildProcessWithoutNullStreams } from 'child_process';
import * as path from 'path';

// Helper function to find the bundled script path
function getScriptPath(context: vscode.ExtensionContext): string | undefined {
    // Assumes manage_rules.py is in a 'dist' or similar folder relative to the extension root
    // Adjust the path based on your actual bundling strategy
    const scriptPath = path.join(context.extensionPath, 'dist', 'manage_rules.py');
    // Basic check if the file exists (more robust checking might be needed)
    return vscode.Uri.file(scriptPath).fsPath; // Using fsPath to get the system path
}

// Helper function to execute the python script
function executeScript(context: vscode.ExtensionContext, command: string, args: string[], outputChannel: vscode.OutputChannel): Promise<number> {
    return new Promise((resolve, reject) => {
        const scriptPath = getScriptPath(context);
        if (!scriptPath) {
            vscode.window.showErrorMessage('manage_rules.py script not found.');
            outputChannel.appendLine('Error: manage_rules.py script not found.');
            return reject(new Error('Script not found'));
        }

        // Determine the Python executable - could be configured by the user later
        // For now, relying on the system's default 'python' or 'python3'
        const pythonExecutable = 'python'; // Or 'python3' or a configurable path

        outputChannel.show(true); // Show the output channel
        outputChannel.appendLine(`Executing command: ${pythonExecutable} ${path.basename(scriptPath)} ${command} ${args.join(' ')}`);
        outputChannel.appendLine('---');

        const process = spawn(pythonExecutable, [scriptPath, command, ...args], {
            cwd: vscode.workspace.workspaceFolders?.[0]?.uri.fsPath // Execute in the workspace root
        });

        process.stdout.on('data', (data) => {
            outputChannel.append(data.toString());
        });

        process.stderr.on('data', (data) => {
            outputChannel.append(data.toString());
            vscode.window.showErrorMessage(`Error during ${command} command. Check output channel for details.`);
        });

        process.on('close', (code) => {
            outputChannel.appendLine('---');
            outputChannel.appendLine(`Command finished with code ${code}`);
            if (code === 0) {
                resolve(code);
            } else {
                reject(new Error(`Command failed with code ${code}`));
            }
        });

        process.on('error', (err) => {
            outputChannel.appendLine(`Failed to start process: ${err.message}`);
            vscode.window.showErrorMessage(`Failed to execute command: ${err.message}. Check output channel.`);
            reject(err);
        });
    });
}
```
### `handleInstallCommand`
```
typescript
import * as vscode from 'vscode';
// ... (import necessary modules like spawn, path, getScriptPath, executeScript)

async function handleInstallCommand(outputChannel: vscode.OutputChannel) {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('No workspace folder open.');
        return;
    }

    try {
        // First, list available rule sets to prompt the user
        outputChannel.appendLine('Fetching available rule sets...');
        const listRulesProcess = spawn('python', [getScriptPath(vscode.extensions.getExtension('your.extension.id')!.extensionPath)!, 'list-rules'], {
             cwd: workspaceFolder.uri.fsPath // Execute in the workspace root if needed, or adjust pathing
        });

        let ruleSetsOutput = '';
        listRulesProcess.stdout.on('data', (data) => {
            ruleSetsOutput += data.toString();
        });

        await new Promise((resolve, reject) => {
            listRulesProcess.on('close', (code) => {
                if (code === 0) {
                    resolve(null);
                } else {
                    reject(new Error(`Failed to list rule sets (code ${code})`));
                }
            });
            listRulesProcess.on('error', reject);
        });

        const availableRuleSets = ruleSetsOutput.split('\n')
                                                .map(line => line.trim())
                                                .filter(line => line && !line.startsWith('Available rule sets:')); // Parse the output

        const selectedRuleSet = await vscode.window.showQuickPick(availableRuleSets, {
            placeHolder: 'Select a rule set to install',
            ignoreFocusOut: true // Keep the picker open
        });

        if (!selectedRuleSet) {
            vscode.window.showInformationMessage('Install cancelled.');
            return;
        }

        outputChannel.appendLine(`Installing framework with rule set: ${selectedRuleSet}`);
        await executeScript(vscode.extensions.getExtension('your.extension.id')!, 'install', [workspaceFolder.uri.fsPath, '--rule-set', selectedRuleSet], outputChannel);

        vscode.window.showInformationMessage('AI Rule Management Framework installed successfully!');
        outputChannel.appendLine('Remember to review and commit project-specific files (memory/, tools/, env.example, requirements.txt) and add generated files to .gitignore.');

    } catch (error: any) {
        vscode.window.showErrorMessage(`Failed to install framework: ${error.message}`);
        outputChannel.appendLine(`Error: ${error.message}`);
    }
}
```
*Note: Replace `'your.extension.id'` with your actual extension ID.*

### `handleSyncCommand`
```
typescript
import * as vscode from 'vscode';
// ... (import necessary modules like spawn, path, getScriptPath, executeScript)

async function handleSyncCommand(outputChannel: vscode.OutputChannel) {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('No workspace folder open.');
        return;
    }

    try {
        outputChannel.appendLine('Synchronizing rules...');
        await executeScript(vscode.extensions.getExtension('your.extension.id')!, 'sync', [workspaceFolder.uri.fsPath], outputChannel);
        vscode.window.showInformationMessage('AI Rules synchronized successfully!');
    } catch (error: any) {
        vscode.window.showErrorMessage(`Failed to synchronize rules: ${error.message}`);
         outputChannel.appendLine(`Error: ${error.message}`);
    }
}
```
*Note: Replace `'your.extension.id'` with your actual extension ID.*

### `handleCleanRulesCommand`
```
typescript
import * as vscode from 'vscode';
// ... (import necessary modules like spawn, path, getScriptPath, executeScript)

async function handleCleanRulesCommand(outputChannel: vscode.OutputChannel) {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('No workspace folder open.');
        return;
    }

    const confirm = await vscode.window.showQuickPick(['Yes', 'No'], {
        placeHolder: 'Are you sure you want to remove rule files and the project_rules/ directory? This action is not reversible.',
        ignoreFocusOut: true
    });

    if (confirm !== 'Yes') {
        vscode.window.showInformationMessage('Clean Rules cancelled.');
        return;
    }

    try {
        outputChannel.appendLine('Cleaning rule files and project_rules/ directory...');
        await executeScript(vscode.extensions.getExtension('your.extension.id')!, 'clean-rules', [workspaceFolder.uri.fsPath], outputChannel);
        vscode.window.showInformationMessage('Rule files cleaned successfully!');
    } catch (error: any) {
        vscode.window.showErrorMessage(`Failed to clean rule files: ${error.message}`);
         outputChannel.appendLine(`Error: ${error.message}`);
    }
}
```
*Note: Replace `'your.extension.id'` with your actual extension ID.*

### `handleCleanAllCommand`
```
typescript
import * as vscode from 'vscode';
// ... (import necessary modules like spawn, path, getScriptPath, executeScript)

async function handleCleanAllCommand(outputChannel: vscode.OutputChannel) {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('No workspace folder open.');
        return;
    }

    const confirm = await vscode.window.showInputBox({
        prompt: 'This will remove ALL framework components (project_rules/, memory/, tools/, generated rules, env.example, requirements.txt). Type "yes" to confirm.',
        placeHolder: 'Type "yes" to confirm',
        ignoreFocusOut: true
    });

    if (confirm !== 'yes') {
        vscode.window.showInformationMessage('Clean All cancelled.');
        return;
    }

    try {
        outputChannel.appendLine('Cleaning all framework components...');
        await executeScript(vscode.extensions.getExtension('your.extension.id')!, 'clean-all', [workspaceFolder.uri.fsPath], outputChannel);
        vscode.window.showInformationMessage('All AI Rule Management Framework components removed successfully!');
    } catch (error: any) {
        vscode.window.showErrorMessage(`Failed to clean all components: ${error.message}`);
         outputChannel.appendLine(`Error: ${error.message}`);
    }
}
```
*Note: Replace `'your.extension.id'` with your actual extension ID.*

### `handleListRulesCommand`
```
typescript
import * as vscode from 'vscode';
// ... (import necessary modules like spawn, path, getScriptPath, executeScript)

async function handleListRulesCommand(outputChannel: vscode.OutputChannel) {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    // This command might not strictly need a workspace folder if the script can list rules from its bundled location
    // Adjust execution context (cwd) as needed for the script's implementation of list-rules
    const executionCwd = workspaceFolder ? workspaceFolder.uri.fsPath : undefined;


    try {
        outputChannel.appendLine('Listing available rule sets...');
        // For list-rules, we might just want to show the output in a quick pick and the output channel
        let ruleSetsOutput = '';
        const listProcess = spawn('python', [getScriptPath(vscode.extensions.getExtension('your.extension.id')!)!, 'list-rules'], {
             cwd: executionCwd // Adjust cwd if script's list-rules doesn't need a target repo
        });

        outputChannel.show(true); // Show the output channel
        outputChannel.appendLine(`Executing command: python ${path.basename(getScriptPath(vscode.extensions.getExtension('your.extension.id')!)!)} list-rules`);
        outputChannel.appendLine('---');


        listProcess.stdout.on('data', (data) => {
            const dataString = data.toString();
            outputChannel.append(dataString);
            ruleSetsOutput += dataString;
        });

        listProcess.stderr.on('data', (data) => {
            outputChannel.append(data.toString());
            vscode.window.showErrorMessage(`Error listing rule sets. Check output channel for details.`);
        });

        listProcess.on('close', async (code) => {
            outputChannel.appendLine('---');
            outputChannel.appendLine(`Command finished with code ${code}`);
            if (code === 0) {
                 vscode.window.showInformationMessage('Available rule sets listed in output channel.');
                 // Optionally parse ruleSetsOutput and show in a QuickPick for easier reading
                 const availableRuleSets = ruleSetsOutput.split('\n')
                                                 .map(line => line.trim())
                                                 .filter(line => line && !line.startsWith('Available rule sets:'));

                 if (availableRuleSets.length > 0) {
                     await vscode.window.showQuickPick(availableRuleSets, {
                         title: 'Available Rule Sets',
                         ignoreFocusOut: true
                     });
                 } else {
                      vscode.window.showInformationMessage('No rule sets found.');
                 }

            } else {
                vscode.window.showErrorMessage(`Failed to list rule sets (code ${code}). Check output channel.`);
            }
        });

         listProcess.on('error', (err) => {
            outputChannel.appendLine(`Failed to start process: ${err.message}`);
            vscode.window.showErrorMessage(`Failed to execute command: ${err.message}. Check output channel.`);
        });


    } catch (error: any) {
        // This catch might be less relevant if handling errors in the process events directly
        vscode.window.showErrorMessage(`An error occurred while listing rule sets: ${error.message}`);
         outputChannel.appendLine(`Error: ${error.message}`);
    }
}
```
*Note: Replace `'your.extension.id'` with your actual extension ID.*

## Using VS Code APIs for User Interaction

*   `vscode.window.showInformationMessage(message)`: Displays an informational message to the user. Useful for success confirmations or general guidance.
*   `vscode.window.showErrorMessage(message)`: Displays an error message to the user. Use when a command fails or encounters a problem.
*   `vscode.window.showInputBox(options)`: Prompts the user for text input. Used in the `cleanAll` example for confirmation. Can be used for other inputs like a custom rule set path if that feature were added.
*   `vscode.window.showQuickPick(items, options)`: Displays a list of items for the user to select from. Used in the `install` example to let the user choose a rule set from the available options.

These APIs provide standard VS Code UI elements for interacting with the user and should be used to make the extension intuitive and informative.