"""
Command-line interface for rulebook-ai.

This module provides a modern CLI interface for the rulebook-ai package,
built on the core functionality in the core module.
"""

import argparse
import sys
from typing import List, Optional

from .core import RuleManager, DEFAULT_RULE_SET
from .assistants import SUPPORTED_ASSISTANTS


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Manage LLM rulesets and assistant configurations for various AI assistants.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Command to execute")

    # --- Install Command ---
    install_parser = subparsers.add_parser("install", help="Install a rule set and framework components into a project.")
    install_parser.add_argument("--rule-set", "-r", default=DEFAULT_RULE_SET, help=f"Rule set to install (default: {DEFAULT_RULE_SET})")
    install_parser.add_argument("--project-dir", "-p", help="Target project directory (default: current directory)")
    install_parser.add_argument("--clean", "-c", action="store_true", help="Clean existing rules before installation")
    
    assistant_group = install_parser.add_argument_group('assistant selection (if omitted, all are generated)')
    for assistant in SUPPORTED_ASSISTANTS:
        assistant_group.add_argument(f"--{assistant.name}", action='append_const', dest='assistants', const=assistant.name, help=f"Generate rules for {assistant.display_name}")
    assistant_group.add_argument("--all", "-a", action='store_const', dest='assistants', const=[a.name for a in SUPPORTED_ASSISTANTS], help="Generate rules for all supported assistants")

    # --- Sync Command ---
    sync_parser = subparsers.add_parser("sync", help="Synchronize assistant rules from the project_rules/ directory.")
    sync_parser.add_argument("--project-dir", "-p", help="Target project directory (default: current directory)")

    sync_assistant_group = sync_parser.add_argument_group('assistant selection (if omitted, syncs existing)')
    for assistant in SUPPORTED_ASSISTANTS:
        sync_assistant_group.add_argument(f"--{assistant.name}", action='append_const', dest='assistants', const=assistant.name, help=f"Sync rules for {assistant.display_name}")
    sync_assistant_group.add_argument("--all", "-a", action='store_const', dest='assistants', const=[a.name for a in SUPPORTED_ASSISTANTS], help="Sync rules for all supported assistants")

    # --- Clean Commands ---
    clean_rules_parser = subparsers.add_parser("clean-rules", help="Remove all rule-related files (generated rules and project_rules/).")
    clean_rules_parser.add_argument("--project-dir", "-p", help="Target project directory (default: current directory)")
    
    clean_all_parser = subparsers.add_parser("clean-all", help="Remove ALL rulebook-ai components, including memory/ and tools/.")
    clean_all_parser.add_argument("--project-dir", "-p", help="Target project directory (default: current directory)")
    
    # --- Utility Commands ---
    subparsers.add_parser("list-rules", help="List available rule sets.")
    subparsers.add_parser("doctor", help="Check environment and setup for issues.")

    return parser


def handle_command(args: argparse.Namespace) -> int:
    """Handle the parsed command-line arguments."""
    # Instantiate RuleManager with the project directory if the command needs it
    project_dir = args.project_dir if hasattr(args, 'project_dir') else None
    rule_manager = RuleManager(project_dir)

    command = args.command
    if command == "install":
        # If no assistants are specified, RuleManager's install->sync will handle the default
        return rule_manager.install(args.rule_set, args.project_dir, args.clean, args.assistants)
    
    elif command == "sync":
        # If assistants is None, RuleManager's sync will auto-detect
        return rule_manager.sync(args.project_dir, args.assistants)

    elif command == "clean-rules":
        return rule_manager.clean_rules(args.project_dir)

    elif command == "clean-all":
        print("WARNING: This will remove all rulebook-ai components from the target directory, including:")
        print("- project_rules/, memory/, and tools/ directories")
        print("- All generated assistant rule directories (.cursor/, .clinerules/, etc.)")
        print("\nThis may delete user-customized files in 'memory/' and 'tools/'.")
        try:
            confirm = input("Are you sure you want to proceed? (yes/No): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nClean-all operation cancelled.")
            return 1
        if confirm == 'yes':
            print("\nProceeding with full clean...")
            return rule_manager.clean_all(args.project_dir)
        else:
            print("Clean-all operation cancelled by user.")
            return 0

    elif command == "list-rules":
        rule_manager.list_rules()
        return 0

    elif command == "doctor":
        print("Doctor command not yet implemented in this version.")
        return 0

    return 1


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])
    
    if not args.command:
        parser.print_help()
        return 1

    try:
        return handle_command(args)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        # Consider adding a traceback here for debugging if needed
        # import traceback
        # traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())