# VS Code Extension Task Plan: `manage_rules.py` Wrapper

This document outlines a task plan for developing the VS Code extension based on the `vscode_extension_plan.md` file. The plan is broken down into phases, tasks, and subtasks, with estimated timelines for each phase.

This plan is designed to be easily modified and extended. Additional context for specific tasks or subtasks can be added in separate Markdown files within subdirectories to keep this main plan concise.

## Phase 1: Setup and Basic Implementation (Estimate: 1-2 days)

- Task 1.1: Set up VS Code Extension Development Environment
    - State: In progress
    - Description: Install necessary tools and generate the basic extension project structure.
    - Subtasks:
        - [x] Install Node.js and npm
        - [x] Install the VS Code Extension Generator (`yo code`)
        - [ ] Generate a new TypeScript or JavaScript extension project using `yo code`
        - [ ] Familiarize with the extension project structure (`package.json`, `extension.ts`)
    - Context: See ./task_1_1/ for detailed steps and notes.

- Task 1.2: Integrate `manage_rules.py`
    - State: Completed
    - Description: Determine how to execute the Python script from the extension and ensure its accessibility.
    - Subtasks:
        - [ ] Determine the best way to execute the Python script from Node.js/TypeScript (e.g., `child_process.exec`, `spawn`)
        - [ ] Ensure the Python script is accessible to the extension (e.g., plan for bundling or user-specified path)
    - Context: See ./task_1_2/ for detailed steps and notes.

- Task 1.3: Implement a Basic Command # This is a new line for task 1.3
    - State: In progress
    - Description: Create and register a simple command in VS Code to execute `manage_rules.py` and display its output.
    - Subtasks:
        - [x] Define a simple command in `package.json` (e.g., `aiRuleManager.listRuleSets`)
        - [ ] Register the command in `extension.ts`
        - [ ] In the command handler, execute `manage_rules.py` with a basic argument (e.g., `list-rules`)
        - [ ] Display the output in a VS Code output channel

## Phase 2: GUI and Core Command Implementation (POC Focus) (Estimate: 2-3 weeks)
    - State: In progress

- [ ] Task 2.1: Identify Key `manage_rules.py` Functionality
- Task 2.1: Identify Key `manage_rules.py` Functionality for POC
    - State: To do
    - Description: Review the `manage_rules.py` script to understand its core commands and arguments to be exposed in the extension.
    - Subtasks:
        - [ ] Subtask 2.1.1: Review the `manage_rules.py` script to understand its core commands and arguments: `install`, `sync`, `clean-rules`, `clean-all`, `list-rules`.

- [ ] Task 2.2: Create Dedicated View Container (Sidebar) and Define Commands
    - State: To do
    - [ ] Subtask 2.2.1: Define and register a new View Container and View in `package.json`
    - [ ] Subtask 2.2.2: For each core function, define a corresponding VS Code command in `package.json`
- [ ] Task 2.3: Implement Command Handlers
    - State: In progress
    - [ ] Subtask 2.3.1: Register handlers for each command in `extension.ts`
    - [ ] Subtask 2.3.3: Use VS Code APIs for user interaction (notifications, input boxes)

- [ ] Task 2.4: Build GUI in View Container (Webview)
    - [ ] Subtask 2.4.1: Implement HTML, CSS, and JavaScript for the Webview UI
    - [ ] Subtask 2.4.2: Add buttons for `install`, `sync`, `clean-rules`, `clean-all`
    - [ ] Subtask 2.4.3: Add input/dropdown for rule set selection during `install` (possibly using `list-rules` output)
    - [ ] Subtask 2.4.4: Add an area to display execution status and output (linking to Output Channel)
    - [ ] Subtask 2.4.5: Set up message passing between Webview and extension backend

- [ ] Task 2.5: Handle Script Output and Errors
    - [ ] Subtask 2.5.1: Parse script output for structured feedback
    - [ ] Subtask 2.5.2: Implement robust error handling and reporting using VS Code APIs

## Phase 3: Advanced Features and User Experience (Estimate: 1 week)

- [ ] Task 3.1: Rule File Browsing and Selection (Optional for POC)
    - [ ] Subtask 3.1.1: (If implemented) Use `vscode.window.showOpenDialog` for file selection

- [ ] Task 3.2: Configuration
    - [ ] Subtask 3.2.1: Allow configuring Python interpreter path using `vscode.workspace.getConfiguration`
    - [ ] Subtask 3.2.2: Implement other necessary configuration options identified

- [ ] Task 3.3: Context Menus (Optional for POC)
    - [ ] Subtask 3.3.1: (If implemented) Add context menu items in the Explorer view

- [ ] Task 3.4: Status Bar Integration (Optional)
    - [ ] Subtask 3.4.1: (If implemented) Display current rule set in status bar

## Phase 4: Testing and Refinement (Estimate: 1-2 weeks)

- [ ] Task 4.1: Write Unit Tests
    - [ ] Subtask 4.1.1: Test core logic (command construction, execution, output parsing)

- [ ] Task 4.2: Write Integration Tests
    - [ ] Subtask 4.2.1: Simulate user interactions
    - [ ] Subtask 4.2.2: Verify script execution and output processing
    - [ ] Subtask 4.2.3: Consider using VS Code's Test Runner

- [ ] Task 4.3: Test GUI and User Flow
    - [ ] Subtask 4.3.1: Test button functionality and command triggering
    - [ ] Subtask 4.3.2: Test input fields/dropdowns
    - [ ] Subtask 4.3.3: Verify output display

- [ ] Task 4.4: Manual Testing
    - [ ] Subtask 4.4.1: Manually test all commands and features in VS Code
    - [ ] Subtask 4.4.2: Test on different operating systems

- [ ] Task 4.5: Refine GUI and User Flow
    - [ ] Subtask 4.5.1: Based on testing feedback, refine GUI layout and interaction

## Phase 5: Documentation and Publishing (Estimate: 1 week)

- [ ] Task 5.1: Write README
    - [ ] Subtask 5.1.1: Document purpose, features, installation, usage, configuration

- [ ] Task 5.2: Add Examples
    - [ ] Subtask 5.2.1: Provide examples for common rule management tasks

- [ ] Task 5.3: Prepare for Publishing
    - [ ] Subtask 5.3.1: Ensure `package.json` is complete
    - [ ] Subtask 5.3.2: Review Marketplace guidelines
    - [ ] Subtask 5.3.3: Craft Marketplace listing (description, icon, screenshots)
    - [ ] Subtask 5.3.4: Optimize `README.md` for Marketplace

- [ ] Task 5.4: Publish to the VS Code Marketplace
    - [ ] Subtask 5.4.1: Use `vsce` tool to package and publish

## Phase 6: Maintenance and Updates (Estimate: Ongoing)

- [ ] Task 6.1: Address User Feedback and Bug Reports
    - [ ] Subtask 6.1.1: Monitor GitHub repository for issues
    - [ ] Subtask 6.1.2: Prioritize and fix bugs

- [ ] Task 6.2: Implement New Features
    - [ ] Subtask 6.2.1: Add new commands/features based on requests and script evolution

- [ ] Task 6.3: Maintain Compatibility
    - [ ] Subtask 6.3.1: Ensure compatibility with new VS Code and `manage_rules.py` versions

## Notes:
- This plan is a living document and can be updated as development progresses.
- For more detailed context on specific tasks, create subdirectories (e.g., `memory/docs/features/vscode_extension/tasks/phase_2_gui_context/`) and add Markdown files within them. Link to these files from the relevant tasks/subtasks above if necessary.
