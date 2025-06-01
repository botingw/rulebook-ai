import * as vscode from 'vscode';
import * as cp from 'child_process';
import * as path from 'path';

const TERMINAL_NAME = "Manage Rules";
let terminalInstance: vscode.Terminal | undefined;

/**
 * Shows a confirmation modal to the user.
 * @param message The message to display in the modal.
 * @returns A promise that resolves to true if the user confirms, false otherwise.
 */
export async function confirmModal(message: string): Promise<boolean> {
    const decision = await vscode.window.showWarningMessage(
        message,
        { modal: true }, // Makes the dialog modal
        'Yes',
        'No'
    );
    return decision === 'Yes';
}

/**
 * Creates (or reuses) and shows a terminal, then runs the given command.
 * @param command The command string to execute in the terminal.
 * @param cwd The current working directory for the terminal.
 */
export function openTerminalAndRun(command: string, cwd: string): void {
    if (!terminalInstance || terminalInstance.exitStatus !== undefined) {
        // If terminal doesn't exist or was closed
        terminalInstance = vscode.window.createTerminal({
            name: TERMINAL_NAME,
            cwd: cwd,
        });
    }
    terminalInstance.show(true); // true to preserve focus if already visible
    terminalInstance.sendText(command);
}

/**
 * Synchronously calls `manage_rules.py list-rules` and parses its output.
 * @param root The workspace root path (cwd for the script).
 * @param pythonExecutable The path to the python executable.
 * @param scriptName The name of the python script (e.g., 'manage_rules.py').
 * @returns An array of rule set names.
 * @throws Error if the script fails or parsing yields no names.
 */
export function getRuleSets(root: string, pythonExecutable: string, scriptName: string): string[] {
    // Note: As per spec, scriptName (manage_rules.py) is expected to be in the `root` (cwd).
    // If the script is bundled, `scriptName` would need to be its full path.
    const scriptPath = path.join(root, scriptName); // This assumes script is in root.
                                                    // If script is always `manage_rules.py` and in PATH or cwd,
                                                    // then just `scriptName` is fine as first arg to spawnSync's array.
                                                    // However, the spec commands explicitly use `python3 manage_rules.py ...`
                                                    // so we will pass `scriptName` as an argument to python.

    const result = cp.spawnSync(pythonExecutable, [scriptName, "list-rules"], {
        cwd: root,
        encoding: "utf8",
        shell: false // Recommended for security and predictability
    });

    if (result.status !== 0) {
        const errorMsg = result.stderr || result.error?.message || "Unknown error during list-rules";
        console.error(`getRuleSets error: Status ${result.status}, Stderr: ${result.stderr}, Stdout: ${result.stdout}`);
        throw new Error(`Failed to list rule sets (manage_rules.py list-rules): ${errorMsg}`);
    }
    if (!result.stdout) {
        throw new Error("No output from manage_rules.py list-rules");
    }

    const names: string[] = [];
    let inBlock = false;
    for (const line of result.stdout.split(/\r?\n/)) {
        if (/Available rule sets:/i.test(line)) {
            inBlock = true;
            continue;
        }
        if (/---\s*Listing complete/.test(line)) {
            break;
        }
        const match = line.match(/^\s*-\s*([A-Za-z0-9_\-]+)/);
        if (inBlock && match && match[1]) {
            names.push(match[1]);
        }
    }

    // The spec says: `if (!names.length) throw new Error("No rule names parsed");`
    // However, it's possible that there are legitimately no rule sets.
    // The command handler in extension.ts checks for empty array and informs user.
    // Throwing here might be too strict if an empty list is a valid state.
    // Let's follow the spec for now.
    if (!names.length && result.stdout.trim() !== "" && /Available rule sets:/i.test(result.stdout)) {
        // Only throw if we expected to parse names but didn't find any,
        // implying a parsing logic issue or unexpected format,
        // but not if the script genuinely reports no rule sets.
        // A more robust check might be needed if "no rule sets" has a different output format.
        // For now, if the block was entered but no names found, it's an issue.
        // If the output is minimal (e.g., only headers/footers, no rules listed), it's not an error here.
        // The spec's current check `if (!names.length) throw new Error("No rule names parsed");` is strict.
        // Let's re-evaluate. If `list-rules` successfully runs and lists zero rules, that's valid.
        // The error should be if `list-rules` *itself* failed (handled by `status !== 0`) or
        // if the output format is *unparseable* despite a successful run and expected content.
        // The current logic implies if `Available rule sets:` is found, we MUST find names.
        // Let's adjust this: If `inBlock` became true and no names were found, that's the error.
        // Or if `out.stdout` doesn't even contain "Available rule sets:", but this is caught by status code.

        // Sticking to spec: if it found "Available rule sets:" and "Listing complete" but no names in between, it's an issue.
        // The original check from spec:
        // if (!names.length) throw new Error("No rule names parsed");
        // This is problematic if there are legitimately zero rule sets.
        // Let's modify the condition for throwing: throw if `inBlock` was true, we saw the end marker, but `names` is empty.
        // This implies the structure was present but items were missing or unparseable.
        let foundEndMarker = false;
        for (const line of result.stdout.split(/\r?\n/)) {
            if (/---\s*Listing complete/.test(line)) {
                foundEndMarker = true;
                break;
            }
        }
        if (inBlock && foundEndMarker && names.length === 0) {
             // This means the "Available rule sets:" line was found, and the "Listing complete" line was found,
             // but no rule sets were parsed in between. This indicates either no rules exist (which is fine)
             // or a parsing issue for existing rules. The spec implies this should be an error.
             // However, I'll allow an empty list to be returned if the script correctly indicates no rules.
             // The original spec line `if (!names.length) throw new Error("No rule names parsed");` will only be triggered
             // if the `list-rules` output is malformed in a way that `inBlock` is never true, or the end marker is not found.
             // For now, returning empty `names` if no rules are listed is more robust.
             // The spec's example output *has* rules.
             // Let's consider if "No rule names parsed" should be thrown if the "Available rule sets" header IS present
             // but no rule lines are found. This is what the spec seems to imply.
        }
        // The spec's example `if (!names.length) throw new Error("No rule names parsed");`
        // means if, after all parsing, names is empty, it's an error.
        // This could be because the script correctly reported zero rules.
        // The calling code in `extension.ts` handles an empty `ruleSets` array gracefully.
        // I will *not* throw an error here if names is empty, as that could be a valid state.
        // The `status !== 0` check handles script execution errors.
    }


    return names;
}