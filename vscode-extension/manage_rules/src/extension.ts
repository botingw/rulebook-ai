
import * as vscode from 'vscode';
import { spawn } from 'child_process';
import * as path from "path";
import * as fs from 'fs'; // Import the 'fs' module

export function activate(context: vscode.ExtensionContext) {

    console.log('Congratulations, your extension "my-rule-manager" is now active!');

    let disposable = vscode.commands.registerCommand('aiRuleManager.openGUI', () => {
        const panel = vscode.window.createWebviewPanel(
            'aiRuleManagerGUI', // Identifies the type of the webview. Used internally
            'AI Rule Manager GUI', // Title of the panel displayed to the user
            vscode.ViewColumn.One, // Editor column to show the new panel in.
            {
                enableScripts: true, // Enable scripts in the webview
                localResourceRoots: [vscode.Uri.file(path.join(context.extensionPath, 'media'))] // Restrict the webview to only load resources from the media directory
 localResourceRoots: [vscode.Uri.file(path.join(context.extensionPath, 'media')), vscode.Uri.file(path.join(context.extensionPath, 'out'))] // Allow loading resources from media and out directories
            }
        );

        // Get path to HTML file and load its content
        const htmlPath = vscode.Uri.file(
            path.join(context.extensionPath, 'media', 'index.html')
        );
        const htmlContent = fs.readFileSync(htmlPath.fsPath, 'utf8');
        panel.webview.html = htmlContent;

        // Handle messages from the webview
        panel.webview.onDidReceiveMessage(
            message => {
                switch (message.command) {
                    case 'runCommand':
                        runManageRulesCommand(message.text, panel.webview, context); // Call a function to run the command
                        return;
                }
            },
            undefined,
            context.subscriptions
        );

        // Load rule sets when the GUI opens
        runManageRulesCommand('list-rules', panel.webview, context);
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
}


// This method is called when your extension is deactivated
export function deactivate() {}