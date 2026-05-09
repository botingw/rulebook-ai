"""Regression tests for pytest configuration."""

import subprocess
import sys
from pathlib import Path


def test_pytest_config_supports_collect_only_from_repo_root() -> None:
    """The pyproject pytest config should not fail during argument parsing."""
    repo_root = Path(__file__).resolve().parents[2]

    result = subprocess.run(  # noqa: S603
        [
            sys.executable,
            "-m",
            "pytest",
            "--collect-only",
            "tests/unit/test_state_files.py",
            "-q",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        timeout=30,
    )

    if result.returncode != 0:
        raise AssertionError(result.stderr)
    if "test_state_files.py" not in result.stdout:
        raise AssertionError(result.stdout)
