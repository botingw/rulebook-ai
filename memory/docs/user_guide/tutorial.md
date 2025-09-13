# Rulebook-AI: A Step-by-Step Tutorial

## Introduction

Welcome to `rulebook-ai`! This tutorial will guide you through the core features of the command-line tool. We'll start with an empty project and progressively build up a sophisticated, multi-environment setup for your AI assistants.

**Goal:** To learn how to manage AI environments (rules, context, and tools) using packs and profiles.

**Prerequisites:**
*   `uv` is installed (`curl -fsSL https://astral.sh/uv/install.sh | bash`).
*   You are working in a project directory you want to add AI rules to.

---

## Chapter 1: Your First Sync

Let's start by adding a basic environment to your project. We'll use the built-in `light-spec` pack, which provides a great general-purpose starting point for software development.

**1. Add the `light-spec` Pack**

Run the following command:

```bash
uvx rulebook-ai packs add light-spec
```

What did this do?
*   It created a `.rulebook-ai/` directory in your project to store configuration and local copies of packs.
*   It downloaded the `light-spec` pack into `.rulebook-ai/packs/`.
*   It updated `.rulebook-ai/selection.json`, which tracks the library of packs added to your project.

At this point, you have only added the pack to your project's *library*. You haven't applied it yet.

**2. Sync the Environment**

Now, let's apply the pack to your workspace:

```bash
uvx rulebook-ai project sync
```

This is the most important command. Here’s what it did:
*   It read your library of packs (right now, just `light-spec`).
*   It copied the starter files from the pack into `memory/` and `tools/` directories. These are for you to own and edit.
*   It generated the final, assistant-specific rule files (like `.cursor/rules/` and `GEMINI.md`) based on the pack's contents.

Your project directory should now look something like this:

```
my-project/
├── .rulebook-ai/   # Framework state (add to .gitignore)
├── .cursor/        # Generated rules for Cursor (add to .gitignore)
├── memory/         # Your AI's long-term memory (commit to git)
└── tools/          # Your AI's toolbox (commit to git)
```

You now have a foundational AI environment! You can edit the files in `memory/` to give your AI deep project context.

---

## Chapter 2: Composing Environments with Multiple Packs

The real power of `rulebook-ai` comes from combining packs. Let's imagine your project uses React and you want to add a specialized pack for React development.

**1. Discover Community Packs**

First, let's see what packs are available from the community.

```bash
# Fetches the latest list of community packs
uvx rulebook-ai packs update

# Lists all available built-in and community packs
uvx rulebook-ai packs list
```

Let's assume you find a pack named `community-react-pack` that looks promising.

**2. Add the React Pack**

```bash
uvx rulebook-ai packs add community-react-pack
```

Now, check your project's status:

```bash
rulebook-ai packs status
```

The output will show that your library now contains both `light-spec` and `community-react-pack`.

**3. Sync Your Composed Environment**

Run the sync command again:

```bash
uvx rulebook-ai project sync
```

`rulebook-ai` is smart. It now combines the rules and starter files from **both** packs. If there are any conflicts (e.g., both packs provide a `README.md` starter), the pack that was added first (`light-spec`) wins. This order is preserved in `selection.json`.

Your AI now has both general software engineering knowledge and specific expertise in React!

---

## Chapter 3: Specializing with Profiles

Most projects involve different kinds of work. You might be writing backend code one day and frontend code the next. **Profiles** let you create named groups of packs so you can easily switch between these different contexts.

**1. Create Profiles**

Let's create two profiles, `frontend` and `backend`.

```bash
rulebook-ai profiles create frontend
rulebook-ai profiles create backend
```

**2. Assign Packs to Profiles**

Now, let's assign our existing packs to these profiles.

```bash
# Add the react pack to the 'frontend' profile
rulebook-ai profiles add community-react-pack --to frontend

# Add the general-purpose pack to both
rulebook-ai profiles add light-spec --to frontend
rulebook-ai profiles add light-spec --to backend
```

**3. Sync a Specific Profile**

Now, when you're doing frontend work, you can sync just that profile:

```bash
uvx rulebook-ai project sync --profile frontend
```

This will generate rules based *only* on the packs in the `frontend` profile (`light-spec` and `community-react-pack`).

When you switch to backend work, you can apply a different environment:

```bash
uvx rulebook-ai project sync --profile backend
```

This regenerates the rules using only the `backend` profile's packs (just `light-spec` in this case). You now have a powerful way to give your AI the exact context it needs for the job at hand.

**Bonus Tip: Targeting Specific Assistants**

By default, `project sync` generates rules for all supported AI assistants. If you only use one or two, you can keep your project tidy by targeting them specifically with the `--assistant` flag.

You can combine this with profiles:

```bash
# Sync the frontend profile, but only for Cursor and Gemini
uvx rulebook-ai project sync --profile frontend --assistant cursor --assistant gemini
```

This will skip creating rule files for other assistants like RooCode or Windsurf.

---

## Chapter 4: Advanced Pack Sources

While the community index is great for discovering packs, you have more advanced options for adding them.

### Using a Pack Directly from GitHub

You can use any pack directly from a public GitHub repository, even if it's not in the community index. This is perfect for trying out a friend's new pack or using a development version.

Use the `github:` prefix followed by the `user/repo` slug:

```bash
# Add a pack directly from a GitHub URL
uvx rulebook-ai packs add github:some-user/their-awesome-pack
```

### Developing a Pack Locally

This is the most important workflow when you are building your own pack. The `local:` prefix lets you add a pack from a directory on your computer.

Imagine you are building `my-cool-pack` in a folder next to your current project. You can add it like this:

```bash
# Add a pack from a local directory
uvx rulebook-ai packs add local:../my-cool-pack
```

Now you can run `uvx rulebook-ai project sync` in your main project to test your local pack's changes in a real environment. This creates a tight feedback loop for development.

---

## Chapter 5: Managing Your Workspace

Here are a few essential commands for managing your `rulebook-ai` project.

*   **Check the current sync state:** See which profile or packs were last applied.
    ```bash
    rulebook-ai project status
    ```

*   **Remove a pack from your library:**
    ```bash
    rulebook-ai packs remove community-react-pack
    ```

*   **Clean generated rules:** If you want to reset the generated rules without touching your valuable `memory/` and `tools/` files:
    ```bash
    rulebook-ai project clean-rules
    ```

*   **Completely uninstall from a project:** This is a destructive action that removes all `rulebook-ai` related files and directories (`.rulebook-ai`, `memory`, `tools`, etc.). Use with care!
    ```bash
    rulebook-ai project clean
    ```

## Chapter 6: Becoming a Contributor

You now know how to use `rulebook-ai`! The next step is to contribute back to the community by creating your own pack.

`rulebook-ai` makes this easy by providing a pack that turns your AI into an expert on pack authoring.

**1. Add the Authoring Guide Pack**

```bash
uvx rulebook-ai packs add pack-authoring-guide
```

**2. Sync the Guide**

```bash
uvx rulebook-ai project sync --pack pack-authoring-guide
```

**3. Start Creating!**

Your AI now has all the specifications, guides, and validation tools in its context. You can now ask it to help you build a new pack. For example:

> *"Hey AI, using the rules from the `pack-authoring-guide`, help me create a new pack for Python development. Let's start with the `manifest.yaml` file."*

This workflow is the heart of `rulebook-ai`: using the tool to enhance the AI's capabilities to help you use the tool itself.
