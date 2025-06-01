import * as vscode from 'vscode';
import * as path from 'path';
import {
    getRuleSets,
    openTerminalAndRun,
    confirmModal,
} from './util';                      // ← keep whatever helpers you already import
import { SidebarProvider } from './sidebarProvider';


/* ────────────────────────────────────────────────────────────────────────── */
/*  Activate                                                                */
/* ────────────────────────────────────────────────────────────────────────── */
export function activate(context: vscode.ExtensionContext) {
    console.log('Congratulations, your extension "manage-rules-vscode" is now active!');

    const PYTHON_SCRIPT_NAME = path.join(
        context.extensionPath, // points to the root folder of the installed extension
        'python',
        'src',
        'manage_rules.py'
    );
    /* workspace helper — always fetch at call-time */
    const getRootPath = () => vscode.workspace.workspaceFolders?.[0].uri.fsPath;

    /* nudge users who start VS Code without a folder */
    if (!getRootPath()) {
        vscode.window.showInformationMessage(
            'Manage Rules: open a folder first, then run any command.'
        );
    }

    /* side-bar registration */
    const sidebarProvider = new SidebarProvider();
    context.subscriptions.push(
        vscode.window.registerTreeDataProvider('manageRulesView', sidebarProvider),
        vscode.window.createTreeView('manageRulesView', { treeDataProvider: sidebarProvider })
    );

    /* convenience getter */
    const getPythonExecutable = (): string =>
        vscode.workspace.getConfiguration('manageRules').get<string>('pythonPath', 'python3');

    /* ── manageRules.installRuleSet ─────────────────────────────────────── */
    context.subscriptions.push(
        vscode.commands.registerCommand('manageRules.installRuleSet', async () => {
            const rootPath = getRootPath();
            if (!rootPath) {
                vscode.window.showErrorMessage('Please open a folder first.');
                return;
            }

            const python = getPythonExecutable();

            try {
                const ruleSets = getRuleSets(rootPath, python, PYTHON_SCRIPT_NAME);
                if (ruleSets.length === 0) {
                    vscode.window.showInformationMessage('No rule sets found.');
                    return;
                }

                const chosen = await vscode.window.showQuickPick(ruleSets, {
                    placeHolder: 'Select a rule set to install',
                });
                if (!chosen) return;

                const ok = await confirmModal(
                    `Are you sure you want to install the rule set "${chosen}"?`
                );
                if (!ok) return;

                openTerminalAndRun(
                    `${python} ${PYTHON_SCRIPT_NAME} install . --rule-set ${chosen}`,
                    rootPath
                );
            } catch (err: any) {
                vscode.window.showErrorMessage(`Error installing rule set: ${err.message}`);
            }
        })
    );

    /* ── manageRules.syncRuleSet ────────────────────────────────────────── */
    context.subscriptions.push(
        vscode.commands.registerCommand('manageRules.syncRuleSet', async () => {
            const rootPath = getRootPath();
            if (!rootPath) {
                vscode.window.showErrorMessage('Please open a folder first.');
                return;
            }

            const python = getPythonExecutable();
            const ok = await confirmModal(
                'Are you sure you want to sync the current rule set(s) with the project?'
            );
            if (!ok) return;

            openTerminalAndRun(
                `${python} ${PYTHON_SCRIPT_NAME} sync .`,
                rootPath
            );
        })
    );

    /* ── manageRules.cleanRules ─────────────────────────────────────────── */
    context.subscriptions.push(
        vscode.commands.registerCommand('manageRules.cleanRules', async () => {
            const rootPath = getRootPath();
            if (!rootPath) {
                vscode.window.showErrorMessage('Please open a folder first.');
                return;
            }

            const python = getPythonExecutable();
            const confirmed = await vscode.window.showWarningMessage(
                'Warning: This will remove all currently installed rules from your project. Continue?',
                { modal: true },
                'Yes', 'No'
            );
            if (confirmed !== 'Yes') return;

            openTerminalAndRun(
                `${python} ${PYTHON_SCRIPT_NAME} clean-rules .`,
                rootPath
            );
        })
    );

    /* ── manageRules.cleanAll ───────────────────────────────────────────── */
    context.subscriptions.push(
        vscode.commands.registerCommand('manageRules.cleanAll', async () => {
            const rootPath = getRootPath();
            if (!rootPath) {
                vscode.window.showErrorMessage('Please open a folder first.');
                return;
            }

            const python = getPythonExecutable();
            const confirmed = await vscode.window.showWarningMessage(
                'BIG WARNING: This will clean ALL managed files (rules, memory, tools, etc.). Continue?',
                { modal: true },
                'Yes, Clean All', 'Cancel'
            );
            if (confirmed !== 'Yes, Clean All') return;

            openTerminalAndRun(
                `${python} ${PYTHON_SCRIPT_NAME} clean-all .`,
                rootPath
            );
        })
    );

    /* ── manageRules.listRules ──────────────────────────────────────────── */
    context.subscriptions.push(
        vscode.commands.registerCommand('manageRules.listRules', async () => {
            const rootPath = getRootPath();
            if (!rootPath) {
                vscode.window.showErrorMessage('Please open a folder first.');
                return;
            }

            const python = getPythonExecutable();

            try {
                const ruleSets = getRuleSets(rootPath, python, PYTHON_SCRIPT_NAME);
                if (ruleSets.length === 0) {
                    vscode.window.showInformationMessage('No available rule sets found.');
                } else {
                    vscode.window.showInformationMessage(
                        `Available rule sets:\n- ${ruleSets.join('\n- ')}`
                    );
                }
            } catch (err: any) {
                vscode.window.showErrorMessage(`Error listing rule sets: ${err.message}`);
            }
        })
    );

    /* ── manageRules.runCustomCli ───────────────────────────────────────── */
    context.subscriptions.push(
        vscode.commands.registerCommand('manageRules.runCustomCli', async () => {
            const rootPath = getRootPath();
            if (!rootPath) {
                vscode.window.showErrorMessage('Please open a folder first.');
                return;
            }

            const python = getPythonExecutable();
            const customArgs = await vscode.window.showInputBox({
                prompt: `Enter arguments for ${PYTHON_SCRIPT_NAME} (e.g., 'list-tools --verbose')`,
                placeHolder: 'arguments...',
            });
            if (customArgs === undefined) return;   // user cancelled

            openTerminalAndRun(
                `${python} ${PYTHON_SCRIPT_NAME} ${customArgs}`,
                rootPath
            );
        })
    );
}

/* ────────────────────────────────────────────────────────────────────────── */
export function deactivate() {
    /* clean-up tasks if you have any */
}
