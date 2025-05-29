import * as vscode from 'vscode';
import { spawn } from 'child_process';

export function activate(context: vscode.ExtensionContext) {

    console.log('Congratulations, your extension "my-rule-manager" is now active!');

    let disposable = vscode.commands.registerCommand('aiRuleManager.listRuleSets', () => {
        // The code you place here will be executed every time your command is executed

        // Create an output channel to display the script's output
        const outputChannel = vscode.window.createOutputChannel('AI Rule Manager');
        outputChannel.show(); // Show the output channel

        // Get the path to the manage_rules.py script
        // Assuming manage_rules.py is at the root of the workspace for now
        // We will refine this later based on our bundling decision
        // In a real extension, you would get the path to the bundled script
        const scriptPath = 'manage_rules.py'; // Placeholder path

        // Spawn the Python process
        // Ensure 'python' is in the system's PATH or use the full path to the interpreter
        const pythonProcess = spawn('python', [scriptPath, 'list-rules']);

        outputChannel.appendLine(`Executing: python ${scriptPath} list-rules`);

        // Handle stdout
        pythonProcess.stdout.on('data', (data) => {
            outputChannel.append(data.toString());
        });

        // Handle stderr
        pythonProcess.stderr.on('data', (data) => {
            outputChannel.append(`Error: ${data.toString()}`);
        });

        // Handle process close
        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                outputChannel.appendLine(`\nmanage_rules.py process exited with code ${code}`);
                vscode.window.showErrorMessage(`manage_rules.py process exited with code ${code}`);
            } else {
                outputChannel.appendLine('\nmanage_rules.py process finished successfully.');
                vscode.window.showInformationMessage('Rule sets listed successfully.');
            }
        });

        // Handle process error (e.g., python executable not found)
        pythonProcess.on('error', (err) => {
            outputChannel.appendLine(`Failed to start manage_rules.py process: ${err.message}`);
            vscode.window.showErrorMessage(`Failed to start manage_rules.py: ${err.message}. Is Python installed and in your PATH?`);
        });
    });

    context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
export function deactivate() {}