"""Inspect a hand-checkable coordinate chain and optionally save an XY SVG."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Sequence
import xml.etree.ElementTree as ET

import numpy as np
from numpy.typing import NDArray

from algorithms.geometry import (
    inverse_transform,
    make_transform,
    rotation_z,
    transform_points,
)

FloatArray = NDArray[np.float64]
LOGGER = logging.getLogger(__name__)


def build_scene() -> dict[str, FloatArray]:
    """Compute the fixed W/A/B example, reversed product, and round trip."""

    t_wa = make_transform(rotation_z(np.pi / 2), [1.0, 0.0, 0.0])
    t_ab = make_transform(rotation_z(-np.pi / 2), [1.0, 0.0, 0.0])
    p_b = np.array([[1.0, 0.0, 0.0]])
    # Matched adjacent subscripts give a valid B -> A -> W coordinate chain.
    t_wb = t_wa @ t_ab
    p_w = transform_points(t_wb, p_b)
    # These subscripts do not match: this is only a numerical counterexample.
    t_reversed = t_ab @ t_wa
    return {
        "t_wa": t_wa,
        "t_ab": t_ab,
        "t_wb": t_wb,
        "t_reversed": t_reversed,
        "p_b": p_b,
        "p_w": p_w,
        "p_reversed": transform_points(t_reversed, p_b),
        "p_b_roundtrip": transform_points(inverse_transform(t_wb), p_w),
    }


def format_report(scene: dict[str, FloatArray]) -> str:
    """Format observable matrices, coordinates, and the maximum round-trip error."""

    lines = ["Right-handed frames; positions in m; angles in rad."]
    for name in ("t_wa", "t_ab", "t_wb", "t_reversed", "p_b", "p_w",
                 "p_reversed", "p_b_roundtrip"):
        lines.append(f"{name} =\n{np.array2string(scene[name], precision=6, suppress_small=True)}")
    error = float(np.max(np.abs(scene["p_b_roundtrip"] - scene["p_b"])))
    lines.append(f"max round-trip error = {error:.3e} m")
    lines.append("t_wb = t_wa @ t_ab; the reversed product is not a valid B -> W frame chain.")
    return "\n".join(lines)


def render_svg(scene: dict[str, FloatArray]) -> str:
    """Draw the fixed planar scene using its computed frame origins and points."""

    svg = ET.Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg", "width": "960", "height": "640",
        "viewBox": "0 0 960 640", "role": "img", "aria-labelledby": "title description",
    })
    ET.SubElement(svg, "title", id="title").text = "Coordinate frames W, A and B"
    ET.SubElement(svg, "desc", id="description").text = (
        "XY slice in metres. Positive z points out of the page. "
        "The computed point in W is compared with an incorrectly reversed matrix product."
    )
    ET.SubElement(svg, "rect", width="960", height="640", fill="white")
    content = ET.SubElement(svg, "g", {"font-family": "sans-serif", "fill": "#0f172a"})

    def text(x: float, y: float, value: str, size: int = 15, **attrs: str) -> None:
        element = ET.SubElement(content, "text", {
            "x": f"{x:g}", "y": f"{y:g}", "font-size": str(size), **attrs,
        })
        element.text = value

    def xy(point: FloatArray) -> tuple[float, float]:
        # SVG y increases downward, unlike the displayed right-handed XY axes.
        return 140.0 + 160.0 * float(point[0]), 340.0 - 160.0 * float(point[1])

    def coordinates(point: FloatArray) -> str:
        return "(" + ", ".join(f"{float(value):.6g}" for value in point) + ")"

    text(32, 38, "Coordinate frames: W / A / B", 26)
    text(32, 68, "XY slice | right-handed frames | positions: m | angles: rad | +z out of page", 15)
    ET.SubElement(content, "rect", {
        "x": "70", "y": "100", "width": "555", "height": "465",
        "rx": "8", "fill": "#f8fafc", "stroke": "#cbd5e1",
    })
    for tick in (0, 1, 2):
        x, _ = xy(np.array([tick, 0]))
        ET.SubElement(content, "line", {
            "id": f"grid-x-{tick}", "x1": f"{x:g}", "x2": f"{x:g}",
            "y1": "105", "y2": "550", "stroke": "#e2e8f0",
        })
        text(x - 4, 585, str(tick), 13)
    for tick in (-1, 0, 1):
        _, y = xy(np.array([0, tick]))
        ET.SubElement(content, "line", {
            "x1": "85", "x2": "615", "y1": f"{y:g}", "y2": f"{y:g}",
            "stroke": "#e2e8f0",
        })
        text(40, y + 5, str(tick), 13)
    text(550, 585, "x_W (m)", 13)
    text(22, 97, "y_W (m)", 13)
    definitions = ET.SubElement(svg, "defs")
    frames = (("W", np.eye(4), "#334155"),
              ("A", scene["t_wa"], "#2563eb"),
              ("B", scene["t_wb"], "#9333ea"))
    for name, transform, color in frames:
        marker = ET.SubElement(definitions, "marker", {
            "id": f"arrow-{name}", "viewBox": "0 0 10 10", "refX": "9", "refY": "5",
            "markerWidth": "5", "markerHeight": "5", "orient": "auto-start-reverse",
        })
        ET.SubElement(marker, "path", d="M 0 0 L 10 5 L 0 10 z", fill=color)
        origin = transform[:3, 3]
        origin_x, origin_y = xy(origin)
        group = ET.SubElement(content, "g", id=f"frame-{name}")
        ET.SubElement(group, "circle", {
            "cx": f"{origin_x:g}", "cy": f"{origin_y:g}", "r": "4", "fill": color,
        })
        for index, axis in enumerate(("x", "y")):
            endpoint = origin + 0.42 * transform[:3, index]
            end_x, end_y = xy(endpoint)
            ET.SubElement(group, "line", {
                "id": f"axis-{name}-{axis}", "x1": f"{origin_x:g}", "y1": f"{origin_y:g}",
                "x2": f"{end_x:g}", "y2": f"{end_y:g}", "stroke": color,
                "stroke-width": "3", "marker-end": f"url(#arrow-{name})",
            })
            label_y = end_y + 21 if name == "A" and axis == "y" else end_y - 7
            text(end_x + 7, label_y, f"{axis}_{name}", 14, fill=color)
        text(origin_x - 8, origin_y + 25, name, 18, fill=color)

    for key, identifier, color in (("p_w", "point-world", "#047857"),
                                   ("p_reversed", "point-reversed", "#c2410c")):
        point = scene[key][0]
        point_x, point_y = xy(point)
        ET.SubElement(content, "circle", {
            "id": identifier, "cx": f"{point_x:g}", "cy": f"{point_y:g}", "r": "7",
            "fill": color, "data-world-x": f"{float(point[0]):.12g}",
            "data-world-y": f"{float(point[1]):.12g}", "data-world-z": f"{float(point[2]):.12g}",
        })
        label = "p_W" if key == "p_w" else "reversed order"
        text(point_x + 13, point_y + 5, label, 14, fill=color)

    text(655, 125, "Computed scene", 20)
    lines = [
        "T_wa: Rz(+pi/2), t=(1,0,0) m",
        "T_ab: Rz(-pi/2), t=(1,0,0) m",
        f"A in W: {coordinates(scene['t_wa'][:3, 3])} m",
        f"B in W: {coordinates(scene['t_wb'][:3, 3])} m",
        f"p_B = {coordinates(scene['p_b'][0])} m",
        f"p_W = {coordinates(scene['p_w'][0])} m",
        f"reversed = {coordinates(scene['p_reversed'][0])} m",
    ]
    for index, line in enumerate(lines):
        text(655, 162 + 33 * index, line, 14)
    error = float(np.max(np.abs(scene["p_b_roundtrip"] - scene["p_b"])))
    text(655, 425, "Max round-trip error", 16)
    text(655, 453, f"{error:.3e} m", 20)
    text(655, 495, "T_wa @ T_ab matches subscripts.", 13)
    text(655, 522, "The reversed product is a numeric", 13)
    text(655, 543, "counterexample, not a frame chain.", 13)
    text(32, 620, "Planar illustration of rigid transforms; no robot model or simulator is used.", 14)
    ET.indent(svg, space="  ")
    return ET.tostring(svg, encoding="unicode", xml_declaration=False) + "\n"


def write_svg(scene: dict[str, FloatArray], output: Path) -> Path:
    """Write a UTF-8 SVG, creating the requested parent directories."""

    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_svg(scene), encoding="utf-8")
    return output


def main(argv: Sequence[str] | None = None) -> int:
    """Print the fixed example and save its SVG when --output is supplied."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional output SVG path")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    scene = build_scene()
    LOGGER.info("%s", format_report(scene))
    if args.output is not None:
        LOGGER.info("SVG written to %s", write_svg(scene, args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
