# AI Assistant Collaboration Rulesets

## Overview

This repository contains different versions of rule sets designed to enhance the effectiveness of AI coding assistants (like Cursor, Cline, Roo Code, etc.) when collaborating with human developers on software projects. The core philosophy is to improve AI performance by providing structured workflows, clear principles, and mechanisms for integrating project-specific context via a "Memory Bank" system.

Three distinct versions are provided, catering to different needs regarding detail, prescriptiveness, and flexibility:

1.  **`heavy-spec/`**: The original, highly detailed and prescriptive ruleset.
2.  **`medium-spec/`**: A simplified version balancing detail and principle-based guidance.
3.  **`light-spec/`**: An advanced simplification focusing on core principles and maximum conciseness.

All versions share the same fundamental goal: enabling more effective human-AI teamwork on projects ranging from simple tasks to complex epics.

## Rule Set Versions

Each version resides in its own subdirectory:

*   **`./heavy-spec/`**: Contains the most detailed rules, with many explicit checks and granular steps within workflows.
*   **`./medium-spec/`**: Contains rules simplified by consolidating steps and relying slightly more on general principles, reducing redundancy.
*   **`./light-spec/`**: Contains the most concise rules, focusing heavily on core principles and assuming a higher capability for AI interpretation and human context provision.

**Note:** The critical mode determination logic within `00-meta-rules.md` (handling different AI assistant internal modes like Plan/Act/Debug/Architect) remains consistent and detailed across all three versions to ensure broad applicability.

## Version Comparison

| Feature                     | `heavy-spec/` (Original Detailed)                     | `medium-spec/` (Simplified)                            | `light-spec/` (Advanced Simplified)                 |
| :-------------------------- | :---------------------------------------------------- | :----------------------------------------------------- | :-------------------------------------------------- |
| **Detail Level**            | Very High                                             | Medium                                                 | Low                                                 |
| **Prescriptiveness**        | Highly Prescriptive (many explicit steps/checks)    | Balanced (Consolidated steps, more principle reliance) | Low (Primarily Principle-Based)                     |
| **Emphasis**                | Explicit Workflow Steps & Validations                 | Core Principles & Streamlined Workflow Steps           | Core Principles & Workflow Outcomes                 |
| **Memory Bank Interaction** | Detailed checks mandated at multiple points         | Initial scan + Principle of ongoing consistency        | Initial scan + Strong Principle of ongoing alignment |
| **Redundancy**              | Higher (checks repeated in different contexts)        | Reduced                                                | Minimal                                             |
| **Flexibility**             | Lower                                                 | Medium                                                 | Higher                                              |
| **AI Capability Assumption**| Lower (provides more explicit guardrails)           | Medium                                                 | Higher (requires good principle interpretation)     |
| **Human Oversight Needs**   | Medium (easier to check compliance)                 | Medium-High (need to ensure principles are followed)   | High (need to verify interpretation & provide context) |
| **Potential Speed/Tokens**  | Potentially Slower / Higher Tokens                    | Medium                                                 | Potentially Faster / Lower Tokens                   |
| **Risk of Misinterpretation**| Lower                                                 | Medium                                                 | Higher                                              |

## Intended Use Cases

*   **`heavy-spec/`:**
    *   Large, complex projects requiring maximum rigor and traceability.
    *   Teams new to human-AI collaboration needing strong guardrails.
    *   Situations involving less capable AI models that benefit from explicit instructions.
    *   Projects with strict compliance or validation requirements.
    *   When predictability and detailed process adherence are paramount.

*   **`medium-spec/`:**
    *   General-purpose use for moderately complex projects.
    *   Teams comfortable with AI but still wanting clear structure and validation points.
    *   A good balance between reducing verbosity and maintaining explicit guidance.
    *   When the `heavy-spec` feels too cumbersome, but the `light-spec` seems too loose.

*   **`light-spec/`:**
    *   Teams highly experienced with AI collaboration and effective context provision.
    *   Projects utilizing highly capable AI models adept at interpreting and applying principles.
    *   Rapid prototyping or projects where flexibility and speed are prioritized over extreme process rigidity.
    *   Situations where human oversight is readily available to guide and validate the AI's interpretation of principles.
    *   Smaller tasks or stories where minimal overhead is desired.

## How to Choose the Right Version

Consider these factors:

1.  **Project Complexity & Scale:** How large and intricate is your project? (More Complex -> `heavy-spec` or `medium-spec`)
2.  **Team Experience:** How familiar is your team with directing and validating AI assistants? (Less Experience -> `heavy-spec`)
3.  **AI Assistant Capability:** How well does your specific AI handle nuance, context, and applying general principles? (Less Capable -> `heavy-spec`)
4.  **Need for Rigor vs. Flexibility:** Do you need strict, verifiable steps or more adaptable guidance? (Rigor -> `heavy-spec`; Flexibility -> `light-spec`)
5.  **Tolerance for AI Errors:** How critical is it to minimize AI deviation versus allowing more freedom? (Low Tolerance -> `heavy-spec`)
6.  **Time Investment:** How much effort can the team dedicate to defining precise context vs. reviewing principle-based AI output? (`heavy-spec` front-loads detail; `light-spec` requires more review/guidance).

**Recommendation:** Start with `medium-spec` as a baseline. If you find the AI frequently misses crucial checks or needs more explicit guidance, consider `heavy-spec`. If you find `medium-spec` too verbose and your team/AI combination works effectively with more abstract guidance, experiment with `light-spec`.

## Key Files (Common Structure Across Versions)

While the content detail varies, the core file structure remains similar:

*   `00-meta-rules.md`: Determines operational focus (Plan/Implement/Debug) and handles cross-assistant mode logic.
*   `06-rules_v1.md` / `06-rules_v1-*.md`: Defines General Principles & Best Practices (including context gathering, SE standards). *Content varies significantly by spec level.*
*   `01-plan_v1.md` / `01-plan_v1-*.md`: Workflow for Planning focus. *Content varies significantly by spec level.*
*   `01-code_v1.md` / `01-code_v1-*.md`: Workflow for Implementation focus. *Content varies significantly by spec level.*
*   `01-debug_v1.md` / `01-debug_v1-*.md`: Workflow for Debugging focus. *Content varies significantly by spec level.*
*   *(Other files relate to Memory Bank definitions, directory structure, etc.)*

## Usage

Integrate the chosen ruleset (from the corresponding subdirectory) into your AI coding assistant's configuration according to its specific mechanism for loading custom instructions or rule files. Ensure the AI has access to the referenced Memory Bank files within your project structure.

## Customization

These rulesets are starting points. Feel free to adapt, modify, and combine elements from different versions to best suit your specific project needs, team workflow, and AI assistant capabilities.