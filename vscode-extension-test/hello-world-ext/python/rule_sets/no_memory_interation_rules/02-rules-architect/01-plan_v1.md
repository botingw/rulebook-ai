# AI Assistant - Workflow: Planning & Solution Proposal (FOCUS = PLANNING)
# Applies when internal mode is Plan Mode (Cline) / Architect Mode (Roo Code), OR when task FOCUS is PLANNING.
# Assumes General Principles (File approx. 6) processed.

**(Rules for Planning, Analysis, and Solution Design follow)**

**Overall Goal:** To thoroughly understand the task (building on general clarification principles), rigorously explore potential solutions using internal and external resources appropriately, and produce a detailed, validated implementation plan *before* any code is written.

## Process & Best Practices:

1.  **Deep Dive into Requirements & Achieve Certainty:**
    *   **(Mandatory First Step - Intensive Clarification)** Apply the general clarification principle with *maximum rigor*. Actively probe for *all* ambiguities, edge cases, and assumptions related to the specific task. Re-state complex requirements to confirm understanding.
    *   **Anticipate Needs:** Suggest related considerations, potential future needs, or alternative scenarios pertinent to *this specific task* that might require specification.
    *   **Goal:** Achieve 100% clarity and confidence on *this specific task's* requirements before proceeding. If uncertainty remains, explicitly state what information is still needed.

2.  **Decompose the Problem & Explore Solutions:**
    *   **(Leverage Internal Context First - As per General Rules)**
    *   **Decomposition:** Break the core problem down into smaller, logical sub-problems or key functional components based on the requirements and existing system structure. Outline a high-level architectural approach if applicable.
    *   **Brainstorm Multiple Solutions:** For the core problem and key sub-problems, generate *multiple* potential implementation approaches, considering project standards and existing patterns found during context gathering.
    *   **Define Evaluation Criteria:** Establish clear criteria for comparing solutions specifically for this task (e.g., maintainability, performance, security, complexity, alignment with project patterns, effort).
    *   **Utilize Tools for Solution Ideas (If Necessary):** If internal resources lack specific algorithmic patterns or library usage examples needed for *solution design*, use approved external search tools (following general tool usage guidelines).

3.  **Evaluate, Refine, and Select Optimal Solution:**
    *   **Trade-off Analysis:** Evaluate the brainstormed solutions against the defined criteria. Clearly articulate the pros and cons (trade-offs) of each promising approach *in the context of this task*.
    *   **Rigorous Reasoning:** Question the assumptions and inferences behind each potential solution. Support claims with evidence or strong reasoning based on project context or general principles.
    *   **Iterative Refinement:** Consider combining the strongest aspects of different approaches. Refine the leading solution(s) based on the analysis.
    *   **Justify Optimality:** Select the solution deemed optimal *for this task*. Clearly state *why* it is considered optimal based on the evaluation criteria and trade-offs, compared to other viable alternatives.

4.  **Develop the Detailed Implementation Plan:**
    *   **Step-by-Step Breakdown:** Provide a detailed, sequential plan for implementing the chosen solution.
    *   **Specify Key Implementation Details:** For each step, define *how* the general principles (from General Instructions) will be applied *specifically* for this task:
        *   Functions/Classes/Modules to be created or modified.
        *   Data structures and algorithms to be used.
        *   API endpoints to interact with or define.
        *   Database schema changes (if any).
        *   *Specific* error handling logic/mechanisms for anticipated task errors.
        *   *Specific* security measures required by this task (input validation, output encoding, etc.).
        *   *Specific* logging points and levels.
    *   **Testing Strategy:** Outline the *specific* unit tests needed (types of cases: success, failure, edge cases, security aspects). Mention integration points affected or requiring testing.
    *   **Documentation Plan:** Specify required code comments (for complex logic) and docstrings/API documentation *for the components of this task*.
    *   **Dependencies:** List any dependencies on other components, libraries, or tasks.
    *   **Explicit Assumptions:** Clearly list any assumptions made *during this planning phase*.

5.  **Present Plan for Validation:**
    *   Structure the plan clearly (e.g., using headings, bullet points, numbered lists).
    *   Include the justification for the chosen solution and its trade-offs.
    *   **(Await Explicit Approval):** State that the plan requires review and approval from a human developer before proceeding to "Act Mode".