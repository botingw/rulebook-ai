# Analysis of AI Rule Set Benchmark (Corrected)
Please note that the following analysis is based on a **limited set of ad-hoc tests**. This was not a comprehensive or rigorously controlled benchmark. Findings should be considered **preliminary observations** rather than definitive conclusions. Use this data as a starting point for your own evaluations.

## Benchmark Goal

To evaluate how different rule specifications (`heavy`, `medium`, `light`) combined with AI model capability (`gemini-1.5-pro` vs. `llama-3.1-nano`) and file attachment strategies affect the AI's ability to:

1.  Understand and answer a meta-question about whether the rules align with the project goal ("I updated rule files... Do you think it align with the goal of this project?").
2.  Potentially perform a related follow-up action (like updating `task_plan.md` or `active_context.md`).
3.  Token usage efficiency.

*(Corrections applied: Token count for the last Gemini Pro entry is 150k, not 15k. Attachment definitions clarified.)*

---

## Organized Benchmark Data (Corrected & Clarified)

**Attachment Definitions:**
*   `attach general rule file`: Only the general principles file (`06-rules...`) was attached.
*   `attach all files`: All core rule files (`00-meta`, `06-general`, `01-plan`, `01-code`, `01-debug`) were attached.

### Model: `nvidia/llama-3.1-nemotron-nano-8b-v1:free` (Non-Top Model)

| Rules Condition                    | Files Attached?         | Initial Tokens | Action/Outcome                               | Action Tokens | Notes                                |
| :--------------------------------- | :---------------------- | :------------- | :------------------------------------------- | :------------ | :----------------------------------- |
| `heavy-spec`                       | *Not Specified*         | 30k            | *Outcome Unclear*                            | N/A           | Lowest initial cost for this model |
| `medium-spec`                      | *Not Specified*         | 52k            | -> Act                                       | 200k          | High action cost                     |
| `light-spec`                       | *Not Specified*         | 25k            | -> Understand task 9?                        | 170k          | Low initial, high action/understanding cost |
| `only memory`                      | *Not Specified*         | 70k            | ERROR                                        | N/A           | High initial cost, failed            |
| `only memory + general light rule` | *Not Specified*         | N/A            | -> Understand need update `task_plan` -> FAIL | 72k           | Partial understanding, failed        |
| `only memory + general light rule` | `general rule file` (?) | 47k            | Find FOCUS workflow not defined              | N/A           | Identified rule gap, incomplete      |

### Model: `gemini-1.5-pro` (Best Model)

| Rules Condition                     | Files Attached?          | Initial Tokens | Outcome / Action                                   | Action Tokens | Notes                                     |
| :---------------------------------- | :----------------------- | :------------- | :------------------------------------------------- | :------------ | :---------------------------------------- |
| `only memory + general light rule`  | `general rule file`      | 26k            | Give conclusion                                    | N/A           | Efficient conclusion                    |
| `only memory + general medium rule` | `general rule file`      | 26k            | Give conclusion, **Correctly update `active_context`** | 155k          | Efficient conclusion, successful action   |
| `only memory + general heavy rule`  | `general rule file`      | 29k            | Give conclusion, **Updated `task_plan`**           | 125k          | Efficient conclusion, successful action   |
| `light-spec`                        | `all files`              | 69k            | -> Answer correct                                  | 168k          | Higher initial cost, correct answer       |
| `heavy-spec`                        | `general rule file`      | 33k            | Give conclusion, **Update `task_plan`**            | 150k          | Moderate conclusion cost, successful action |
| `only memory + general light rule`  | `all files`              | 27k            | Answer question, **Decide update `task_plan`**   | **150k**      | Efficient conclusion, *expensive* action proposal |

---

## Summary of Findings (Reflecting Corrections)

1.  **Model Capability is Dominant:** (No Change)
    *   `gemini-1.5-pro` consistently outperformed the `llama-3.1-nano` model in terms of token efficiency and task success.
    *   `llama-3.1-nano` struggled significantly, prone to errors and high token costs.

2.  **Minimal Rules are Risky:** (No Change)
    *   Providing `only memory` or `only memory + general rule` often led to errors or failures, especially with the less capable model.
    *   With `gemini-1.5-pro`, minimal rules were efficient for initial conclusions but required sufficient context (implicit or explicit) for successful action.

3.  **Impact of Rule Specification (`heavy` vs. `medium` vs. `light`) - Nuanced:** (Minor Adjustment)
    *   **With `llama-3.1-nano`:** Still inconclusive due to inconsistent results.
    *   **With `gemini-1.5-pro`:**
        *   `heavy-spec` (with general file): Successful `task_plan` update (29k + 125k). Also successful (update `task_plan`) when run as 'heavy-spec' with *only* general file attached (33k + 150k). *Slight discrepancy in costs across runs, but successful*.
        *   `medium-spec` (with general file): Successful `active_context` update (26k + 155k).
        *   `light-spec` (with `all files`): Correct answer, but higher token cost overall (69k + 168k).
        *   **Comparison:** Attaching only the `general rule file` alongside `medium` or `heavy` principles allowed `gemini-1.5-pro` to act successfully with reasonable token costs for the action itself (125k-155k).

4.  **File Attachment Strategy is Critical:** (Significant Change in Interpretation)
    *   Attaching relevant rule files remains essential for avoiding some errors (like the FOCUS definition error).
    *   Attaching *only* the `general rule file` was sufficient for `gemini-1.5-pro` to successfully execute actions when combined with `medium` or `heavy` principles. This suggests the general rules provide enough core guidance for a capable model if the principles themselves are detailed enough (`medium`/`heavy`).
    *   Attaching `all files` (including specific workflow rules) with `light principles + memory` proved **expensive** for the action proposal (27k + 150k), contrary to the previous interpretation based on the incorrect token count.
    *   Attaching `all files` with the full `light-spec` was also expensive overall (69k + 168k).
    *   **Revised Conclusion:** For `gemini-1.5-pro`, providing *only* the `general rule file` seems potentially more token-efficient *for performing actions* when using `medium` or `heavy` guiding principles, compared to attaching `all rule files`, especially with `light` principles. Providing all files might force processing of unnecessary details or conflict with the AI's internal reasoning when rules are minimal.

---

## Key Takeaways from Benchmark (Reflecting Corrections)

*   **Invest in Capable Models:** Still the most critical factor.
*   **Provide Context:** Still crucial. Attaching at least the relevant general rules, and likely having access to memory, is needed.
*   **Minimal Rules Insufficient Alone:** Still holds true.
*   **Rule Spec Choice & Attachment:**
    *   For `gemini-1.5-pro`, using `medium` or `heavy` principles combined with attaching *only* the `general rule file` proved effective and reasonably efficient for performing file update actions.
    *   Using `light` principles required attaching `all files` for a successful answer, but this configuration proved expensive overall, especially for action proposal/execution.
    *   The strategy of "light principles + full context access" is **not** the most token-efficient based on the corrected data; it was expensive for the action proposal step.
    *   `medium-spec` (with general file attached) remains a strong contender for balancing guidance and efficiency for capable models.
*   **Further Investigation Needed:** (Mostly Unchanged)
    *   Verify target file update consistency (`active_context` vs. `task_plan`).
    *   Assess the qualitative correctness of conclusions and file updates.
    *   Confirm the exact files attached in the `heavy-spec` run that cost 33k+150k (was it just general or all?).

---