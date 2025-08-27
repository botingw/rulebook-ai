# VS Code Extension Feature Specification: AI Rule Manager

## 1. Overview
This document specifies the features and user experience of a Visual Studio Code extension that provides a graphical interface and command palette access to the functionality of the `manage_rules.py` script. The extension will allow users to easily manage AI coding assistant rule sets and project memory within their VS Code workspace.

A key purpose of this extension is to serve as a primary discovery and installation channel for the associated AI Rule Management Framework GitHub repository. By providing a convenient, IDE-integrated installation method, the extension aims to promote the framework and make it easily accessible to VS Code users seeking enhanced AI coding assistance.
This extension is intended as a Proof-of-Concept (POC) to gauge the effectiveness of the VS Code Marketplace as a promotional tool for the framework, focusing on core functionality over extensive UI complexity in the initial version.

## 2. User Stories

*   As a developer, I want to easily install the AI rule management framework into my project directly from VS Code.
*   As a developer, I want to synchronize my project's custom rules to generate the platform-specific rule files for my AI assistant without leaving VS Code.
*   As a developer, I want to clean up the generated and temporary rule files within my project using a simple VS Code command.
*   As a developer, I want to completely remove the AI rule management framework components from my project via a clear command in VS Code.
*   As a developer, I want to see which rule sets are available in the framework's source repository directly within VS Code.

## 2.1 Alternative Promotion Approaches
Beyond the VS Code extension, other potential avenues for promoting the framework and its repository include exploring integration with other IDEs, developing a simple web-based demo or playground, and seeking partnerships with the developers of supported AI coding assistants. These approaches could broaden the framework's reach and visibility.


## 3. Commands

The extension will expose the following commands via the VS Code Command Palette (accessible with `Ctrl+Shift+P` or `Cmd+Shift+P`). Each command will operate on the currently active VS Code workspace folder.

### 3.1. AI Rule Manager: Install Framework

*   **Command ID:** `aiRuleManager.installFramework`
*   **Description:** Installs the AI rule management framework into the current workspace folder. This includes copying a chosen rule set, memory bank starters, tool starters, `env.example`, and `requirements.txt`. It then performs an initial synchronization.
*   **Invocation:** Command Palette -> "AI Rule Manager: Install Framework"
*   **Behavior:**
    *   Prompts the user to select an available rule set (listing options discovered by `manage_rules.py list-rules`). Defaults to `light-spec`.
    *   Executes `python manage_rules.py install <workspace_path> --rule-set <chosen_rule_set>`.
    *   Displays progress and output from the script in the VS Code Output pane (e.g., under a dedicated "AI Rule Manager" channel).
    *   Notifies the user upon completion, including important post-installation steps (like adding generated files to `.gitignore` and committing project-specific files).
    *   Handles potential errors during installation and reports them to the user via notifications or the Output pane.

### 3.2. AI Rule Manager: Sync Rules

*   **Command ID:** `aiRuleManager.syncRules`
*   **Description:** Synchronizes the platform-specific rule files based on the source rules in the `project_rules/` directory within the current workspace folder.
*   **Invocation:** Command Palette -> "AI Rule Manager: Sync Rules"
*   **Behavior:**
    *   Executes `python manage_rules.py sync <workspace_path>`.
    *   Displays progress and output in the VS Code Output pane.
    *   Notifies the user upon successful completion or reports errors.
    *   Should ideally confirm that the `project_rules/` directory exists before running, warning the user if it's missing.

### 3.3. AI Rule Manager: Clean Rules

*   **Command ID:** `aiRuleManager.cleanRules`
*   **Description:** Removes generated platform-specific rule files and the `project_rules/` source directory from the current workspace folder.
*   **Invocation:** Command Palette -> "AI Rule Manager: Clean Rules"
*   **Behavior:**
    *   Executes `python manage_rules.py clean-rules <workspace_path>`.
    *   Displays progress and output in the VS Code Output pane.
    *   Notifies the user upon successful completion or reports errors.
    *   Should ideally confirm with the user before proceeding, as this deletes user-modifiable files within `project_rules/`. A simple confirmation dialog ("Are you sure you want to remove rule files?") should suffice.

### 3.4. AI Rule Manager: Clean All

*   **Command ID:** `aiRuleManager.cleanAll`
*   **Description:** Removes all AI rule management framework components (`project_rules/`, `memory/`, `tools/`, generated rules, `env.example`, `requirements.txt`) from the current workspace folder.
*   **Invocation:** Command Palette -> "AI Rule Manager: Clean All"
*   **Behavior:**
    *   Presents a prominent confirmation dialog to the user, explicitly stating which directories (`memory/`, `tools/`) and files (`env.example`, `requirements.txt`) containing user-managed content will be deleted and requiring explicit confirmation ("yes").
    *   If confirmed, executes `python manage_rules.py clean-all <workspace_path>`.
    *   Displays progress and output in the VS Code Output pane.
    *   Notifies the user upon successful completion or reports errors.

### 3.5. AI Rule Manager: List Available Rule Sets

*   **Command ID:** `aiRuleManager.listRuleSets`
*   **Description:** Lists the names of available rule sets in the source framework repository.
*   **Invocation:** Command Palette -> "AI Rule Manager: List Available Rule Sets"
*   **Behavior:**
    *   Executes `python manage_rules.py list-rules`.
    *   Displays the output (the list of rule set names) in the VS Code Output pane.
    *   Should ideally also display the list in a quick pick dialog for easier readability.

## 4. UI Elements

*   **Output Channel:** A dedicated output channel named "AI Rule Manager" will display the console output from the executed `manage_rules.py` script for all commands.
*   **Dedicated View Container (Sidebar Panel):** This is the primary intended interface for the POC. The extension will provide a sidebar panel where users can interact with the core commands (`Install`, `Sync`, `Clean Rules`, `Clean All`). This panel will feature:
    *   Buttons or simple interactive elements for triggering each command.
    *   An input field or dropdown for selecting the rule set during the `Install` command.
    *   A dedicated area (potentially integrated with or linking to the Output Channel) to display the execution status and output of the commands.
    *   The design should prioritize functionality and clarity for the POC rather than complex or highly polished visuals. The goal is to provide a more discoverable and intuitive alternative to the Command Palette for the primary user interactions.
*   **Status Bar Item (Optional for POC, likely for future):** A status bar item could indicate if the framework is installed in the current workspace and potentially offer quick access to the view container or `sync`.
*   **Context Menus (Optional for POC, likely for future):** Add context menu items in the Explorer view for the workspace root to quickly access the commands (e.g., "Install AI Rules", "Sync AI Rules").

## 5. Configuration

The extension will need to locate the `manage_rules.py` script and the associated framework directories (`rule_sets`, `memory_starters`, `tool_starters`). For the POC, a simple approach is assumed:

*   **Bundled Script and Files:** The `manage_rules.py` script and the necessary source directories (`rule_sets`, `memory_starters`, `tool_starters`, `env.example`, `requirements.txt`) will be packaged directly within the extension's VSIX file. The extension will locate these resources relative to its installation directory.

For future releases, more flexible configuration might be considered:

*   **`aiRuleManager.frameworkRepoPath`:** (Future consideration) Allows users to specify the path to the source AI Rule Framework repository if it's not the current workspace or bundled within the extension package. This would likely be an advanced setting.

Regardless of how the framework files are located, the extension should allow configuring the Python interpreter:


The extension may offer configuration options in VS Code settings:

*   **`aiRuleManager.pythonPath`:** Allows users to specify the path to the Python interpreter used to run `manage_rules.py`. Defaults to the system's default Python or the one selected by the Python extension if available.
*   **`aiRuleManager.frameworkRepoPath`:** (Less likely needed if the extension is part of the framework repo itself, but useful for external installation) Allows users to specify the path to the source AI Rule Framework repository if it's not the current workspace. This would likely be an advanced setting.


## 7. Error Handling

The extension should capture `stderr` from the executed `manage_rules.py` script and display it prominently in the Output pane. Notifications should alert the user to command failures.

## 8. Future Enhancements (Out of Scope for Initial Release)

*   Refinement of the GUI with better visual feedback, progress indicators, and structured output display within the view container.
*   Configuration options for framework location if not bundled.
*   Enhanced handling of the target repository path (e.g., supporting multi-root workspaces, explicitly prompting the user if no workspace is open).
*   More robust validation of inputs (like rule set names).


*   UI for configuring specific rules within `project_rules/`.
*   Watcher to automatically run `sync` when files in `project_rules/` are modified.
*   Integration with Git status to indicate if generated files are untracked or committed (reminding user of `.gitignore`).
*   More detailed reporting or logging within the VS Code environment.
*   Support for multi-root workspaces.