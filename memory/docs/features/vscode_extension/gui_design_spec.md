**Simple GUI User Experience Design**

The GUI will reside in a dedicated View Container (sidebar panel) within VS Code. It will be a single page with the following sections:

1.  **Command Buttons:** A set of prominent buttons, each representing a core `manage_rules.py` command:
    *   Install
    *   Sync Rules
    *   Clean Rules
    *   Clean All
    *   List Available Rule Sets

2.  **Rule Set Selection (for Install):** Below the "Install" button, a dropdown or input field will allow the user to select the desired rule set for installation. This dropdown will be populated when the GUI is opened by running the `list-rules` command in the background (non-interactively) and displaying the results in a dedicated area (see below).

3.  **Output and Information Area:** A read-only area within the GUI (or a clear link to the dedicated Output Channel) where the user can see:
    *   The list of available rule sets after the GUI loads.
    *   Status messages indicating which command is being executed.
    *   Any non-interactive output from the `manage_rules.py` script (e.g., progress messages, summaries).
    *   Crucially, for commands that require user input (like `clean-all` and potentially `install` if `project_rules/` exists), a message clearly instructing the user to look at the **integrated terminal** for prompts and to provide input there.

**User Interaction Flow (Revised)**

1.  **Opening the GUI:** The user opens the GUI from a single Command Palette entry (e.g., "AI Rule Manager: Open GUI").
2.  **Loading Rule Sets:** When the GUI opens, the extension automatically runs `manage_rules.py list-rules` in the background. The output is captured and displayed in the Output and Information Area within the GUI.
3.  **Initiating Commands (Non-Interactive):** When the user clicks a button for a non-interactive command (e.g., "Sync Rules", "Clean Rules", "List Available Rule Sets"):
    *   The GUI sends a message to the extension's backend.
    *   The backend executes the corresponding `manage_rules.py` command using `child_process.spawn`.
    *   The standard output and standard error of the script are streamed to the Output and Information Area in the GUI and/or the dedicated VS Code Output Channel.
    *   Status messages are displayed in the Output and Information Area (e.g., "Executing Sync Rules...", "Sync Rules completed.").
4.  **Initiating Commands (Interactive - Clean All & Install Prompt):** When the user clicks a button for a command that might require user input (`Clean All`, and potentially `Install` if `project_rules/` exists):
    *   The GUI sends a message to the extension's backend.
    *   The backend executes the corresponding `manage_rules.py` command using `child_process.spawn`.
    *   **Crucially, a clear message appears in the Output and Information Area instructing the user:** "This command requires your confirmation in the integrated terminal. Please switch to the terminal to proceed."
    *   The backend does *not* attempt to capture or respond to the prompts. The prompts will appear directly in the integrated terminal where the spawned process is running.
    *   The user switches to the integrated terminal and provides the required input ("yes" or "no").
    *   The rest of the script's output is then streamed to the Output and Information Area.

**Advantages of this Simple Design:**

*   **Reduced Coupling:** The extension's code doesn't need to parse script output for specific prompts or manage the script's `stdin`/`stdout` for interactive sequences.
*   **Easier Maintenance:** Changes to the prompts or interactive behavior of `manage_rules.py` have minimal impact on the extension's codebase.
*   **Faster Implementation:** This approach is significantly faster to implement as it avoids the complexity of building an interactive layer within the Webview or extension backend.

**Disadvantages:**

*   **Less Seamless User Experience:** Users need to switch between the GUI and the integrated terminal for certain commands, which is not as smooth as a fully integrated interactive experience.
*   **Potential for User Confusion:** Users might miss the instruction to look at the terminal, especially if they are not accustomed to using the integrated terminal. Clear messaging in the GUI is crucial to mitigate this.