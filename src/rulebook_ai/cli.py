"""
Command-line interface for rulebook-ai.

This module provides a modern CLI interface for the rulebook-ai package,
built on the core functionality in the core module.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any

from .core import RuleManager, DEFAULT_RULE_SET


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Args:
        args: Command line arguments (uses sys.argv if None)
        
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Manage LLM rulesets and assistant configurations",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Install command
    install_parser = subparsers.add_parser("install", help="Install a rule set")
    install_parser.add_argument(
        "--rule-set", "-r",
        default=DEFAULT_RULE_SET,
        help=f"Rule set to install (default: {DEFAULT_RULE_SET})"
    )
    install_parser.add_argument(
        "--project-dir", "-p",
        help="Target project directory (default: current directory)"
    )
    install_parser.add_argument(
        "--clean", "-c",
        action="store_true",
        help="Clean existing rules before installation"
    )
    install_parser.add_argument(
        "--no-copilot",
        action="store_true",
        help="Skip creating GitHub Copilot instructions"
    )
    
    # Assistant-specific installation flags
    assistant_group = install_parser.add_mutually_exclusive_group()
    assistant_group.add_argument(
        "--cursor",
        action="store_true",
        help="Install rules for Cursor AI assistant only"
    )
    assistant_group.add_argument(
        "--windsurf",
        action="store_true",
        help="Install rules for Windsurf AI assistant only"
    )
    assistant_group.add_argument(
        "--cline",
        action="store_true",
        help="Install rules for Cline AI assistant only"
    )
    assistant_group.add_argument(
        "--roo",
        action="store_true",
        help="Install rules for RooCode AI assistant only"
    )
    assistant_group.add_argument(
        "--all-assistants", "-a",
        action="store_true",
        help="Install rules for all AI assistants"
    )
    
    # Sync command
    sync_parser = subparsers.add_parser("sync", help="Synchronize with a rule set")
    sync_parser.add_argument(
        "--rule-set", "-r",
        default=DEFAULT_RULE_SET,
        help=f"Rule set to sync with (default: {DEFAULT_RULE_SET})"
    )
    sync_parser.add_argument(
        "--project-dir", "-p",
        help="Target project directory (default: current directory)"
    )
    sync_parser.add_argument(
        "--no-copilot",
        action="store_true",
        help="Skip updating GitHub Copilot instructions"
    )
    
    # Assistant-specific sync flags
    sync_assistant_group = sync_parser.add_mutually_exclusive_group()
    sync_assistant_group.add_argument(
        "--cursor",
        action="store_true",
        help="Sync rules for Cursor AI assistant only"
    )
    sync_assistant_group.add_argument(
        "--windsurf",
        action="store_true",
        help="Sync rules for Windsurf AI assistant only"
    )
    sync_assistant_group.add_argument(
        "--cline",
        action="store_true",
        help="Sync rules for Cline AI assistant only"
    )
    sync_assistant_group.add_argument(
        "--roo",
        action="store_true",
        help="Sync rules for RooCode AI assistant only"
    )
    sync_assistant_group.add_argument(
        "--all-assistants", "-a",
        action="store_true",
        help="Sync rules for all AI assistants"
    )
    
    # Clean-rules command
    clean_rules_parser = subparsers.add_parser("clean-rules", help="Remove installed rules")
    clean_rules_parser.add_argument(
        "--project-dir", "-p",
        help="Target project directory (default: current directory)"
    )
    
    # Clean-all command
    clean_all_parser = subparsers.add_parser("clean-all", help="Remove all rulebook-ai files")
    clean_all_parser.add_argument(
        "--project-dir", "-p",
        help="Target project directory (default: current directory)"
    )
    
    # List-rules command
    subparsers.add_parser("list-rules", help="List available rule sets")
    
    # Doctor command
    subparsers.add_parser("doctor", help="Verify environment and rule activation")
    
    return parser.parse_args(args)


def handle_install(args: argparse.Namespace) -> int:
    """
    Handle the 'install' command.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success)
    """
    rule_manager = RuleManager()
    
    # Determine which assistants to install for
    assistants = []
    if args.cursor:
        assistants = ['cursor']
    elif args.windsurf:
        assistants = ['windsurf']
    elif args.cline:
        assistants = ['cline']
    elif args.roo:
        assistants = ['roo']
    elif args.all_assistants:
        assistants = ['cursor', 'windsurf', 'cline', 'roo']
    else:
        # Default behavior - install for all assistants like original
        assistants = ['cursor', 'windsurf', 'cline', 'roo']
    
    return rule_manager.install(
        rule_set=args.rule_set,
        project_dir=args.project_dir,
        clean_first=args.clean,
        include_copilot=not args.no_copilot,
        assistants=assistants
    )


def handle_sync(args: argparse.Namespace) -> int:
    """
    Handle the 'sync' command.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success)
    """
    rule_manager = RuleManager()
    
    # Determine which assistants to sync
    assistants = []
    if args.cursor:
        assistants = ['cursor']
    elif args.windsurf:
        assistants = ['windsurf']
    elif args.cline:
        assistants = ['cline']
    elif args.roo:
        assistants = ['roo']
    elif args.all_assistants:
        assistants = ['cursor', 'windsurf', 'cline', 'roo']
    else:
        # Default behavior - sync all existing assistants
        assistants = None
    
    return rule_manager.sync(
        rule_set=args.rule_set,
        project_dir=args.project_dir,
        include_copilot=not args.no_copilot,
        assistants=assistants
    )


def handle_clean_rules(args: argparse.Namespace) -> int:
    """
    Handle the 'clean-rules' command.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success)
    """
    rule_manager = RuleManager()
    return rule_manager.clean_rules(project_dir=args.project_dir)


def handle_clean_all(args: argparse.Namespace) -> int:
    """
    Handle the 'clean-all' command.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success)
    """
    rule_manager = RuleManager()
    return rule_manager.clean_all(project_dir=args.project_dir)


def handle_list_rules(args: argparse.Namespace) -> int:
    """
    Handle the 'list-rules' command.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success)
    """
    rule_manager = RuleManager()
    rule_sets = rule_manager.list_rules()
    
    if not rule_sets:
        print("No rule sets found.")
        return 1
        
    print("Available rule sets:")
    for rule_set in rule_sets:
        print(f"  - {rule_set}")
        
    print(f"\nDefault rule set: {DEFAULT_RULE_SET}")
    print("\nTo install a rule set:")
    print(f"  rulebook-ai install --rule-set <rule_set_name>")
    
    return 0


def handle_doctor(args: argparse.Namespace) -> int:
    """
    Handle the 'doctor' command.
    
    This command verifies the environment and rule activation.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 for success)
    """
    print("Rulebook-AI Doctor: Checking environment and setup...")
    
    # Check Python version
    import platform
    python_version = platform.python_version()
    print(f"Python version: {python_version}")
    major, minor, _ = map(int, python_version.split('.'))
    if major < 3 or (major == 3 and minor < 9):
        print("⚠️ WARNING: Python version should be 3.9 or higher")
    else:
        print("✅ Python version is compatible")
    
    # Check if running in a virtual environment
    in_venv = sys.prefix != sys.base_prefix
    if in_venv:
        print(f"✅ Running in a virtual environment: {sys.prefix}")
    else:
        print("⚠️ WARNING: Not running in a virtual environment")
    
    # Check installed packages
    try:
        import importlib.metadata
        required_packages = [
            "openai", "anthropic", "python-dotenv", 
            "playwright", "html5lib", "duckduckgo-search"
        ]
        missing = []
        for pkg in required_packages:
            try:
                version = importlib.metadata.version(pkg)
                print(f"✅ {pkg} version {version} installed")
            except importlib.metadata.PackageNotFoundError:
                missing.append(pkg)
                print(f"❌ {pkg} not installed")
        
        if missing:
            print("\n⚠️ Some required packages are missing. Install them with:")
            print(f"  pip install {' '.join(missing)}")
    except ImportError:
        print("⚠️ Unable to check installed packages (importlib.metadata not available)")
    
    # Check for project rules
    cwd = Path.cwd()
    rules_dir = cwd / "project_rules"
    if rules_dir.is_dir():
        rule_count = len([f for f in rules_dir.glob("*.md") if f.is_file()])
        if rule_count > 0:
            print(f"✅ Found {rule_count} rule files in {rules_dir}")
        else:
            print(f"⚠️ Rules directory exists but contains no .md files: {rules_dir}")
    else:
        print(f"❌ Rules directory not found: {rules_dir}")
        print("   Run 'rulebook-ai install' to set up rules")
    
    # Check for environment variables
    env_path = cwd / ".env"
    if env_path.exists():
        print(f"✅ Found .env file: {env_path}")
    else:
        env_example = cwd / ".env.example"
        if env_example.exists():
            print(f"⚠️ .env file not found, but .env.example exists")
            print("   Create a .env file by copying .env.example and filling in your API keys")
        else:
            print("❌ Neither .env nor .env.example found")
    
    # Check for known issues
    print("\nChecking for known issues...")
    
    # Check for the Windsurf activation bug
    try:
        import os
        if "WINDSURF_ACTIVATION_TOKEN" in os.environ:
            print("✅ WINDSURF_ACTIVATION_TOKEN is set in environment")
        else:
            print("ℹ️ WINDSURF_ACTIVATION_TOKEN not found in environment")
            print("   This is only needed if you're using Windsurf")
    except Exception:
        print("⚠️ Unable to check for Windsurf activation token")
    
    print("\nDiagnostic check complete.")
    return 0


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CLI.
    
    Args:
        args: Command line arguments (uses sys.argv if None)
        
    Returns:
        Exit code (0 for success)
    """
    parsed_args = parse_args(args)
    
    # Handle the selected command
    if parsed_args.command == "install":
        return handle_install(parsed_args)
    elif parsed_args.command == "sync":
        return handle_sync(parsed_args)
    elif parsed_args.command == "clean-rules":
        return handle_clean_rules(parsed_args)
    elif parsed_args.command == "clean-all":
        return handle_clean_all(parsed_args)
    elif parsed_args.command == "list-rules":
        return handle_list_rules(parsed_args)
    elif parsed_args.command == "doctor":
        return handle_doctor(parsed_args)
    else:
        print("Error: Please specify a command.")
        print("Run 'rulebook-ai --help' for usage information.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
