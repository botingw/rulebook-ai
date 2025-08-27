source: https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot?tool=visualstudio#enabling-or-disabling-repository-custom-instructions

# Prerequisites for repository custom instructions
A custom instructions file (see the instructions below).
The Enable custom instructions option must be enabled in your settings. This is disabled by default. See Enabling or disabling repository custom instructions later in this article.

# Creating a repository custom instructions file
In the root of your repository, create a file named .github/copilot-instructions.md.

Create the .github directory if it does not already exist.

Add natural language instructions to the file, in Markdown format.

Whitespace between instructions is ignored, so the instructions can be written as a single paragraph, each on a new line, or separated by blank lines for legibility.

To see your instructions in action, go to https://github.com/copilot, attach the repository containing the instructions file, and start a conversation.
