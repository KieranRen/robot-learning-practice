"""Check the example's numerical results, SVG geometry, and command-line output."""

from __future__ import annotations

import logging
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

from numpy.testing import assert_allclose
import pytest

from examples.coordinate_frames import build_scene, format_report, main, render_svg, write_svg

SVG = {"svg": "http://www.w3.org/2000/svg"}


def test_fixed_scene_agrees_with_hand_computed_points_and_frame_origins() -> None:
    scene = build_scene()
    assert_allclose(scene["t_wa"][:3, 3], [1, 0, 0], atol=1e-12, rtol=0)
    assert_allclose(scene["t_wb"][:3, 3], [1, 1, 0], atol=1e-12, rtol=0)
    assert_allclose(scene["p_w"], [[2, 1, 0]], atol=1e-12, rtol=0)
    assert_allclose(scene["p_reversed"], [[2, -1, 0]], atol=1e-12, rtol=0)
    assert_allclose(scene["p_b_roundtrip"], [[1, 0, 0]], atol=1e-12, rtol=0)


def test_report_exposes_matrices_points_error_and_order_warning() -> None:
    report = format_report(build_scene())
    for name in ("t_wa", "t_ab", "t_wb", "t_reversed", "p_b", "p_w",
                 "p_reversed", "p_b_roundtrip"):
        assert f"{name} =\n" in report
    assert "p_w =\n[[2. 1. 0.]]" in report
    assert "max round-trip error" in report
    assert "not a valid B -> W frame chain" in report


def test_svg_is_valid_xml_and_labels_all_frames_and_units() -> None:
    root = ET.fromstring(render_svg(build_scene()))
    assert root.tag == "{http://www.w3.org/2000/svg}svg"
    labels = [element.text for element in root.findall(".//svg:text", SVG)]
    for frame in ("W", "A", "B"):
        assert frame in labels
        assert root.find(f".//svg:g[@id='frame-{frame}']", SVG) is not None
        for axis in ("x", "y"):
            assert f"{axis}_{frame}" in labels
            line = root.find(f".//svg:line[@id='axis-{frame}-{axis}']", SVG)
            assert line is not None and "marker-end" in line.attrib
    assert "p_W = (2, 1, 0) m" in labels
    assert "reversed = (2, -1, 0) m" in labels
    assert "x_W (m)" in labels and "y_W (m)" in labels


def test_svg_point_positions_match_world_coordinates_and_grid_scale() -> None:
    root = ET.fromstring(render_svg(build_scene()))
    world = root.find(".//svg:circle[@id='point-world']", SVG)
    reversed_point = root.find(".//svg:circle[@id='point-reversed']", SVG)
    origin = root.find(".//svg:line[@id='axis-W-x']", SVG)
    unit = root.find(".//svg:line[@id='grid-x-1']", SVG)
    assert world is not None and reversed_point is not None
    assert origin is not None and unit is not None
    x0, y0 = float(origin.attrib["x1"]), float(origin.attrib["y1"])
    unit_pixels = float(unit.attrib["x1"]) - x0
    for element, expected_y in ((world, 1.0), (reversed_point, -1.0)):
        assert float(element.attrib["data-world-x"]) == pytest.approx(2)
        assert float(element.attrib["data-world-y"]) == pytest.approx(expected_y)
        assert float(element.attrib["data-world-z"]) == pytest.approx(0)
        assert (float(element.attrib["cx"]) - x0) / unit_pixels == pytest.approx(2)
        assert (y0 - float(element.attrib["cy"])) / unit_pixels == pytest.approx(expected_y)


def test_write_svg_creates_requested_parent_directory(tmp_path: Path) -> None:
    output = tmp_path / "nested" / "frames.svg"
    assert write_svg(build_scene(), output) == output
    assert ET.parse(output).getroot().tag == "{http://www.w3.org/2000/svg}svg"


def test_main_without_output_only_reports_results(tmp_path: Path, monkeypatch, caplog) -> None:
    monkeypatch.chdir(tmp_path)
    with caplog.at_level(logging.INFO):
        assert main([]) == 0
    assert "p_w =\n[[2. 1. 0.]]" in caplog.text
    assert list(tmp_path.iterdir()) == []


def test_module_command_writes_svg_at_a_path_with_spaces(tmp_path: Path) -> None:
    output = tmp_path / "results with spaces" / "frames.svg"
    result = subprocess.run(
        [sys.executable, "-B", "-m", "examples.coordinate_frames", "--output", str(output)],
        cwd=Path(__file__).resolve().parents[1], capture_output=True, text=True, check=True,
    )
    assert "p_w =\n[[2. 1. 0.]]" in result.stderr
    assert str(output) in result.stderr
    assert ET.parse(output).getroot().find(".//svg:circle[@id='point-world']", SVG) is not None
