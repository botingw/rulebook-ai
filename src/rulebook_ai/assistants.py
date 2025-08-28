"""
This module contains the declarative specification for all AI assistants
supported by the rulebook-ai tool.

It serves as the single source of truth for assistant configurations.
"""

import dataclasses
from typing import Dict, List, Optional

@dataclasses.dataclass(frozen=True)
class AssistantSpec:
    """
    Declaratively describes the project-level custom rule system for an AI assistant.
    This spec contains no generation logic; it only describes what the assistant expects.
    """
    # --- Core Identity ---
    name: str               # The internal, unique identifier (e.g., 'copilot')
    display_name: str       # The user-facing name (e.g., 'GitHub Copilot')

    # --- Rule Location & Structure ---
    # The primary path where project-specific rules are stored.
    rule_path: str

    # Does the assistant read a single file or a directory of files?
    is_multi_file: bool

    # Does the assistant recursively search subdirectories for rules?
    supports_subdirectories: bool

    # The top-level path to remove during a 'clean' operation.
    clean_path: str

    # --- File Constraints (with default values) ---
    # If not multi-file, what is the exact name of the rule file?
    filename: Optional[str] = None
    # If multi-file, what is the required extension for rule files? (None means any)
    file_extension: Optional[str] = None


# The single source of truth for all supported AI assistants
SUPPORTED_ASSISTANTS: List[AssistantSpec] = [
    AssistantSpec(
        name='cursor',
        display_name='Cursor',
        rule_path='.cursor/rules',
        is_multi_file=True,
        supports_subdirectories=False,
        file_extension='.mdc',
        clean_path='.cursor'
    ),
    AssistantSpec(
        name='windsurf',
        display_name='Windsurf',
        rule_path='.windsurf/rules',
        is_multi_file=True,
        supports_subdirectories=False,
        file_extension='.md',
        clean_path='.windsurf'
    ),
    AssistantSpec(
        name='cline',
        display_name='Cline',
        rule_path='.clinerules',
        is_multi_file=True,
        supports_subdirectories=False,
        file_extension=None,  # Extension is removed by our generator
        clean_path='.clinerules'
    ),
    AssistantSpec(
        name='roo',
        display_name='RooCode',
        rule_path='.roo/rules',
        is_multi_file=True,
        supports_subdirectories=True,
        clean_path='.roo'
    ),
    AssistantSpec(
        name='copilot',
        display_name='GitHub Copilot',
        rule_path='.github',
        is_multi_file=False,
        supports_subdirectories=False,
        filename='copilot-instructions.md',
        clean_path='.github/copilot-instructions.md'
    ),
]

# For quick lookups
ASSISTANT_MAP: Dict[str, AssistantSpec] = {a.name: a for a in SUPPORTED_ASSISTANTS}
