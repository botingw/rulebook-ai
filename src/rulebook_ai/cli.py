"""Command line interface for rulebook-ai."""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from .assistants import SUPPORTED_ASSISTANTS
from .core import RuleManager


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage composable rulebook-ai packs and project context",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ------------------------------------------------------------------
    # Packs command group
    # ------------------------------------------------------------------

    packs_parser = subparsers.add_parser("packs", help="Manage pack library")
    packs_sub = packs_parser.add_subparsers(dest="packs_command", required=True)

    list_parser = packs_sub.add_parser("list", help="List available packs")
    list_parser.add_argument("--project-dir", "-p")

    add_parser = packs_sub.add_parser("add", help="Add pack(s) to the library")
    add_parser.add_argument("names", nargs="+")
    add_parser.add_argument("--project-dir", "-p")

    remove_parser = packs_sub.add_parser("remove", help="Remove pack(s) from the library")
    remove_parser.add_argument("names", nargs="+")
    remove_parser.add_argument("--project-dir", "-p")

    update_parser = packs_sub.add_parser(
        "update", help="Refresh community pack index"
    )
    update_parser.add_argument("--project-dir", "-p")

    status_parser = packs_sub.add_parser("status", help="Show configured packs and profiles")
    status_parser.add_argument("--project-dir", "-p")

    # ------------------------------------------------------------------
    # Profiles command group
    # ------------------------------------------------------------------

    profiles_parser = subparsers.add_parser("profiles", help="Manage pack profiles")
    profiles_sub = profiles_parser.add_subparsers(dest="profiles_command", required=True)

    create_p = profiles_sub.add_parser("create", help="Create a profile")
    create_p.add_argument("name")
    create_p.add_argument("--project-dir", "-p")

    delete_p = profiles_sub.add_parser("delete", help="Delete a profile")
    delete_p.add_argument("name")
    delete_p.add_argument("--project-dir", "-p")

    add_to = profiles_sub.add_parser("add", help="Add pack to profile")
    add_to.add_argument("pack")
    add_to.add_argument("--to", dest="profile", required=True)
    add_to.add_argument("--project-dir", "-p")

    remove_from = profiles_sub.add_parser("remove", help="Remove pack from profile")
    remove_from.add_argument("pack")
    remove_from.add_argument("--from", dest="profile", required=True)
    remove_from.add_argument("--project-dir", "-p")

    list_p = profiles_sub.add_parser("list", help="List profiles")
    list_p.add_argument("--project-dir", "-p")

    # ------------------------------------------------------------------
    # Project command group
    # ------------------------------------------------------------------

    project_parser = subparsers.add_parser("project", help="Operate on project context")
    project_sub = project_parser.add_subparsers(dest="project_command", required=True)

    sync_parser = project_sub.add_parser("sync", help="Compose context and generate rules")
    sync_parser.add_argument("--project-dir", "-p")
    sync_parser.add_argument("--profile")
    sync_parser.add_argument("--pack", action="append", dest="packs")
    assist_group = sync_parser.add_argument_group("assistant selection")
    for assistant in SUPPORTED_ASSISTANTS:
        assist_group.add_argument(
            f"--{assistant.name}",
            action="append_const",
            dest="assistants",
            const=assistant.name,
            help=f"Generate rules for {assistant.display_name}",
        )
    assist_group.add_argument(
        "--all",
        action="store_const",
        dest="assistants",
        const=[a.name for a in SUPPORTED_ASSISTANTS],
        help="Generate rules for all supported assistants",
    )

    status_p = project_sub.add_parser("status", help="Show last sync info")
    status_p.add_argument("--project-dir", "-p")

    clean_p = project_sub.add_parser("clean", help="Remove all rulebook-ai artifacts")
    clean_p.add_argument("--project-dir", "-p")

    clean_r = project_sub.add_parser("clean-rules", help="Remove generated rules and state")
    clean_r.add_argument("--project-dir", "-p")

    clean_ctx = project_sub.add_parser(
        "clean-context", help="Remove orphaned context files"
    )
    clean_ctx.add_argument("--project-dir", "-p")
    clean_ctx.add_argument("--action", choices=["delete", "keep"])
    clean_ctx.add_argument("--force", action="store_true")

    # ------------------------------------------------------------------
    # Utility commands
    # ------------------------------------------------------------------

    subparsers.add_parser("bug-report", help="Open issue tracker")
    subparsers.add_parser("rate-ruleset", help="Open ratings & reviews page")

    return parser


def handle_command(args: argparse.Namespace) -> int:
    project_dir = getattr(args, "project_dir", None)
    rm = RuleManager(project_dir)

    if args.command == "packs":
        cmd = args.packs_command
        if cmd == "list":
            rm.list_packs()
            return 0
        if cmd == "add":
            rc = 0
            for name in args.names:
                result = rm.add_pack(name, project_dir)
                if result != 0:
                    rc = result
            return rc
        if cmd == "remove":
            rc = 0
            for name in args.names:
                result = rm.remove_pack(name, project_dir)
                if result != 0:
                    rc = result
            return rc
        if cmd == "update":
            return rm.update_community_index()
        if cmd == "status":
            return rm.packs_status(project_dir)

    elif args.command == "profiles":
        cmd = args.profiles_command
        if cmd == "create":
            return rm.create_profile(args.name, project_dir)
        if cmd == "delete":
            return rm.delete_profile(args.name, project_dir)
        if cmd == "add":
            return rm.add_pack_to_profile(args.pack, args.profile, project_dir)
        if cmd == "remove":
            return rm.remove_pack_from_profile(args.pack, args.profile, project_dir)
        if cmd == "list":
            return rm.list_profiles(project_dir)

    elif args.command == "project":
        cmd = args.project_command
        if cmd == "sync":
            return rm.project_sync(
                assistants=getattr(args, "assistants", None),
                profile=args.profile,
                packs=getattr(args, "packs", None),
                project_dir=project_dir,
            )
        if cmd == "status":
            return rm.project_status(project_dir)
        if cmd == "clean":
            print(
                "WARNING: This will remove .rulebook-ai/, memory/, tools/, and generated rules."
            )
            try:
                confirm = input("Are you sure? (yes/No): ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nClean cancelled.")
                return 1
            if confirm == "yes":
                return rm.project_clean(project_dir)
            print("Clean cancelled by user.")
            return 0
        if cmd == "clean-rules":
            return rm.project_clean_rules(project_dir)
        if cmd == "clean-context":
            return rm.project_clean_context(
                project_dir=project_dir, action=args.action, force=args.force
            )

    elif args.command == "bug-report":
        return rm.report_bug()
    elif args.command == "rate-ruleset":
        return rm.rate_ruleset()

    return 1


def main(argv: Optional[List[str]] = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])
    try:
        return handle_command(args)
    except Exception as e:  # pragma: no cover - top level safety
        print(f"An unexpected error occurred: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

