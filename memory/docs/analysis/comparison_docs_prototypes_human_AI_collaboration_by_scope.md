# Comparison of Documentation Prototypes for Human-AI Collaboration by Scope

This table compares the recommended documentation structures for managing software development work involving human-AI collaboration at different levels of granularity: Epic/Large-Scope Project, Single Story, and Task/Proof of Concept (POC). The focus is on enabling efficient interaction and maximizing AI contribution while ensuring human oversight and control.

| Aspect / Dimension          | Epic / Large-Scope Project                        | Single Story                                    | Task / POC                                           |
| :-------------------------- | :------------------------------------------------ | :---------------------------------------------- | :--------------------------------------------------- |
| **Primary Goal**            | Manage long-term complexity, consistency, risk, strategy | Deliver specific user value/functional increment | Execute specific technical action or validate feasibility/learn |
| **Scope Definition**        | Project Charter / Vision Document                 | User Story Definition                           | Technical Task Description / POC Goal                |
| **Acceptance Criteria**     | High-level business goals; Functional for Epics   | Functional, user-centric, testable for Story    | Technical completion or validation/measurement       |
| **Work Breakdown**          | Full Hierarchy (Epic -> Story -> Task)            | Story decomposed into Tasks                     | Minimal/None (Task is the unit)                      |
| **Context Provision**       | Comprehensive Memory Bank (Arch, Tech, Standards, Decisions); Central Repositories; Linked from Tasks | Relevant snippets/links provided *with* Story/Tasks; Focused context | Hyper-focused code pointers, constraints, setup *only* for the Task/POC |
| **Detail Level**            | High; Comprehensive documentation maintained      | Medium; Sufficient detail for the story         | Low; Only immediate technical details                |
| **Interaction Protocol**    | Formal Team Process & AI Protocols (Project-wide) | Defined Interaction Protocol *for the story*    | Immediate, tactical Checkpoints *for the task*       |
| **Testing/Validation Focus**| Comprehensive Strategy (Unit, Integration, E2E, Security, Perf) | Focused on Story functionality & related code   | Focused on technical correctness or POC outcome      |
| **Documentation Overhead**  | High (Necessary for scale & complexity)           | Medium/Minimal (Focused on the story)           | Near-Zero (Focused on immediate execution)           |
| **Traceability/Linkage**    | Essential across all levels (Epic->Story->Task->Context) | Task->Story, Story->Epic (opt), Task->Context | *Requires* link back to parent Story/Question        |
| **Key Artifacts**           | Charter, Roadmap, Memory Bank, Full Specs, Process Docs, Decision Log, Risk Register | Story Def, Task List, Linked Specs/Context, Story Test Req, Interaction Protocol | Task/POC Def, Execution Context, Checkpoints, Validation Method |
| **AI Interaction Needs**    | Relies on well-maintained Memory Bank & clear task linking | Needs focused context linked directly to tasks | Needs precise technical instructions & code pointers |
| **Human Role Emphasis**     | Strategic planning, oversight, process definition, complex integration, risk management | Story refinement, task prep for AI, review, validation, handling complexity beyond AI | Task definition, context prep, quick review/unblocking, interpreting POC results |

---

**Summary:**

The required documentation scales directly with the scope of the work being managed.

*   **Epic/Large-Scope:** Emphasizes comprehensive, persistent documentation for strategic alignment, consistency, risk management, and traceability across many interconnected parts. Requires significant setup and maintenance but is crucial for managing complexity with human-AI teams.
*   **Single Story:** Focuses on providing sufficient context and clear instructions to implement a specific piece of user value efficiently. It strips away project-wide overhead but retains essential functional and technical details for the story.
*   **Task/POC:** Represents the most tactical level, minimizing documentation to the absolute essentials needed for immediate technical execution or validation. It relies heavily on the context provided by the parent story or driving question.

Choosing the appropriate level ensures that both humans and AI assistants have the necessary information to collaborate effectively without being burdened by irrelevant overhead.