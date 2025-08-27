# Prioritized Features & Tasks for Custom User Prompt Framework

This document outlines the prioritized features and tasks derived from the PRD, including dependencies, to guide development and implementation.

## Priority definition
P0 - Critical: Essential for the core value proposition and basic usability. Must be done first.

P1 - High: Highly important for achieving key goals or significantly enhancing usability.

P2 - Medium: Important for completeness, robustness, or supporting secondary goals.

P3 - Low: Nice-to-have; improves the experience but not essential for core function or initial goals.

## Core Features & Specific Tasks/Specs
*(refer @/tasks/task_plan.md for task status tracking)*

**1. Cross-Platform Compatibility & Rule Adaptation**

*   **1.a. Define Core Universal Rules:**
    *   **Priority:** P0
    *   **Dependencies:** None
    *   **Spec:** Identify foundational rules applicable across all target platforms (e.g., persona, core directive style).
*   **1.b. Develop Platform-Specific Rule Files:**
    *   **Priority:** P0
    *   **Dependencies:** 1.a
    *   **Spec:** Create individual rule files (`cursor_rules.json`, `cline_rules.yaml`, etc.) adapting core rules and adding platform specifics. *Initial focus on 1-2 key platforms might be pragmatic.*
*   **1.c. Document Platform Rule Differences:**
    *   **Priority:** P1
    *   **Dependencies:** 1.b
    *   **Spec:** Create documentation explaining syntax/behavior variations across platforms.
*   **1.d. Create Setup Guides:**
    *   **Priority:** P0
    *   **Dependencies:** 1.b
    *   **Spec:** Write clear, step-by-step instructions in README or SETUP.md for each supported platform.
*   **1.e. (Optional) Develop Setup Scripts:**
    *   **Priority:** P3
    *   **Dependencies:** 1.d
    *   **Spec:** Create helper scripts (shell, etc.) for easier installation.

**2. Latest Compatibility & Maintenance**

*   **2.a. Implement Semantic Versioning & Changelog:**
    *   **Priority:** P1
    *   **Dependencies:** Requires an initial version (e.g., after P0 tasks are done).
    *   **Spec:** Establish SemVer for the template repo. Create and maintain `CHANGELOG.md`.
*   **2.b. Define Compatibility Testing Process:**
    *   **Priority:** P2
    *   **Dependencies:** 1.b (Need rules to test)
    *   **Spec:** Outline steps (manual/automated) to verify rules against new platform versions.
*   **2.c. Document "Last Tested Versions":**
    *   **Priority:** P1
    *   **Dependencies:** 2.b (Requires testing to be done)
    *   **Spec:** Regularly update README/docs with tested platform versions.

**3. Minimal Token Usage & Efficiency**

*   **3.a. Design Modular Rule Structure:**
    *   **Priority:** P1
    *   **Dependencies:** 1.a, 1.b (Applies to how rules are structured)
    *   **Spec:** Organize rules into logical files/sections (style, debug, etc.) for selective loading if possible.
*   **3.b. Provide Rule Guidance for Context Prioritization:**
    *   **Priority:** P1
    *   **Dependencies:** 1.a, 4.a (Needs rules and Memory Bank structure)
    *   **Spec:** Include specific instructions within rules on how AI should selectively use Memory Bank info.
*   **3.c. Document Rule Writing Guidelines for Brevity:**
    *   **Priority:** P2
    *   **Dependencies:** 1.a
    *   **Spec:** Add a section to contribution/customization docs on writing concise rules.

**4. Common Memory Bank (Structure & Integration)**

*   **4.a. Define Standardized Memory Bank Document Templates:**
    *   **Priority:** P0
    *   **Dependencies:** None
    *   **Spec:** Create template files (`ARCHITECTURE.md`, `CODING_STYLE.md`, `TASK_TEMPLATE.md`, etc.) in `docs/` and `tasks/`.
*   **4.b. Write Specific Rules Integrating with Memory Bank:**
    *   **Priority:** P0
    *   **Dependencies:** 1.a, 4.a
    *   **Spec:** Create core rules instructing AI *when* and *how* to use `docs/` and `tasks/` content.
*   **4.c. Develop Task Context Management Rules:**
    *   **Priority:** P1
    *   **Dependencies:** 4.a, 4.b
    *   **Spec:** Add rules guiding AI to focus on an "active task" based on user input or context, referencing the relevant `tasks/TASK_ID.md`.

**5. Fundamental Software Engineering Principles (Integration & Guidance)**

*   **5.a. Create Phase-Specific Rule Modules/Sections:**
    *   **Priority:** P1
    *   **Dependencies:** 1.a, 4.b (Needs core rules and Memory Bank integration)
    *   **Spec:** Develop distinct rule sets for Planning, Implementation, Testing, Debugging, Documentation, Refactoring, linking them to Memory Bank usage. *Start with Planning & Implementation*.
*   **5.b. Include Optional Quality Gate Prompts/Rules:**
    *   **Priority:** P2
    *   **Dependencies:** 5.a
    *   **Spec:** Add examples or specific rules users can invoke for code review, plan critique, etc., referencing relevant Memory Bank docs.
*   **5.c. Integrate Basic Tool Usage Guidance:** *(New Section)*
    *   **Priority:** P1 (Collectively high importance for quality/efficiency)
    *   **Dependencies:** Requires tools (formatter, linter etc.) to be configured in the user's project. Relies on Phase-Specific Rules (5.a) for context on *when* to apply tools.
    *   **Spec:** Define rules instructing the AI on how and when to leverage common development tools configured within the project.
*   **5.c.i. Define Rules for Code Formatting:**
    *   **Priority:** P1
    *   **Dependencies:** 5.a (Implementation Phase)
    *   **Spec:** Add rules instructing the AI to assume a standard code formatter (e.g., Prettier, Black) is configured and to apply it to generated or modified code blocks. Example Rule: "After generating or modifying code, ensure it conforms to the project's standard formatter (assume Prettier/Black unless specified otherwise in `docs/CODING_STYLE.md`)."
*   **5.c.ii. Define Rules for Linting:**
    *   **Priority:** P1
    *   **Dependencies:** 5.a (Implementation/Debugging Phase), 5.c.i (Linting often runs after formatting)
    *   **Spec:** Add rules instructing the AI to check generated/modified code with the project's linter (e.g., ESLint, Flake8). Include guidance on interpreting and fixing reported errors/warnings, referencing `docs/CODING_STYLE.md` if needed. Example Rule: "After formatting, run the project's linter (e.g., ESLint/Flake8) on the changed code. Report critical errors and attempt to fix them based on linter messages and `docs/CODING_STYLE.md`."
*   **5.c.iii. Define Rules for Type Checking (If Applicable):**
    *   **Priority:** P1
    *   **Dependencies:** 5.a (Implementation/Debugging Phase), 5.c.ii (Often run after linting)
    *   **Spec:** For projects using static typing, add rules instructing the AI to run the type checker (e.g., tsc, MyPy) and address reported type errors. Example Rule: "If using TypeScript/Python with type hints, run the type checker (tsc/MyPy) after linting. Report and attempt to fix any type errors found."
*   **5.c.iv. Define Rules for Running Tests:**
    *   **Priority:** P1
    *   **Dependencies:** 5.a (Testing/Debugging Phase)
    *   **Spec:** Add rules instructing the AI on how to trigger the project's test suite (e.g., via npm test, pytest) and interpret the results (pass/fail). Example Rule: "After implementing a feature or fixing a bug as described in a task, run the project's test suite (e.g., `npm test` or `pytest`). Report if tests pass or fail. If they fail, analyze the output to help debug."
*   **5.c.v. Document Tool Configuration Assumption:**
    *   **Priority:** P1
    *   **Dependencies:** None (but supports all 5.c tasks)
    *   **Spec:** Clearly state in the main `README.md` or a dedicated `docs/SETUP.md` that the tool usage rules *assume* standard development tools (formatter, linter, type checker, test runner) are already configured correctly in the user's project environment (e.g., via `package.json`, `pyproject.toml`, `go.mod`, etc.). The rules guide the AI to *use* them, not configure them.

**6. User Customization & Extensibility**

*   **6.a. Document Customization Points:**
    *   **Priority:** P1
    *   **Dependencies:** 1.b, 4.a (Needs the core structure to be defined)
    *   **Spec:** Explain clearly *how* users can modify/extend rules and Memory Bank templates.
*   **6.b. Provide Example Use Cases/Scenarios:**
    *   **Priority:** P2
    *   **Dependencies:** Requires most P0/P1 features to be implemented to showcase them.
    *   **Spec:** Create 1-2 small example projects demonstrating the framework in action.

**7. Onboarding & Community Support**

*   **7.a. Comprehensive README and Quick Start Guide:**
    *   **Priority:** P0
    *   **Dependencies:** 1.d, 4.a (Needs setup info and basic structure explanation)
    *   **Spec:** Ensure README is clear, covers motive, setup, basic usage, structure. Include a Quick Start.
*   **7.b. Create Contribution Guidelines:**
    *   **Priority:** P1
    *   **Dependencies:** Requires a basic structure (P0 tasks) to contribute to.
    *   **Spec:** Develop `CONTRIBUTING.md` outlining contribution process.
*   **7.c. Set up Issue Templates:**
    *   **Priority:** P1
    *   **Dependencies:** None (Can be done anytime, but most useful once the repo is active)
    *   **Spec:** Configure GitHub issue templates for bugs and features.