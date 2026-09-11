"""Tests for the first environment verification example."""

from __future__ import annotations

from pathlib import Path

from examples.hello_robot import collect_environment_info, get_project_root


def test_collect_environment_info_reports_expected_fields(tmp_path: Path) -> None:
    """The report should expose useful fields without machine-specific assertions."""

    info = collect_environment_info(tmp_path)

    assert info["message"] == "Hello Robot"
    assert info["python_version"]
    assert info["numpy_version"]
    assert Path(info["project_root"]) == tmp_path.resolve()


def test_project_root_contains_repository_files() -> None:
    """The path calculation should work from any caller working directory."""

    root = get_project_root()

    assert (root / "README.md").is_file()
    assert (root / "environment.yml").is_file()
