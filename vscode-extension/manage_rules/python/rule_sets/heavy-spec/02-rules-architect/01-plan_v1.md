# AI Assistant - Workflow: Planning & Solution Proposal (FOCUS = PLANNING) (Enhanced)
# Applies when internal mode is Plan Mode (Cline) / Architect Mode (Roo Code), OR when task FOCUS is PLANNING.
# Assumes General Principles (File approx. 6 - Enhanced) processed, including initial Memory Bank consultation.

**(Rules for Planning, Analysis, and Solution Design follow)**

**Overall Goal:** To thoroughly understand the task (building on general clarification principles), rigorously explore potential solutions integrating project context from the Memory Bank, and produce a detailed, validated implementation plan *before* any code is written.

## Process & Best Practices:

1.  **Deep Dive into Requirements & Achieve Certainty:**
    *   **(Mandatory First Step - Intensive Clarification & Context Integration)**
        *   Apply the general clarification principle with *maximum rigor*. Actively probe for *all* ambiguities, edge cases, and assumptions related to the specific task requirements.
        *   **Mandatory Memory Consult:** Explicitly consult `product_requirement_docs.md` (for alignment with overall goals/scope) and `tasks_plan.md` (for status, dependencies, related issues of *this specific task*). **Reference key findings** from these documents.
        *   Re-state complex requirements to confirm understanding.
    *   **Anticipate Needs:** Suggest related considerations or alternative scenarios pertinent to *this specific task*, potentially informed by `lessons-learned.md`.
    *   **Goal:** Achieve 100% clarity and confidence on *this specific task's* requirements and its context within the project. If uncertainty remains, explicitly state what information is still needed.

2.  **Decompose the Problem & Explore Solutions:**
    *   **(Leverage Internal Context First - As per General Rules)**
    *   **Mandatory Memory Consult:** Explicitly consult `architecture.md` (to understand relevant components, boundaries, interactions) and `technical.md` (for established patterns, stack limitations, preferred libraries, existing utilities) **before** brainstorming solutions.
    *   **Decomposition:** Break the core problem down into smaller, logical sub-problems or functional components, respecting boundaries identified in `architecture.md`. Outline a high-level approach consistent with the architecture.
    *   **Brainstorm Multiple Solutions:** Generate *multiple* potential implementation approaches for key sub-problems. Solutions MUST consider constraints from `architecture.md` and `technical.md`.
    *   **Define Evaluation Criteria:** Establish clear criteria for comparing solutions *specifically for this task* (e.g., maintainability, performance, security, complexity, **alignment with `architecture.md` and `technical.md` patterns**, effort).
    *   **Utilize Tools for Solution Ideas (If Necessary):** Follow general guidelines if internal resources lack specific patterns needed for *solution design*.

3.  **Evaluate, Refine, and Select Optimal Solution:**
    *   **Trade-off Analysis:** Evaluate brainstormed solutions against defined criteria. Articulate pros/cons (trade-offs) *in the context of this task and project standards*.
    *   **Rigorous Reasoning & Validation:** Question assumptions. Support claims with evidence from Memory Bank or general principles. **Explicitly verify** how solutions align (or conflict) with `architecture.md`, `technical.md`, and `product_requirement_docs.md`.
    *   **Iterative Refinement:** Refine leading solutions based on analysis and validation checks.
    *   **Justify Optimality:** Select the optimal solution *for this task*. Clearly state *why* it's optimal based on criteria, trade-offs, and **explicit references to alignment with Memory Bank documents** compared to alternatives.

4.  **Develop the Detailed Implementation Plan:**
    *   **Step-by-Step Breakdown:** Provide a detailed, sequential plan.
    *   **Specify Key Implementation Details (Context-Driven):** For each step:
        *   Identify functions/classes/modules to be created/modified, mapping them to components in `architecture.md`.
        *   Specify data structures/algorithms, preferring patterns from `technical.md` or existing codebase.
        *   Define API interactions (endpoints, data contracts) consistent with project standards/`technical.md`.
        *   Detail database schema changes (if any).
        *   Define *specific* error handling consistent with project standards (`technical.md`).
        *   Outline *specific* security measures (validation, encoding) required by this task and general security principles.
        *   Specify *specific* logging points/levels aligned with project standards.
    *   **Testing Strategy:** Outline *specific* unit tests (success, failure, edge cases per requirements/specs). Mention integration points affected (referencing `architecture.md`). Ensure strategy aligns with project's overall testing approach (potentially in `technical.md` or separate testing docs).
    *   **Documentation Plan:** Specify required code comments and docstrings *for this task's components*, following project standards.
    *   **Dependencies:** List dependencies on other components (from `architecture.md`), libraries (`technical.md`), or tasks (`tasks_plan.md`).
    *   **Explicit Assumptions:** List assumptions made *during planning*.

5.  **Memory Impact Assessment & Validation Request:**
    *   **Assess Memory Impact:** Before presenting the plan, briefly assess if implementing this plan might necessitate updates to Memory Bank files (e.g., `architecture.md` if structure changes, `technical.md` if new pattern/library introduced, `tasks_plan.md` for new dependencies). **Note potential updates needed.**
    *   **Present Plan for Validation:** Structure the plan clearly. Include justification for the chosen solution.
    *   **(Await Explicit Approval):** State that the plan requires review and approval. **Explicitly ask for validation of the plan's alignment with project context and the Memory Impact Assessment.**

**(End of Planning Workflow - Enhanced)**