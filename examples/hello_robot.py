"""Report the minimal Python environment used by this repository."""

from __future__ import annotations

import logging
import platform
from pathlib import Path

import numpy as np

LOGGER = logging.getLogger(__name__)


def get_project_root() -> Path:
    """Return the repository root without depending on the current directory."""

    return Path(__file__).resolve().parents[1]


def collect_environment_info(project_root: Path | None = None) -> dict[str, str]:
    """Collect stable environment fields for display and automated tests."""

    root = (project_root or get_project_root()).resolve()
    return {
        "message": "Hello Robot",
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "project_root": str(root),
    }


def main() -> None:
    """Print a short environment report for a new contributor."""

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    info = collect_environment_info()
    LOGGER.info(info["message"])
    LOGGER.info("Python version: %s", info["python_version"])
    LOGGER.info("NumPy version: %s", info["numpy_version"])
    LOGGER.info("Project root: %s", info["project_root"])


if __name__ == "__main__":
    main()
