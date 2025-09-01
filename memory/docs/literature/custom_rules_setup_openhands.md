**Sources:**
- https://docs.all-hands.dev/usage/prompting/microagents-overview
- https://docs.all-hands.dev/usage/prompting/microagents-repo
- https://docs.all-hands.dev/usage/prompting/microagents-keyword
- https://docs.all-hands.dev/usage/prompting/microagents-org
- https://docs.all-hands.dev/usage/prompting/repository

While OpenHands doesn’t use a `.rules` file like some other assistants, it supports microagents and repository scripts that allow you to extend and customize the agent’s behaviour. Microagents are specialized prompts that provide domain-specific knowledge and guidelines; they can apply to a single repository, trigger on keywords, or be shared across an organization or user.

---

### Microagents Overview

Microagents enhance OpenHands with domain-specific knowledge and expertise. To customize the agent, create a `.openhands/microagents/` directory at the root of your repository and add one or more `<microagent_name>.md` files. Each microagent file contains guidelines that are loaded into the agent’s context and can take up space in the context window.

---

### General Microagents

General microagents are always loaded for a repository. You can ask OpenHands to analyze your repository and automatically create a `repo.md` microagent summarizing the project’s purpose, structure and CI workflows. This reduces repeated searches and ensures the agent has complete context about your codebase.

---

### Keyword-Triggered Microagents

Keyword-triggered microagents provide instructions that activate only when certain keywords appear in a prompt. They require frontmatter at the top of the file specifying a list of trigger words, and optionally the agent type. For example, a `yummy.md` microagent could respond with a specific message whenever a user types a secret keyword.

---

### Organization & User Microagents

Organizations and users can define microagents that apply across all of their repositories by placing microagent files in a special repository named `.openhands` (or `openhands-config` on GitLab). These microagents are automatically loaded for every project owned by the organization or user. For locally running OpenHands installations, you can place microagents in `~/.openhands/microagents` to have them loaded for all conversations.

---

### Frontmatter Requirements

Keyword-triggered microagents require frontmatter with a `triggers` field that lists the keywords to activate the agent and an optional `agent` field to specify which agent it applies to. General microagents do not require frontmatter.

---

### Repository Customization

OpenHands also allows repository-level customizations using a `.openhands` directory. You can create a `.openhands/setup.sh` script that runs each time OpenHands begins working with your repository to install dependencies or set environment variables. A `.openhands/pre-commit.sh` script can be used to enforce code quality and run tests before each commit.

---

### Usage Summary

- Create a `.openhands/microagents/` directory in the root of your repository and add `.md` files containing guidelines or specialized knowledge.
- Use general microagents for always-loaded repository context and keyword-triggered microagents for instructions that activate on specific keywords.
- Place microagent files in a `.openhands` repository (or `openhands-config` on GitLab) to apply them across an organization, or in `~/.openhands/microagents` for user-level customizations.
- Use repository scripts (`setup.sh` and `pre-commit.sh`) to customize runtime behaviour and enforce standards.