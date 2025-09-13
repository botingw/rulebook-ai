[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Rulebook-AI: Universal Rules Template for AI Coding Assistants

* Bugs or ideas → open an **Issue** in the repo (run `rulebook-ai bug-report`)
* Rate or review rule sets → run `rulebook-ai rate-ruleset`
* See rule set reviews before installing → run `rulebook-ai list-rules` and follow the link
* Anonymous feedback: [Go to the Google Form](https://docs.google.com/forms/d/e/1FAIpQLSeW57QtPEWIRhHY1iOb8f5KQZTGLSeeb_PN2iZLd0Aw_pVYxw/viewform?usp=header)

## Quick Start with uv/uvx

```bash
# Install uv if you don't have it yet
curl -fsSL https://astral.sh/uv/install.sh | bash

# Install rulebook-ai in an ephemeral environment and add a pack
uvx rulebook-ai packs add light-spec
uvx rulebook-ai project sync  # apply pack contents to your workspace

# Or create a persistent environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
rulebook-ai doctor  # Check your setup
```

## Built-in Packs

Rulebook-AI ships with three packs that you can add to your project:

- **light-spec** – minimal guardrails for rapid prototyping.
- **medium-spec** – balanced guidelines for everyday development.
- **heavy-spec** – verbose, step-by-step rules for thorough reviews.

`rulebook-ai packs add <name>` copies the chosen pack into `.rulebook-ai/packs/` along with any bundled memory or tool starters. Run `rulebook-ai project sync` to copy those starters into `memory/` and `tools/` and to generate assistant-specific rules.

## Contributing Packs

Want to share your own pack? See the [Pack Developer Guide](memory/docs/features/community_packs/pack_developer_guide.md) for structure and publishing instructions. For hands-on help, add the built-in `pack-authoring-guide` (`rulebook-ai packs add pack-authoring-guide`) which walks you through converting rules into a pack and provides checklists and validation tools before submission.

## Supercharge Your AI Coding Workflow Across Cursor, CLINE, Claude Code, Codex CLI, Gemini CLI, Kilo Code, RooCode, Warp, Windsurf, and Github Copilot

Tired of inconsistent AI behavior across different coding assistants? Struggling to maintain context and enforce best practices on complex projects? This template provides a robust, cross-platform framework designed to elevate your AI pair-programming experience.

Leveraging established software engineering principles and a structured documentation system, this template ensures your AI assistants (like Cursor, CLINE, Claude Code, Codex CLI, Gemini CLI, Kilo Code, RooCode, Warp, Windsurf, and Github Copilot) operate consistently, understand your project deeply, and follow optimal workflows. Move beyond simple prototypes and build sophisticated applications with AI partners that truly understand your project's architecture, requirements, and history.

## Why Use This Template?

*   **Consistent AI Behavior:** Define clear workflows (Plan, Implement, Debug) and principles for your AI, ensuring predictable and high-quality output regardless of the platform used.
*   **Persistent Project Memory:** Implement a structured documentation system (`docs/`, `tasks/`) that acts as a shared "memory bank," providing deep context to the AI about requirements, architecture, technical decisions, and progress.
*   **Cross-Platform Compatibility:** Designed from the ground up to work seamlessly with Cursor, CLINE, Claude Code, Codex CLI, Gemini CLI, Kilo Code, RooCode, Warp, Windsurf, and Github Copilot, respecting their specific rule-loading mechanisms.
*   **Enforce Best Practices:** Integrate fundamental software engineering principles directly into the AI's instructions, promoting code quality, maintainability, and structured development.
*   **Reduced Setup Time:** Get started quickly with a pre-configured structure and ruleset, adaptable to your specific project needs.
*   **Optimized for Complex Projects:** The structured memory and workflow approach provides the necessary context and guidance for AI assistants working on more than just simple scripts or prototypes.

## Who Is This For?

This template is particularly beneficial for:

*   **Developers working on complex projects:** Requiring deep context and structured AI assistance beyond basic code generation.
*   **Teams using multiple AI coding assistants:** Ensuring consistency in workflow and AI behavior across different tools.
*   **Individuals seeking a more structured AI workflow:** Implementing proven software engineering practices for AI collaboration.
*   **Researchers needing reproducible AI interactions:** Providing a stable framework for experiments.
*   **Anyone looking to improve the quality and reliability of AI-generated code and documentation.**

## Key Features (Benefits-Focused)

1.  **Work Seamlessly Across Platforms:** Native support and configuration guidance for Cursor, CLINE, Claude Code, Codex CLI, Gemini CLI, Kilo Code, RooCode, Warp, Windsurf, and Github Copilot ensures your rules work consistently wherever you code.
2.  **Maintain Consistent AI Context:** The structured "Memory Bank" (core documentation files) provides deep, persistent context, reducing repetitive explanations and improving AI understanding.
3.  **Enforce Software Engineering Best Practices:** Guide your AI to follow established principles for planning, implementation, debugging, modularity, and testing.
4.  **Optimize Token Usage:** Rules are organized to leverage platform-specific loading mechanisms (where available) to minimize unnecessary token consumption.
5.  **Latest Compatibility:** Designed and tested with recent versions of the supported AI assistants.

## Quickstart: Using this Template for AI Coding


This template repository serves as the central source for master rule sets. To use these rules in your own projects, you'll utilize the `src/rulebook_ai/cli.py` script (or rulebook-ai command with 'pip install -e .') provided within *this* repository.

**Core Concepts:**

*   **Source Template Repo:** This repository, containing master rule sets (in `rule_sets/`), master memory bank starter documents (in `memory_starters/`), master tool starters (in `tool_starters/`), and the `src/rulebook_ai/cli.py` script (or rulebook-ai command with 'pip install -e .').
*   **Target Repo:** Your project repository (e.g., `~/git/my_cool_project`) where you want to use the rules.
*   **Target Project Rules Directory:** A folder named **`project_rules/`** created *inside your Target Repo* by the `install` command. It holds the specific rule files for *your* project, copied from a chosen set in the Source Template Repo's `rule_sets/` directory. This folder is used by the `sync` command and **removed by the `clean-rules` command**. It is managed by the script, though you can version control it for manual backups if desired.
*   **Target Memory Bank Directory:** A folder named **`memory/`** created *inside your Target Repo* during installation. It's populated with project-specific memory documents from the Source Template Repo's `memory_starters/` (new starter files are copied if they don't exist; existing files are **not** overwritten). **This folder should be version controlled in your Target Repo.**
*   **Target Tools Directory:** A folder named **`tools/`** created *inside your Target Repo* during installation. It's populated with utility scripts or configurations from the Source Template Repo's `tool_starters/` (new starter files/subdirectories are copied if they don't exist; existing files/subdirectories are **not** overwritten). **This folder should be version controlled in your Target Repo.**
*   **Target `env.example` and `requirements.txt`:** The `env.example` and `requirements.txt` files are copied from the Source Template Repo's root to *your Target Repo's root* during installation (non-destructively; existing files are preserved). **These files should be version controlled in your Target Repo.**
*   **Target Platform Rules:** Generated, platform-specific rule directories/files (e.g., `.cursor/rules/`, `.clinerules/`, `.roo/`, `.kilocode/`, `.windsurf/rules/`, `WARP.md`, `.github/copilot-instructions.md`, `CLAUDE.md`, `AGENTS.md`, `.gemini/GEMINI.md`) created *inside your Target Repo* by the `sync` command using `project_rules/` as input. **These folders/files should be added to your Target Repo's `.gitignore` file.**

**Workflow & Commands:**

*(Run these commands from your terminal, inside your checked-out copy of **this** `rules_template` repository)*

1.  **List Available Rule Sets (Optional):**
    *   Use the `list-rules` command to see which rule sets are available for installation from this Source Template Repo.
    *   **Note:** The command also prints a link to the ratings & reviews wiki so you can read feedback before installing.
    *   **Command:**
        ```bash
        rulebook-ai list-rules
        ```
    *   **Action:** Scans the `rule_sets/` directory in this repository and lists all available rule set names.

2.  **Install Rules and Framework Components into Your Project:**
    *   Use the `install` command to copy a chosen rule set, memory starters, and tool starters from this repo into your target project, and then perform an initial sync.
        * **NOTE** for windsurf user, after install rules, activate rules in GUI (see this [bug fix](https://github.com/botingw/rulebook-ai/issues/13#issuecomment-2911331241))
    *   **Command:**
        ```bash
        # Syntax: rulebook-ai install <path_to_your_target_repo> [--rule-set <rule_set_name>]
        # Example (using default 'light-spec' rule set):
        rulebook-ai install ~/git/my_cool_project
        # Example (specifying a rule set):
        rulebook-ai install ~/git/my_cool_project --rule-set heavy-spec
        ```
    *   **Action:**
        *   Copies the specified rule set (default: `light-spec`) from this repo's `rule_sets/<rule_set_name>/` to `~/git/my_cool_project/project_rules/`. (Overwrites `project_rules/` if it exists, with a warning).
        *   Copies content from this repo's `memory_starters/` to `~/git/my_cool_project/memory/` (non-destructively; existing files are preserved).
        *   Copies content from this repo's `tool_starters/` to `~/git/my_cool_project/tools/` (non-destructively; existing files/subdirectories are preserved).
        *   Copies `env.example` and `requirements.txt` from this repo's root to `~/git/my_cool_project/` (non-destructively; existing files are preserved).
        *   Automatically runs the `sync` command to generate the initial Target Platform Rules (e.g., `.cursor/rules/`, `.clinerules/`, `.roo/`, `.kilocode/`, `.windsurf/rules/`, `WARP.md`, `.github/copilot-instructions.md`, `CLAUDE.md`, `AGENTS.md`, `.gemini/GEMINI.md`) inside `~/git/my_cool_project/` based on the new `project_rules/`.
    *   **Follow Up:**
        *   Add the generated directories/files (e.g., `.cursor/`, `.clinerules/`, `.roo/`, `.kilocode/`, `.windsurf/`, `WARP.md`, `.github/copilot-instructions.md`, `CLAUDE.md`, `AGENTS.md`, `.gemini/GEMINI.md`) to your target project's (`~/git/my_cool_project/`) `.gitignore`.
        *   Commit the newly created/updated `memory/`, `tools/`, `env.example`, and `requirements.txt` files/directories within your target project.

# Sync (update) rules when rulebook-ai is updated
uvx rulebook-ai sync --rule-set light-spec --project-dir /path/to/your/project

# List available rule sets
uvx rulebook-ai list-rules

# Check your setup with the doctor command
uvx rulebook-ai doctor

# Clean up rules
uvx rulebook-ai clean-rules --project-dir /path/to/your/project

# Rate or review rule sets
uvx rulebook-ai rate-ruleset

# Report a bug in rulebook-ai
uvx rulebook-ai bug-report
```

### Using a Virtual Environment

For development or more persistent usage:

```bash
# Create and activate a virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install rulebook-ai in development mode
uv pip install -e .

# Now use the commands directly
rulebook-ai install --rule-set light-spec --project-dir /path/to/your/project
rulebook-ai sync --rule-set light-spec
rulebook-ai list-rules
```

### Start Coding with AI Assistants

Once rules are installed, use your AI coding assistants (Cursor, CLINE, Claude Code, Codex CLI, Gemini CLI, Kilo Code, RooCode, Warp, etc.) in your target project.

**Initial Prompt Suggestion (for setting up memory in a new project):**
> Using the project's custom rules, initialize the Memory Bank files (docs/, tasks/) based on the project's current state or initial requirements. Follow the structure and instructions defined in the rules for documenting project context.

6.  **Clean Up Rules (Preserving Memory & Tools):**
    *   To remove the generated Target Platform Rules and the `project_rules/` directory from your target project, while keeping your customized `memory/` and `tools/` directories intact, use the `clean-rules` command.
    *   **Command:**
        ```bash
        # Syntax: rulebook-ai clean-rules <path_to_your_target_repo>
        # Example:
        rulebook-ai clean-rules ~/git/my_cool_project
        ```
    *   **Action:** Removes `~/git/my_cool_project/project_rules/` and the generated rule directories/files (e.g., `.cursor/`, `.clinerules/`, `.roo/`, `.kilocode/`, `.windsurf/`, `WARP.md`, `.github/copilot-instructions.md`, `CLAUDE.md`, `AGENTS.md`, `.gemini/`). The `memory/` and `tools/` directories are **not** affected.

7.  **Clean Up All Framework Components (Full Uninstall):**
    *   To completely remove *all* framework components (Target Platform Rules, `project_rules/`, `memory/`, `tools/`, `env.example`, and `requirements.txt`) from your target project, use the `clean-all` command.
    *   **Important:** This command will prompt for confirmation because it removes `memory/`, `tools/`, `env.example`, and `requirements.txt`, which may contain your project-specific customizations.
    *   **Command:**
        ```bash
        # Syntax: rulebook-ai clean-all <path_to_your_target_repo>
        # Example:
        rulebook-ai clean-all ~/git/my_cool_project
        ```
    *   **Action:** After confirmation, removes `project_rules/`, `memory/`, `tools/`, `env.example`, `requirements.txt`, and all generated rule directories/files (e.g., `.cursor/`, `.clinerules/`, `.roo/`, `.kilocode/`, `.windsurf/`, `WARP.md`, `.github/copilot-instructions.md`, `CLAUDE.md`, `AGENTS.md`, `.gemini/`) from `~/git/my_cool_project/`.

### Environment Setup (Using Conda)

Before running the tools described in the rules, set up the Conda environment:

1.  **Create the environment:**
    ```bash
    conda create -n rules_template python=3.11 -y 
    ```
    *(Ensure you have Conda installed. We recommend Python 3.11, but adjust if needed.)*

2.  **Activate the environment:**
    ```bash
    conda activate rules_template
    ```
    *(You'll need to activate this environment in any terminal session where you intend to run the tools.)*

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install playwright:**
    ```bash
    playwright install
    ```
5.  **Configure your environment:**
    ```bash
    - Setup your API keys in `.env` (optional, check out rules_template/light-spec/01-rules/06-rules_v1.md for API tool context) 

With the environment set up and activated, you can run the Python tools as described in the rules files (e.g., `python tools/llm_api.py ...`).

## Rule Loading Summary (Based on Official Docs & Template Implementation)
For detail, go to [rule_loading_summary.md](memory/docs/user_guide/rule_loading_summary.md)

# Tips in General Using Cursor, CLINE, Claude Code, Codex CLI, Gemini CLI, Kilo Code, RooCode, Warp, Windsurf, and Github Copilot:
## CLINE/RooCode:
1. Every time you change Roo Code **mode** in the middle of an task, it changes the system prompt and reset the prompt caching.

# The Rules Template: Universal Rules for AI Coding Assistants 🔥 

This template provides a robust and adaptable framework of rules designed to enhance the performance of AI coding assistants like Cursor, CLINE, Claude Code, Codex CLI, Gemini CLI, Kilo Code, RooCode, Warp, Windsurf, and Github Copilot. Rooted in established software engineering principles and documentation best practices, it ensures consistent and effective AI-assisted development across different platforms.

For detail, go to [rule_template.md](memory/docs/user_guide/rule_template.md)

# Rule Files:

This template relies on a carefully orchestrated system of directories and files for Cursor, CLINE, Claude Code, Codex CLI, Gemini CLI, Kilo Code, RooCode, Warp, Windsurf, and Github Copilot. These components work together to provide a consistent and context-aware experience with your AI assistant. The **'rule' files** (e.g., `plan.md`, `implement.md`, `debug.md` found within a chosen rule set like `light-spec/`) are designed to define *how your AI should approach tasks*. They dictate specific workflows for planning, coding, or debugging, rooted in software engineering best practices. These rules guide the AI's *process* and operational methodology. The **'memory' files** and the `memory/
` directory structure (populated from `memory_starters/
` during installation) are designed to provide the AI with *persistent, structured knowledge about your specific project*. This includes its requirements (@`memory/docs/product_requirement_docs.md`), architecture (@`memory/docs/architecture.md`), ongoing tasks (@`memory/tasks/tasks_plan.md`), and learned information. This forms the AI's *contextual understanding* and long-term project "memory." Within each environment, there are crucial files that shape how the AI operates:

1. <strong>rules</strong> –
   Thois can house generic rules. Bring your own flavour to this minimal document. Below are three files: (a) plan, (b) implement, (c) debug, that defines workflows for these three tasks based on refining 100s of rule repositories and software engineering best practices:

2. <strong>plan</strong> – Defines the Workflow to be followed for any Planning based on *chain of thinking*. includes **exhaustive searching and optimal plan, rigourous reasoning and user validation**.
3. <strong>implement</strong> - Defines the Workflow to be followed for any Implementation. inspired by concepts like **seperation of concerns, modular design, and incremental development**. Has testing mandatory after every significant implementation.
4. <strong>debug</strong> - This file defines rules for debugging when stuck in a loop or a hard debugging. Supports looking at the web and for previously solved errors too.
5. <strong>memory</strong> –
   Next comes the recommended documentation. Software documentation starts with PRDs Recording the requirements, architecture plan, technical plan, and the RFCs for individual functionality or group of functionalities.
So our documentation that also served as a context is very relevant for an AI cod as it has mostly the knowledge and the skills to work on and with these proper software documentations.
6. <strong>directory-structure</strong> (directory-structure) –
   This is a very simple file stating the directory structure so that all parts of a project development is covered like : (a) code, (b) test, (c) configurations, (d) data, (e) project rules, etc separately and in modular approach.

In <strong>Cursor </strong>, these three files reside in <code>.cursor/rules</code>:

```bash
.cursor/rules/rules.mdc
.cursor/rules/plan.mdc
.cursor/rules/implement.mdc
.cursor/rules/debug.mdc
.cursor/rules/memory.mdc
.cursor/rules/directory-structure.mdc
```
In **CLINE**, this template uses the `clinerules/` directory for files intended for AI guidance (via `.clinerules`) or manual copy-paste into UI settings:
```bash
clinerules/
├── plan
├── implement
└── debug
# Plus the .clinerules file at the root for general project rules & AI mode guidance.
```
For **RooCode**, the *correct* structure (which this template needs to adopt - See To-Do #1) would be:
```bash
.roo/
├── rules/              # Workspace-wide rules (e.g., memory, dir-structure)
│   └── ...
├── rules-architect/    # Mode-specific rules (e.g., plan)
│   └── ...
├── rules-code/         # Mode-specific rules (e.g., implement)
│   └── ...
└── rules-debug/        # Mode-specific rules (e.g., debug)
    └── ...
```
For **Windsurf**, rules are generated in the `.windsurf/rules/` directory, with each rule as a separate `.md` file.
```bash
.windsurf/rules/
├── 01-example-rule.md
└── 02-another-rule.md
```

## Directory Structure: Modular Project Organization


The `directory-structure` files (located in `clinerules/directory-structure` and `cursor/rules/directory-structure.mdc`) define a clear and modular directory structure to organize project files logically. This structure promotes separation of concerns and enhances project maintainability. This is a very simple file stating the directory structure so that all parts of a project development is covered like : (a) code, (b) test, (c) configurations, (d) data, e.g. project rules, etc separately and in modular approach.

**Directory Structure Diagram:**

```mermaid
flowchart TD
    Root[Project Root]
    Root --> Docs[docs/]
    Root --> Tasks[tasks/]
    Root --> Cursor[.cursor/rules/]
    Root --> CLINE[.clinerules]
    Root --> SourceCode[src/]
    Root --> Test[test/]
    Root --> Utils[utils/]
    Root --> Config[config/]
    Root --> Data[data/]
    Root --> Other[Other Directories]
```

This structure ensures that different aspects of the project, such as code, tests, configurations, and documentation, are kept separate and well-organized.

## Advantages of Using the Rules Template

1.  **Cross-Platform Compatibility:** Usable seamlessly with Cursor, CLINE, Claude Code, Codex CLI, Gemini CLI, Kilo Code, RooCode, Warp, Windsurf, Github Copilot, and other AI coding assistants.
2.  **Context Sharing:** Enables context sharing and consistent workflows across different AI assistants, facilitating collaborative and platform-agnostic development.
3.  **Up-to-Date Compatibility:** Designed to be compatible with the latest versions of Cursor and CLINE, ensuring long-term usability.
4.  **Automated Documentation Generation:**  Provides the foundation for automatically generating comprehensive project documentation in PDF format, streamlining documentation efforts.
5.  **Amalgamation of Memory and Custom Prompts:** Combines the benefits of persistent project memory with customizable prompts (like `.clinerules/.cursorrules`) for a balanced approach to AI-assisted coding.
6.  **Foundation in Software Engineering Principles:** Built upon established software engineering and documentation best practices, ensuring a robust and reliable framework.
7.  **Precise Control and Flexibility:** Strikes a balance between providing precise guidance to LLMs and allowing for exploration and adaptability in problem-solving.
8.  **Adaptation of Traditional Software Engineering:** Bridges the gap between traditional software engineering methodologies and modern AI-assisted development.
9.  **Potential for Auto-Evolving Rules:**  Opens up possibilities for AI-driven rule evolution and refinement, allowing the template to adapt and improve over time.

By adhering to the principles and structure outlined in this Rules Template, development teams can leverage AI coding assistants more effectively, ensuring consistency, quality, and maintainability across their projects.

## Additional Notes:

1. **Product Requirements Documents (PRDs):** PRDs serve multiple purposes: defining product scope and goals, aligning stakeholders across teams, and mitigating risks early in development. They offer significant utility by providing clarity on product vision, prioritizing features, ensuring quality, and enabling traceability throughout the development lifecycle . While traditionally detailed in Waterfall, PRDs are adapted for Agile methodologies as leaner, iterative documents. Related documents include Market Requirements Documents (MRDs) and Functional Requirements Documents (FRDs).
2. **Architecture Documentation:** It serves to preserve design rationale, support scalability, and facilitate decision-making. Key benefits include improved knowledge sharing, risk mitigation, and stakeholder communication. Types of architecture documentation vary, including decision-centric ADRs, structural C4 model diagrams, and behavioral sequence diagrams. Frameworks like arc42 provide structured templates for comprehensive architecture documentation.
3. **Technical Specifications:** Technical Specifications Documents (TSDs) serve as blueprints translating business needs into technical guidelines. They clarify project vision, bridge stakeholder communication, and mitigate risks. TSDs are highly useful for engineers as step-by-step guides, for teams as alignment tools, and for projects in ensuring accountability. Technical documentation broadly includes process documentation (user manuals, API docs), and specialized specs for IT or Agile projects. A robust TSD enhances project clarity and reduces failure risks associated with unclear requirements.
4. **RFCs (Request for Comments):** Request for Comments (RFCs) are structured proposals for technical decision-making and standardization. They document technical specifications, solicit feedback, and preserve institutional knowledge. RFCs enhance utility by reducing silos, mitigating risks, and ensuring decision traceability. Types range from standards-track protocol specifications to organizational RFCs for team-specific designs. Modern RFCs often include problem statements, proposed solutions, alternatives, rollout plans, and security impact assessments. While RFCs improve decision quality, they also pose challenges like time overhead and consensus bottlenecks.