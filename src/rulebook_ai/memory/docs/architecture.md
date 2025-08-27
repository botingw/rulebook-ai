# System Architecture Document

## Overview:
The system uses platform-specific rule files (`.cursor/rules/`, `.clinerules`, `.clinerules-{mode}`) that define workflows (Plan, Implement, Debug) and a shared set of documentation files acting as a persistent memory bank (`docs/`, `tasks/`).

## Components:
1. Rule Files (per platform)
2. Memory Files (Core & Context)
3. Directory Structure Standard

## Goal:
Provide consistent AI behavior and context across different assistants.
