# Project Management Documentation Prototype for Task/POC Human-AI Collaboration

**Project Context:** This prototype outlines the absolute minimum documentation required for efficiently executing a single, well-defined **technical Task** (part of a User Story) or a focused **Proof of Concept (POC)** using human-AI collaboration. The goal is extremely rapid execution and/or technical validation with AI assistance.

**Core Principle:** Provide **hyper-focused, explicit technical instructions and immediate context** necessary *only* for completing this specific Task/POC, eliminating all non-essential overhead.

---

## I. Required Information & Components (Essential for the Task/POC)

These are the bare minimum inputs needed for the AI (and human reviewer) to act effectively on this small scope.

1.  **Task Definition / POC Goal:**
    *   **Purpose:** Clearly defines the specific technical objective or the question the POC aims to answer.
    *   **Content:**
        *   **For Task:** Precise description of the technical action (e.g., "Refactor `getUserData()` function to use async/await," "Implement input validation for the `email` field according to spec X," "Write unit tests covering edge cases for `calculateDiscount()`").
        *   **For POC:** Clear statement of the goal/hypothesis (e.g., "Determine if Library 'FastLib' achieves <50ms response time under simulated load Y," "Prototype a minimal UI component using 'NewFramework' to assess integration difficulty," "Verify if API endpoint Z can be called successfully with authentication method Q").
        *   **Acceptance Criteria (Technical/Validation):**
            *   **For Task:** Concrete technical outcomes (e.g., "Code refactored, all existing tests pass, linter shows no errors," "Validation implemented, blocks invalid emails, allows valid ones per RFC 5322," "Unit tests achieve 90% branch coverage for the specified function").
            *   **For POC:** What constitutes success/completion (e.g., "Performance data collected and summarized," "Minimal UI component renders and interacts with basic state," "Successful API call confirmed, response logged").
        *   **Link to Parent (Crucial):** Direct link to the parent User Story (for Task) or the requirement/question driving the POC. Provides essential context.
    *   **AI Relevance:** The direct instruction. Needs to be technically precise. AC defines the target state or the required output/measurement.
    *   **Human Relevance:** Defines the specific work unit and its completion criteria.

2.  **Execution Context (Hyper-Focused):**
    *   **Purpose:** Provides the *exact* technical details, code references, and constraints needed *only* for this Task/POC.
    *   **Content (Must be extremely specific and readily available):**
        *   **Code Pointers:** Direct links/references to the specific files, functions, classes, or code snippets to be modified, tested, or used.
        *   **Technical Constraints:** Any specific library versions, API endpoints, configuration settings, algorithms, or data structures that *must* be used or adhered to.
        *   **Input Data/Setup (for POC/Testing):** Specific input data, environment setup instructions, or configuration needed to run the task or experiment.
        *   **Relevant Standards Snippet:** If a specific coding standard or pattern applies *directly* to this task, quote or link *only that specific rule* (don't link the entire standards doc).
    *   **AI Relevance:** **Mission-critical.** Provides the immediate technical environment and instructions. Eliminates any need for the AI to search broader context.
    *   **Human Relevance:** Contains the necessary details for implementation or verification. Human ensures this context is complete *for the task*.

3.  **Immediate Interaction Checkpoints:**
    *   **Purpose:** Defines the minimal necessary sync points for this short task.
    *   **Content (Very brief):**
        *   "Ping human reviewer immediately after code generation."
        *   "Provide output/results immediately after POC execution."
        *   "Ask clarification question via [channel] if blocked for > 5 minutes."
    *   **AI Relevance:** Sets clear, immediate expectations for interaction.
    *   **Human Relevance:** Defines the points for quick review or unblocking.

4.  **Validation Method:**
    *   **Purpose:** How the successful completion (meeting AC) will be verified *for this specific task/POC*.
    *   **Content:**
        *   **For Task:** "Run existing unit tests," "Execute specific test script," "Manual code review against checklist X," "Verify output against expected value Y."
        *   **For POC:** "Analyze logged performance metrics," "Demonstrate UI component interaction," "Confirm expected API response code/body."
    *   **AI Relevance:** May involve tasks for the AI (e.g., "Run tests"). Defines the success signal.
    *   **Human Relevance:** Specifies the verification step(s) required.

---

## II. Optional (Rarely Needed) Information

Generally avoided to maintain focus, but might include:

5.  **Brief Rationale Snippet:**
    *   **Purpose:** Tiny bit of context on *why* this specific technical task or POC is needed (e.g., "Refactoring for performance," "POC to de-risk technology choice for Story Z").
    *   **Content:** Single sentence, often included in the Task/POC definition itself.