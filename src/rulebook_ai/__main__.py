"""
Main entry point for direct module execution.

This allows running the module directly with 'python -m rulebook_ai'
or via 'uvx rulebook-ai' after installing the uv package.
"""

from .cli import main
import sys

if __name__ == "__main__":
    sys.exit(main())
