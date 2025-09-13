# Heavy-Spec Pack

Heavy-Spec is the most detailed and prescriptive ruleset in the Rulebook-AI collection. It provides maximum guardrails and explicit workflow steps for rigorous, large-scale projects.

## When to Choose Heavy-Spec

- Large, complex projects requiring maximum rigor and traceability.
- Teams new to human-AI collaboration needing strong guardrails.
- Situations involving less capable AI models that benefit from explicit instructions.
- Projects with strict compliance or validation requirements.
- When predictability and detailed process adherence are paramount.

If you need less overhead, consider the `medium-spec` or `light-spec` packs.

## Pack Structure

- `rules/`: core instruction files such as `00-meta-rules.md`, `06-rules_v1.md`, and workflow guides for planning, coding, and debugging.
- `memory_starters/`: starter documents that seed the persistent project memory bank.
- `tool_starters/`: helper scripts or configurations copied into your project.

## Installation & Usage

```bash
# Add this built-in pack to your project's library
uvx rulebook-ai packs add heavy-spec --project-dir /path/to/your/project

# Apply the pack and generate assistant-specific rule files
uvx rulebook-ai project sync --assistant cursor --project-dir /path/to/your/project
```

Add `memory/`, `tools/`, `env.example`, and `requirements.txt` to version control. Framework state in `.rulebook-ai/` and generated rule directories (e.g., `.cursor/`, `.clinerules/`, `.roo/`) should go in `.gitignore`.

## Key Concepts & Prompting Tips

- **`.rulebook-ai/`** – internal framework state. After `project sync`, local copies of pack rules live in `.rulebook-ai/packs/` and are regenerated as needed.
- **`memory/`** – persistent, user-owned documents (PRD, architecture, technical specs, task plans) that the AI can read and update.
- **File references** – point your assistant at files using its reference syntax (e.g., `@memory/docs/product_requirement_docs.md`).

### Prompt Patterns

- **Planning** – ask the AI to update tasks or docs.  
  _Example:_ "Add a 'Refactor Auth' task to @memory/tasks/tasks_plan.md with a short description."
- **Context lookup** – query the AI about project decisions or status.  
  _Example:_ "What database did we choose in @memory/docs/architecture.md?"
- **Implementation guidance** – request code while referencing rules and memory.
  _Example:_ "Follow @.rulebook-ai/packs/heavy-spec/rules/03-rules-code/01-code_v1.md to build the login flow described in @memory/tasks/active_context.md."

## Plan/Implement/Debug: Systematic Workflow for Tasks

The rule files cached in `.rulebook-ai/packs/heavy-spec/rules/` define a structured workflow for approaching any development task, regardless of granularity. This workflow is based on standard software engineering best practices and promotes a systematic approach to problem-solving.

## Five-Phased Workflow

Heavy-Spec encodes a five-phased approach to software development. The phases correspond to the planning, coding, and debugging rules in `rules/02-rules-architect`, `rules/03-rules-code`, and `rules/04-rules-debug`.

**(i) Requirements and Clarifications:**

   it starts with making the requirements very clear and asking as much clarification as possible in the beginning. This is always the first task software development. Where all the requirements are made as precise and verbose as possible so as to save Time and effort later in redoing. Plus anticipate Major bottlenecks ahead of any work.

**(ii) Exhaustive Searching and Optimal Plan:**
  exhaustive searching and optimal plan: search all possible directions in which the problem can be solved. And find out the optimal solution, which can be also a amalgamation of many different approaches. And reason rigourously, why the chosen approach is optimal.

**(iii) User Validation:**

  validate the developed optimal plan with the user clearly stating the assumptions and design decisions made, and the reasons for them.

**(iv) Implementation:**

   implement proposed plan in an iterative way, taking one functionality at a time, testing it exhaustively with all the cases. And then building the next functionality. In this way to make the system, robust and incremental.

**(v) Further Suggestions:**

   after implementation, suggesting possible optimisation to be done or possible, additional features for security or functionality to be added.

So this five phased approach, is for a software life-cycle. But this can be applied for any grnuarlity, like entire project or a single functionality. For example, very clearly recording the requirement for the functionality and asking clarifying questions is as good for a single small functionality as for a program. So this five phased, solution strategy workflow is to be followed at every part of development.

## Leveraging Your AI's Enhanced Brain: Example Interactions

Once Rulebook-AI is set up with a chosen pack (cached under `.rulebook-ai/`) and the memory bank (in `memory/`), you can interact with your AI coding assistant much more effectively. Here are a few crucial examples of how to leverage this enhanced context and guidance. Remember to use your AI assistant's specific syntax for referencing files (e.g., `@filename` in Cursor or Copilot).

1.  **Maintain Project Structure & Planning:**
    *   **Goal:** Use the AI to help keep your project documentation and task lists up-to-date.
    *   **Example Prompt (in your AI chat):**
        ```
        Based on section 3.2 of @memory/docs/product_requirement_docs.md, create three new tasks in @memory/tasks/tasks_plan.md for the upcoming 'User Profile Redesign' feature. For each task, include a brief description, assign it a unique ID, and estimate its priority (High/Medium/Low).
        ```
    *   **Why this is important:** This demonstrates the AI actively participating in project management by updating the "memory bank" itself. It ensures your planning documents stay synchronized with insights derived from foundational requirements, turning the AI into a proactive assistant beyond just code generation.
2.  **Retrieve Context-Specific Information Instantly:**
    *   **Goal:** Quickly access key project details without manually searching through documents.
    *   **Example Prompt (in your AI chat):**
        ```
        What is the current status of task 'API-003' as listed in @memory/tasks/tasks_plan.md? Also, remind me which database technology we decided on according to @memory/docs/architecture.md.
        ```
    *   **Why this is important:** This highlights the power of the "persistent memory bank." The AI acts as a knowledgeable team member, capable of quickly recalling specific project decisions, technical details, and task statuses, significantly improving your workflow efficiency.
3.  **Implement Features with Deep Context & Guided Workflow:**
    *   **Goal:** Guide the AI to develop code by following defined procedures and referencing precise project context.
    *   **Example Prompt (in your AI chat):**
        ```
        Using the workflow defined in @.rulebook-ai/packs/heavy-spec/rules/03-rules-code/01-code_v1.md, please develop the `updateUserProfile` function. The detailed requirements for this function are specified under the 'User Profile Update' task in @memory/tasks/active_context.md. Ensure the implementation aligns with the API design guidelines found in @memory/docs/technical.md.
        ```
    *   **Why this is important:** This is the core development loop where Rulebook-AI shines. It shows the AI leveraging both the *procedural rules* (how to approach implementation, from `.rulebook-ai/packs/`) and the rich *contextual memory* (what to implement and its surrounding technical landscape, from `memory/`). This leads to more accurate, consistent, and context-aware code generation, reducing rework and improving quality.

These examples illustrate how providing structured rules and a persistent memory bank allows for more sophisticated and productive interactions with your AI coding assistant. Experiment with referencing different files from your `.rulebook-ai/packs/` and `memory/` directories to best suit your workflow.

## Memory: Persistent Project Documentation

The `memory` files (located in `clinerules/memory` and `cursor/rules/memory.mdc`) establish a robust documentation system that serves as persistent memory for the project and the AI assistant. This system is inspired by standard software development documentation practices, including PRDs, architecture plans, technical specifications, and RFCs. So, keeping these software life-cycle documentation is as focus. We develop our memory bank to have these document in sync to provide the complete context for the project. We have few additional files for current context and task plan in tasks/.

**Memory Files Structure:**

The memory system is structured into Core Files (required) and Context Files (optional), forming a hierarchical knowledge base for the project.
```mermaid
flowchart TD
    PRD[product_requirement_docs.md] --> TECH[technical.md]
    PRD --> ARCH[docs/architecture.md]

    ARCH --> TASKS[tasks/tasks_plan.md]
    TECH --> TASKS
    PRD --> TASKS

    TASKS --> ACTIVE[tasks/active_context.md]

    ACTIVE --> ERROR[.cursor/rules/error-documentation.mdc]
    ACTIVE --> LEARN[.cursor/rules/lessons-learned.mdc]

    subgraph LIT[docs/literature]
        L1[Research 1]
        L2[Research 2]
    end

    subgraph RFC[tasks/rfc]
        R1[RFC 1]
        R2[RFC 2]
    end

    TECH --o LIT
    TASKS --o RFC

```

**Core Files (Required):**

1.  **`product_requirement_docs.md` (docs/product_requirement_docs.md):** Product Requirement Document (PRD) or Standard Operating Procedure (SOP).
    - Defines the project's purpose, problems it solves, core requirements, and goals.
    - Serves as the foundational document and source of truth for project scope.

    Product Requirement Documents (PRDs) are foundational blueprints in software development, defining what a product should achieve and guiding teams to align on scope, features, and objectives .

2.  **`architecture.md` (docs/architecture.md):** System Architecture Document.
    - Outlines the system's design, component relationships, and dependencies.

    Software architecture documentation is a blueprint that captures design decisions, component interactions, and non-functional requirements.

3.  **`technical.md` (docs/technical.md):** Technical Specifications Document.
    - Details the development environment, technologies used, key technical decisions, design patterns, and technical constraints.

4.  **`tasks_plan.md` (tasks/tasks_plan.md):** Task Backlog and Project Progress Tracker.
    - Provides an in-depth list of tasks, tracks project progress, current status, and known issues.

5.  **`active_context.md` (tasks/active_context.md):** Active Development Context.
    - Captures the current focus of development, active decisions, recent changes, and next steps.

6.  **`error-documentation.mdc` (.cursor/rules/error-documentation.mdc):** Error Documentation.
    - Documents reusable fixes for mistakes and corrections, serving as a knowledge base of known issues and resolutions.

7.  **`lessons-learned.mdc` (.cursor/rules/lessons-learned.mdc):** Lessons Learned Journal.
    - A project-specific learning journal that captures patterns, preferences, and project intelligence for continuous improvement.

**Context Files (Optional):**

**NOTE**: I use LATEX, but you can use .md or any other format.
1.  **`docs/literature/`:** Literature Survey and Research Directory.
    - Contains research papers and literature surveys in LaTeX format (`docs/literature/*.tex`).

2.  **`tasks/rfc/`:** Request for Comments (RFC) Directory.
    - Stores RFCs for individual tasks in LaTeX format (`tasks/rfc/*.tex`), providing detailed specifications and discussions for specific functionalities.

**Additional Context:**

Further files and folders can be added within `docs/` or `tasks/` to organize supplementary documentation such as integration specifications, testing strategies, and deployment procedures.
