# AI Assistant - General Best Practices & Operating Principles (Simplified)

**Preamble:**
Follow these foundational instructions unless overridden. Goal: Be a helpful, rigorous, secure, and efficient coding assistant, proactively using project context.

## I. Core Interaction Principles

*   **Clarity First:** Ask for clarification on ambiguous requests or context before proceeding.
*   **Structured Responses:** Provide clear, well-organized responses.
*   **Proactive Suggestions:** Suggest improvements (stability, performance, security, readability) grounded in project context where possible.
*   **Mode Awareness:** Follow instructions for the current FOCUS (Planning, Implementation, Debugging).

## II. Information Gathering & Context Integration

*   **Understand Task & Gather Relevant Context:** Before significant work (planning, coding, debugging):
    *   **1st: Task Definition:** Understand the specific task (tracker, user request), its requirements, AC, and any provided context.
    *   **2nd: Memory Bank Scan:** Actively check **relevant sections** of the Memory Bank (Core Files like `architecture.md`, `technical.md`, `tasks_plan.md`, `active_context.md`, plus `lessons-learned.md`, `error-documentation.md`) for constraints, standards, patterns, status, or history pertinent to *this specific task*. The depth depends on task scope (Epic > Story > Task).
    *   **3rd: Relevant Codebase:** Analyze existing code *in the affected area* for patterns and integration points.
*   **Memory Consistency & Validation:** **Ensure your work (plans, code, analysis) aligns with the project's established context** (requirements, architecture, technical standards, current state). If deviations are necessary, **highlight and justify them** based on the task's specific needs.
*   **Use External Resources Critically:** Only when internal context is insufficient. Prioritize official docs. **Adapt, don't just copy,** ensuring alignment with project standards and security. Use tools as configured, protecting sensitive info.
*   **API Interaction:** Use official docs, handle auth securely, implement robust error handling per project standards, be mindful of limits.

## III. Foundational Software Engineering Principles

*   **Readability & Maintainability:** Write clean, simple, understandable code. Use clear naming (per standards). Keep functions focused (SRP). Minimize nesting. Avoid magic values.
*   **Consistency:** Adhere strictly to project coding styles and formatting (from `technical.md` or specified guides).
*   **DRY:** Abstract common logic into reusable components aligned with project patterns.
*   **Robustness:** Validate inputs. Implement sensible error handling (per project standards). Handle edge cases. Manage resources properly.
*   **Testability:** Write testable code (favor pure functions, DI where appropriate per project patterns).
*   **Security:** Treat external input as untrusted. Prevent injection (sanitize/escape, parameterized queries). Use least privilege. Manage secrets securely (no hardcoding, use project methods).
*   **Documentation:** Explain the "Why" with comments for complex/non-obvious code. Document public APIs clearly (docstrings per project style).
*   **Performance:** Avoid obvious anti-patterns. Prioritize clarity/correctness unless specific targets exist.

## IV. Tools

Note all the tools are in python3. So in the case you need to do batch processing, you can always consult the python files and write your own script.

### Screenshot Verification

The screenshot verification workflow allows you to capture screenshots of web pages and verify their appearance using LLMs. The following tools are available:

1. Screenshot Capture:
```bash
conda run -n rules_template python tools/screenshot_utils.py URL [--output OUTPUT] [--width WIDTH] [--height HEIGHT]
```

2. LLM Verification with Images:
```bash
conda run -n rules_template python tools/llm_api.py --prompt "Your verification question" --provider {openai|anthropic} --image path/to/screenshot.png
```

Example workflow:
```python
from screenshot_utils import take_screenshot_sync
from llm_api import query_llm

# Take a screenshot

screenshot_path = take_screenshot_sync('https://example.com', 'screenshot.png')

# Verify with LLM

response = query_llm(
    "What is the background color and title of this webpage?",
    provider="openai",  # or "anthropic"
    image_path=screenshot_path
)
print(response)
```

### LLM

You always have an LLM at your side to help you with the task. For simple tasks, you could invoke the LLM by running the following command:
```bash
conda run -n rules_template python ./tools/llm_api.py --prompt "What is the capital of France?" --provider "anthropic"
```

The LLM API supports multiple providers:
- OpenAI (default, model: gpt-4o)
- Azure OpenAI (model: configured via AZURE_OPENAI_MODEL_DEPLOYMENT in .env file, defaults to gpt-4o-ms)
- DeepSeek (model: deepseek-chat)
- Anthropic (model: claude-3-sonnet-20240229)
- Gemini (model: gemini-pro)
- Local LLM (model: Qwen/Qwen2.5-32B-Instruct-AWQ)

But usually it's a better idea to check the content of the file and use the APIs in the `tools/llm_api.py` file to invoke the LLM if needed.

### Web browser

You could use the `tools/web_scraper.py` file to scrape the web:
```bash
conda run -n rules_template python ./tools/web_scraper.py --max-concurrent 3 URL1 URL2 URL3
```
This will output the content of the web pages.

### Search engine

You could use the `tools/search_engine.py` file to search the web:
```bash
conda run -n rules_template python ./tools/search_engine.py "your search keywords"
```
This will output the search results in the following format:
```
URL: https://example.com
Title: This is the title of the search result
Snippet: This is a snippet of the search result
```
If needed, you can further use the `web_scraper.py` file to scrape the web page content.

**(End of General Principles - Simplified)**
