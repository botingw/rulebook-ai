import * as vscode from 'vscode';
import * as path from 'path';
import { SidebarProvider } from './sidebarProvider';
import { getRuleSets, confirmModal, openTerminalAndRun } from './utils';

const PYTHON_SCRIPT_NAME = 'manage_rules.py'; // As per spec, expected in workspace root

export function activate(context: vscode.ExtensionContext) {
    console.log('Congratulations, your extension "manage-rules-vscode" is now active!');

    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (!workspaceFolders || workspaceFolders.length === 0) {
        vscode.window.showErrorMessage('Manage Rules: No folder opened. Please open a folder to use this extension.');
        return;
    }
    const rootPath = workspaceFolders[0].uri.fsPath;

    // As per spec (Section 7, Assumption 2), manage_rules.py is expected in the workspace root.
    // If it were bundled with the extension, the path would be constructed using context.extensionUri:
    // const scriptFullPath = vscode.Uri.joinPath(context.extensionUri, 'python', 'src', PYTHON_SCRIPT_NAME).fsPath;
    // And commands would use `scriptFullPath` instead of just `PYTHON_SCRIPT_NAME`.
    // For this 0.0.1-alpha, we adhere to `PYTHON_SCRIPT_NAME` being in `rootPath`.

    const getPythonExecutable = (): string => {
        return vscode.workspace.getConfiguration('manageRules').get<string>('pythonPath', 'python3');
    };

    const sidebarProvider = new SidebarProvider();
    vscode.window.registerTreeDataProvider('manageRulesView', sidebarProvider);
    vscode.window.createTreeView('manageRulesView', { treeDataProvider: sidebarProvider });


    // --- Command Registrations ---

    context.subscriptions.push(
        vscode.commands.registerCommand('manageRules.installRuleSet', async () => {
            const pythonExecutable = getPythonExecutable();
            try {
                const ruleSets = getRuleSets(rootPath, pythonExecutable, PYTHON_SCRIPT_NAME);
                if (ruleSets.length === 0) {
                    vscode.window.showInformationMessage('No rule sets found by manage_rules.py list-rules.');
                    return;
                }

                const selectedRuleSet = await vscode.window.showQuickPick(ruleSets, {
                    placeHolder: 'Select a rule set to install',
                });

                if (selectedRuleSet) {
                    const confirmed = await confirmModal(`Are you sure you want to install the rule set "${selectedRuleSet}"?`);
                    if (confirmed) {
                        const command = `${pythonExecutable} ${PYTHON_SCRIPT_NAME} install . --rule-set ${selectedRuleSet}`;
                        openTerminalAndRun(command, rootPath);
                    }
                }
            } catch (error: any) {
                vscode.window.showErrorMessage(`Error installing rule set: ${error.message}`);
            }
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('manageRules.syncRuleSet', async () => {
            const pythonExecutable = getPythonExecutable();
            const confirmed = await confirmModal('Are you sure you want to sync the current rule set(s) with the project?');
            if (confirmed) {
                const command = `${pythonExecutable} ${PYTHON_SCRIPT_NAME} sync .`;
                openTerminalAndRun(command, rootPath);
            }
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('manageRules.cleanRules', async () => {
            const pythonExecutable = getPythonExecutable();
            const confirmed = await vscode.window.showWarningMessage(
                'Warning: This will clean (remove) all currently installed rules from your project. Are you sure?',
                { modal: true },
                'Yes', 'No'
            );
            if (confirmed === 'Yes') {
                const command = `${pythonExecutable} ${PYTHON_SCRIPT_NAME} clean-rules .`;
                openTerminalAndRun(command, rootPath);
            }
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('manageRules.cleanAll', async () => {
            const pythonExecutable = getPythonExecutable();
            const confirmed = await vscode.window.showWarningMessage(
                'BIG WARNING: This will clean (remove) ALL managed files, including rules, memory, tools, etc. This is a highly destructive operation. Are you absolutely sure?',
                { modal: true },
                'Yes, Clean All', 'Cancel'
            );
            if (confirmed === 'Yes, Clean All') {
                const command = `${pythonExecutable} ${PYTHON_SCRIPT_NAME} clean-all .`;
                openTerminalAndRun(command, rootPath);
            }
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('manageRules.listRules', async () => {
            const pythonExecutable = getPythonExecutable();
            try {
                const ruleSets = getRuleSets(rootPath, pythonExecutable, PYTHON_SCRIPT_NAME);
                if (ruleSets.length > 0) {
                    vscode.window.showInformationMessage(`Available rule sets:\n- ${ruleSets.join('\n- ')}`);
                } else {
                    vscode.window.showInformationMessage('No available rule sets found.');
                }
            } catch (error: any) {
                vscode.window.showErrorMessage(`Error listing rule sets: ${error.message}`);
            }
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('manageRules.runCustomCli', async () => {
            const pythonExecutable = getPythonExecutable();
            const customArgs = await vscode.window.showInputBox({
                prompt: `Enter arguments for ${PYTHON_SCRIPT_NAME} (e.g., 'list-tools --verbose')`,
                placeHolder: 'arguments...',
            });

            if (customArgs !== undefined) { // User provided input (can be empty string)
                const command = `${pythonExecutable} ${PYTHON_SCRIPT_NAME} ${customArgs}`;
                openTerminalAndRun(command, rootPath);
            }
        })
    );
}

export function deactivate() {}