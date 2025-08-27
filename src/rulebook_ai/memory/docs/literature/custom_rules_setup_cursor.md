source: https://arc.net/l/quote/zegkkqjh

# Global Rules
Set in Cursor Settings under "General" > "Rules for AI". These rules apply across all your projects, perfect for personal coding preferences and consistent AI behavior.

Rule Examples
```
# In Cursor Settings > Rules for AI

- Use TypeScript for all new code
- Follow clean code principles
- Prefer async/await over callbacks
- Write comprehensive error handling
```

# Project Rules
Project-specific rules stored as .mdc files in the .cursor/rules directory. These rules help the AI understand your codebase and follow your project's conventions. Add them via Cursor Settings > General > Project Rules. They are synced with your codebase and can be automatically included when needed.

For backward compatibility, you can still use a .cursorrules file in the root of your project. We will eventually remove .cursorrules in the future, so we recommend migrating to the new Project Rules system for better flexibility and control.

Rule Examples
```
# File patterns: *.tsx, *.ts

## React Guidelines
- Use functional components
- Implement proper prop types
- Follow React best practices

## Style
- Use Tailwind CSS
- Follow team's style guide

@file ../tsconfig.json
@file ../tailwind.config.js
