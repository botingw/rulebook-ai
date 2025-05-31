import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

export class AISplendidRuleManagerViewProvider implements vscode.WebviewViewProvider {

    public static readonly viewId = 'aiRuleManagerGUI'; // Must match the view ID in package.json

    private _view?: vscode.WebviewView;

    constructor(
        private readonly _extensionUri: vscode.Uri,
    ) { }

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken,
    ) {
        this._view = webviewView;

 webviewView.webview.options = {
 // Allow scripts in the webview
 enableScripts: true,

 localResourceRoots: [
 vscode.Uri.joinPath(this._extensionUri, 'media'), // Allow access to the media directory
 vscode.Uri.joinPath(this._extensionUri, 'out') // Allow access to the compiled out directory
 ]
 };

 // Get path to HTML file and load its content
 const htmlPath = vscode.Uri.file(
 path.join(this._extensionUri.fsPath, 'media', 'index.html')
 );
 const htmlContent = fs.readFileSync(htmlPath.fsPath, 'utf8');
 webviewView.webview.html = htmlContent;

        // Handle messages from the webview
        webviewView.webview.onDidReceiveMessage(
            message => {
                switch (message.command) {
                    case 'runCommand':
                        // Call a function in extension.ts to run the command
 runManageRulesCommand(message.text, webviewView.webview, context.extension.exports); // Pass extension context exports if needed
                        return;
                }
            },
            undefined,
            this._view.dispose
        );
    }

 // Load rule sets when the GUI opens
 webviewView.webview.postMessage({ command: 'runCommand', text: 'list-rules' });
}

 declare function runManageRulesCommand(command: string, webview: vscode.Webview, context: vscode.ExtensionContext): void;