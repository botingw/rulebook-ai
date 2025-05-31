# Meta-Rules for AI Assistant Interaction (Enhanced)

You will receive a sequence of approximately 10 rule files, starting with this one (the 0th file). Process them in order as they provide context and instructions for our interaction.

**File Sequence Purpose Overview:**
*   **This File (0th):** Explains the overall system, how to interpret the subsequent files, and how to determine your operational focus.
*   **Files 1 through 4 (approx.):** Project Memory Bank (Requirements, Architecture, Technical Details, Lessons Learned, etc.). Consult as directed or needed. Note `alwaysApply` flags. **These files provide essential context.**
*   **File 5 (approx.):** Project Directory Structure.
*   **File 6 (approx.):** General Principles and Best Practices (**ALWAYS FOLLOW**).
*   **Files 7 through 9 (approx.):** Specific operational workflows:
    *   **File 7 (approx.):** Rules for **FOCUS = PLANNING** (analysis, design, planning).
    *   **File 8 (approx.):** Rules for **FOCUS = IMPLEMENTATION** (coding based on a plan).
    *   **File 9 (approx.):** Rules for **FOCUS = DEBUGGING** (diagnosing/fixing errors).

**Determining Your Operational Focus and Applicable Rules:**

Apply the MOST relevant specific workflow rule set (from files approx. 7, 8, or 9) IN ADDITION to the general rules (file approx. 6). **Crucially, initial consultation of relevant Memory Bank files (as guided by File 6 and the specific workflow files) is a prerequisite step before fully executing the logic within a chosen FOCUS.** Use the following hierarchy to determine FOCUS:

1.  **Explicit User Command:** Check IF the user's LATEST request contains an explicit instruction like `FOCUS = PLANNING`, `FOCUS = IMPLEMENTATION`, or `FOCUS = DEBUGGING`.
    *   IF YES: Prioritize applying the workflow rules associated with that specified FOCUS (File 7, 8, or 9). This command OVERRIDES other factors for this turn.

2.  **Infer Task Intent (Primary Method after Explicit Command):** IF no explicit command (Step 1) applies, analyze the user's CURRENT request to determine the primary task intent:
    *   Is it about high-level design, analysis, creating a plan, exploring solutions? -> Determine **FOCUS = PLANNING** (Use rules from file approx. 7).
    *   Is it about writing code, implementing specific steps from a known plan, making direct modifications? -> Determine **FOCUS = IMPLEMENTATION** (Use rules from file approx. 8).
    *   Is it about fixing a reported error, diagnosing unexpected behavior, analyzing a failure? -> Determine **FOCUS = DEBUGGING** (Use rules from file approx. 9).
    *   IF unsure about the intent based on the request, ASK the user for clarification on the required FOCUS (Planning, Implementation, or Debugging).

3.  **Assistant's Internal State (Context / Cross-Check - If Applicable):** IF you are an assistant with persistent internal modes (e.g., 'Act', 'Debug', 'Architect'):
    *   **Cross-check:** Does your current internal mode *conflict* with the FOCUS determined in Step 2?
        *   **Example Conflict:** You are in 'Debug Mode', but Step 2 determined `FOCUS = PLANNING` based on the user's request ("Let's redesign this part").
        *   **Example Ambiguity:** You are in 'Act Mode' (which covers both Implementation and Debugging), and Step 2 determined `FOCUS = DEBUGGING`. This is consistent. If Step 2 determined `FOCUS = IMPLEMENTATION`, this is also consistent.
    *   **Action on Conflict:** If your internal mode *clearly conflicts* with the FOCUS determined from the user's current request (Step 2), NOTIFY the user: "My current internal mode is [Your Mode Name]. However, your request seems to be for [FOCUS determined in Step 2]. I will proceed with FOCUS = [FOCUS determined in Step 2] based on your request. Is this correct, or should I remain focused on tasks related to [Your Mode Name]?" *Prioritize the FOCUS derived from the current request (Step 2) after notifying.*
    *   **Action on Ambiguity:** If your internal mode covers multiple FOCUS types (like Cline's 'Act'), rely primarily on the FOCUS determined in Step 2 from the *specific request*. Your internal mode serves as broader context but doesn't dictate the rules file if the request is clearly about one specific FOCUS (e.g., debugging).

**Applying Rules:**
*   Always apply the rules from file approx. 6 (General Principles). **Ensure required Memory Bank consultations outlined in File 6 happen first.**
*   Apply the *one* most relevant specific workflow rule set (from files approx. 7, 8, or 9) determined primarily by Step 1 or Step 2 logic.
*   Consult memory bank files (approx. 1-4) **actively and as specified** within the applicable general and workflow rule files, or when directed by the user. The *depth* of consultation may vary based on task scope (Epic vs. Story vs. Task), but checking for *relevance* is always required.

**(End of Meta-Rules - Enhanced)**