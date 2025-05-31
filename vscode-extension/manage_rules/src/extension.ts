
import * as vscode from 'vscode';
import { spawn } from 'child_process';
import * as path from "path";
import * as fs from 'fs'; // Import the 'fs' module
import { AIsplendidRuleManagerViewProvider } from './AIsplendidRuleManagerViewProvider';

export function activate(context: vscode.ExtensionContext) {

    console.log('Congratulations, your extension "my-rule-manager" is now active!');

    let disposable = vscode.commands.registerCommand('aiRuleManager.openGUI', () => {
        const panel = vscode.window.createWebviewPanel(
            vscode.commands.executeCommand('workbench.view.focus', 'aiRuleManager') // Reveal the sidebar view
        );
    });
    context.subscriptions.push(disposable);
}

// Function to run manage_rules.py commands
function runManageRulesCommand(command: string, webview: vscode.Webview, context: vscode.ExtensionContext) {
    const outputChannel = vscode.window.createOutputChannel('AI Rule Manager');
    outputChannel.show();

    const scriptPath = context.asAbsolutePath(path.join("python", "src", "manage_rules.py"));

    // Use an integrated terminal for interactive commands
    if (command === 'clean-all' || (command === 'install' && fs.existsSync(path.join(vscode.workspace.rootPath || '', 'project_rules')))) {
        vscode.window.showInformationMessage(`Executing '${command}'. Please switch to the integrated terminal for input.`);
        const terminal = vscode.window.createTerminal('AI Rule Manager Script');
        terminal.show();
        terminal.sendText(`python ${scriptPath} ${command}\n`);
         // We will not capture output here, user interacts with terminal
         webview.postMessage({ command: 'status', text: `Executing '${command}' in terminal. Please refer to the terminal for output and any required interaction.` });

    } else {
        const pythonProcess = spawn('python', [scriptPath, command]);

        outputChannel.appendLine(`Executing: python ${scriptPath} ${command}`);
        webview.postMessage({ command: 'status', text: `Executing: ${command}...` });

        pythonProcess.stdout.on('data', (data) => {
            outputChannel.append(data.toString());
            webview.postMessage({ command: 'output', text: data.toString() });
        });

        pythonProcess.stderr.on('data', (data) => {
            outputChannel.append(`Error: ${data.toString()}`);
            webview.postMessage({ command: 'error', text: data.toString() });
        });

        pythonProcess.on('close', (code) => {
            if (code !== 0) {
                outputChannel.appendLine(`\nmanage_rules.py process exited with code ${code}`);
                vscode.window.showErrorMessage(`manage_rules.py process exited with code ${code}`);
                 webview.postMessage({ command: 'status', text: `${command} failed with code ${code}. Check Output channel.` });
            } else {
                outputChannel.appendLine('\nmanage_rules.py process finished successfully.');
                vscode.window.showInformationMessage(`${command} finished successfully.`);
                 webview.postMessage({ command: 'status', text: `${command} completed successfully.` });
            }
             // If the command was list-rules, send the output back to populate the dropdown
            if (command === 'list-rules' && code === 0) {
                 // Simple parsing for now assumes each line is a rule set
                const ruleSets = outputChannel.toString().split('\n').filter(line => line.trim() !== '' && !line.startsWith('Executing:') && !line.startsWith('manage_rules.py process finished successfully.')).map(line => line.trim());
                webview.postMessage({ command: 'ruleSets', ruleSets: ruleSets });
            }
        });

        pythonProcess.on('error', (err) => {
            outputChannel.appendLine(`Failed to start manage_rules.py process: ${err.message}`);
            vscode.window.showErrorMessage(`Failed to start manage_rules.py: ${err.message}. Is Python installed and in your PATH?`);
             webview.postMessage({ command: 'status', text: `Failed to start ${command}: ${err.message}` });
        });
    }

    // Register the Webview View Provider for the sidebar
    context.subscriptions.push(vscode.window.registerWebviewViewProvider('aiRuleManagerGUI', new AIsplendidRuleManagerViewProvider(context)));
}


// This method is called when your extension is deactivated
export function deactivate() {}