// @ts-ignore
const vscode = acquireVsCodeApi();

const installButton = document.getElementById('install-button') as HTMLButtonElement;
const syncButton = document.getElementById('sync-button') as HTMLButtonElement;
const cleanRulesButton = document.getElementById('clean-rules-button') as HTMLButtonElement;
const cleanAllButton = document.getElementById('clean-all-button') as HTMLButtonElement;
const listRulesButton = document.getElementById('list-rules-button') as HTMLButtonElement;
const ruleSetSelect = document.getElementById('rule-set-select') as HTMLSelectElement;
const outputArea = document.getElementById('output-area') as HTMLPreElement;
const statusMessage = document.getElementById('status-message') as HTMLParagraphElement;


installButton.addEventListener('click', () => {
    const selectedRuleSet = ruleSetSelect.value;
    if (selectedRuleSet) {
        vscode.postMessage({ command: 'runCommand', text: `install ${selectedRuleSet}` });
    } else {
        statusMessage.textContent = 'Please select a rule set to install.';
    }
});

syncButton.addEventListener('click', () => {
    vscode.postMessage({ command: 'runCommand', text: 'sync' });
});

cleanRulesButton.addEventListener('click', () => {
    vscode.postMessage({ command: 'runCommand', text: 'clean-rules' });
});

cleanAllButton.addEventListener('click', () => {
    vscode.postMessage({ command: 'runCommand', text: 'clean-all' });
});

listRulesButton.addEventListener('click', () => {
     vscode.postMessage({ command: 'runCommand', text: 'list-rules' });
});


// Handle messages from the extension backend
window.addEventListener('message', event => {
    const message = event.data; // The JSON data our extension sent
    switch (message.command) {
        case 'output':
            outputArea.textContent += message.text;
            break;
        case 'error':
            outputArea.textContent += `Error: ${message.text}`;
            break;
        case 'status':
            statusMessage.textContent = message.text;
            break;
        case 'ruleSets':
            // Populate the rule set dropdown
            ruleSetSelect.innerHTML = ''; // Clear existing options
            message.ruleSets.forEach((ruleSet: string) => {
                const option = document.createElement('option');
                option.value = ruleSet;
                option.textContent = ruleSet;
                ruleSetSelect.appendChild(option);
            });
            break;
    }
});
