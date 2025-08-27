# VS Code Extension Development Plan: `manage_rules.py` Wrapper

## Project Goal

Develop a VS Code extension that provides a user-friendly interface within the IDE to interact with the `manage_rules.py` script. This will allow users to manage their AI rules directly from VS Code, improving workflow efficiency.

## Phase 1: Setup and Basic Implementation

1.  **Set up VS Code Extension Development Environment:**
    *   Install Node.js and npm.
    *   Install the VS Code Extension Generator (`yo code`).
    *   Generate a new TypeScript or JavaScript extension project using `yo code`.
    *   Familiarize with the extension project structure (`package.json`, `extension.ts`).

2.  **Integrate `manage_rules.py`:**
    *   Determine the best way to execute the Python script from the Node.js/TypeScript extension (e.g., using `child_process.exec` or `spawn`).
    *   Ensure the Python script is accessible to the extension (e.g., bundled with the extension or requiring a user-specified path).

3.  **Implement a Basic Command:**
    *   Define a simple command in `package.json` (e.g., `aiRuleManager.listRuleSets`).
    *   Register the command in `extension.ts`.
    *   In the command handler, execute `manage_rules.py` with a basic argument (e.g., listing available rules) and display the output in a VS Code output channel.

## Phase 2: GUI and Core Command Implementation (POC Focus)

1.  **Identify Key `manage_rules.py` Functionality:**
    *   Review the `manage_rules.py` script to understand its core commands and arguments: `install`, `sync`, `clean-rules`, `clean-all`, `list-rules`.

2.  **Create Dedicated View Container (Sidebar):**
    *   For each key function of `manage_rules.py`, define a corresponding VS Code command in `package.json`.

3.  **Implement Command Handlers:**
    *   In `extension.ts`, register handlers for each defined command.
    *   Within each handler, execute `manage_rules.py` with the appropriate arguments based on the command.
    *   Use VS Code APIs to interact with the user:
        *   `vscode.window.showInformationMessage` for success messages.
        *   `vscode.window.showErrorMessage` for errors.
        *   `vscode.window.showInputBox` to get user input (e.g., rule file path).
        *   `vscode.window.showQuickPick` to allow users to select from a list (e.g., available rule sets during install if not using a dropdown in the GUI).

4.  **Build GUI in View Container:**
    *   Define and register a new View Container and a View within the VS Code sidebar using `package.json`.
    *   Implement the UI elements within the dedicated sidebar view using a Webview. This includes:
        *   HTML, CSS, and JavaScript for the view's layout and interactivity.
        *   Buttons for triggering the `install`, `sync`, `clean-rules`, and `clean-all` commands.
        *   An input field or dropdown for selecting the rule set during the `install` process (potentially leveraging `list-rules` output obtained from the backend).
        *   An area to display the execution status and output from the `manage_rules.py` script, likely by streaming or linking to the dedicated Output Channel.
    *   Set up message passing between the Webview (frontend) and the extension's main process (backend) to handle button clicks and update the UI with script output.

4.  **Build GUI in View Container:**

4.  **Handle Script Output and Errors:**
    *   Parse the output of `manage_rules.py` to provide structured feedback to the user.
    *   Implement robust error handling for cases where the script fails or returns errors.

## Phase 3: Advanced Features and User Experience

1.  **Rule File Browsing and Selection:**
    *   (Optional, lower priority for POC) Implement functionality to help users browse and select rule files using VS Code's file picker API (`vscode.window.showOpenDialog`) for potential future commands or features.

2.  **Configuration:**
    *   Allow users to configure the path to the Python interpreter using VS Code's configuration API (`vscode.workspace.getConfiguration`). (Path to `manage_rules.py` is handled by bundling for POC).
    *   Implement any other necessary configuration options identified.

3.  **Context Menus (Optional):**
    *   (Optional for POC) Consider adding context menu items in the Explorer view for the workspace root to quickly access the main commands (e.g., "Install AI Rules Framework").

4.  **Status Bar Integration (Optional):**
    *   Display the current rule set being used in the VS Code status bar.

## Phase 4: Testing and Refinement

1.  **Unit Tests:**
    *   Write unit tests for the extension's core logic, including how it constructs and executes shell commands, and how it parses script output.

2.  **Integration Tests:**
    *   Write integration tests that simulate user interactions with the extension and verify that the correct `manage_rules.py` commands are executed and the expected output is processed.
    *   Consider using VS Code's Test Runner for extension testing.

4.  **Test GUI and User Flow:**
    *   Specifically test the functionality and user experience of the dedicated view container GUI. Verify that buttons trigger the correct commands, input fields/dropdowns work as expected, and output is displayed correctly.
    *   Refine the layout and interaction flow based on testing feedback.

5.  **Manual Testing:**
    *   Manually test all commands and features within a VS Code instance.
    *   Test on different operating systems.

4.  **Refine GUI and User Flow:**
    *   Based on testing feedback, refine the layout and interaction flow of the sidebar GUI for clarity and ease of use.

## Phase 5: Documentation and Publishing

1.  **Write README:**
    *   Create a comprehensive `README.md` file explaining the extension's purpose, features, installation instructions, usage, and configuration options.

2.  **Add Examples:**
    *   Provide simple examples demonstrating how to use the extension with common rule management tasks.

3.  **Prepare for Publishing:**
    *   Ensure the `package.json` contains all necessary information (name, version, description, publisher, categories, etc.).
    *   Review the VS Code Extension Marketplace guidelines.
    *   **Craft Marketplace Listing:** Prepare a compelling description, icon, and screenshots (demonstrating the GUI) for the VS Code Marketplace, explicitly highlighting the framework's benefits and linking to the GitHub repository to achieve the promotional goal.
    *   Ensure the `README.md` is also optimized for the Marketplace listing.

4.  **Publish to the VS Code Marketplace:**
    *   Use the `vsce` tool to package and publish the extension.

## Phase 6: Maintenance and Updates

1.  **Address User Feedback and Bug Reports:**
    *   Monitor the extension's GitHub repository for issues and feedback.
    *   Prioritize and fix bugs.

2.  **Implement New Features:**
    *   Based on user requests and the evolution of `manage_rules.py`, add new commands and features to the extension.

3.  **Maintain Compatibility:**
    *   Ensure the extension remains compatible with new versions of VS Code and `manage_rules.py`.

## Timeline (Estimate)
*   **Phase 1:** 1-2 days
*   **Phase 2:** 2-3 weeks (Includes core GUI and command wiring)
*   **Phase 3:** 1 week (Focus on secondary features/config)
*   **Phase 4:** 1-2 weeks
*   **Phase 5:** 1 week
*   **Phase 6:** Ongoing


This timeline is a rough estimate and may vary depending on the complexity of `manage_rules.py` and the features implemented in the extension.