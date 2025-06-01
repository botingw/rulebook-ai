import * as vscode from 'vscode';

export class SidebarProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<vscode.TreeItem | undefined | null | void> = new vscode.EventEmitter<vscode.TreeItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<vscode.TreeItem | undefined | null | void> = this._onDidChangeTreeData.event;

    getTreeItem(element: vscode.TreeItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: vscode.TreeItem): Thenable<vscode.TreeItem[]> {
        if (element) {
            // This is a flat list, so children of items are not expected.
            return Promise.resolve([]);
        } else {
            // Root level items
            return Promise.resolve([
                new ActionItem('Install Rule Set', 'manageRules.installRuleSet', 'Install a new rule set into the project.'),
                new ActionItem('Sync Rule Set', 'manageRules.syncRuleSet', 'Synchronize the current rule set(s) with the project.'),
                new ActionItem('Clean Rules', 'manageRules.cleanRules', 'Remove installed rules from the project.'),
                new ActionItem('Clean All', 'manageRules.cleanAll', 'Remove all managed files (rules, memory, tools, etc.).'),
                new ActionItem('List Available Rule Sets', 'manageRules.listRules', 'Display a list of rule sets available from manage_rules.py.'),
                new ActionItem('Run Custom CLI…', 'manageRules.runCustomCli', 'Run manage_rules.py with custom arguments.')
            ]);
        }
    }

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }
}

class ActionItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        commandId: string,
        tooltip?: string,
        icon?: string | vscode.Uri | { light: string | vscode.Uri; dark: string | vscode.Uri } | vscode.ThemeIcon
    ) {
        super(label, vscode.TreeItemCollapsibleState.None);
        this.tooltip = tooltip || label;
        this.command = {
            command: commandId,
            title: label,
            arguments: [] // No arguments passed directly from tree item click
        };
        if (icon) {
            this.iconPath = icon;
        } else {
            // Example: using built-in icons
            // this.iconPath = new vscode.ThemeIcon('zap'); // Placeholder
        }
    }
}