# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: MIT

import argparse
import json
import re
import sys
from argparse import Namespace
from pathlib import Path
from typing import Literal

from materialyoucolor.dynamiccolor.dynamic_scheme import DynamicScheme
from materialyoucolor.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
from materialyoucolor.hct import Hct
from materialyoucolor.scheme.scheme_tonal_spot import SchemeTonalSpot

HEX_PATTERN = re.compile(r"^#[A-Fa-f0-9]{6}$")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create Material You color palettes")
    parser.add_argument(
        "colors",
        nargs="+",
        type=str,
        help="Seed colors",
    )
    parser.add_argument(
        "--dark",
        action="store_true",
        help="Dark palette, default: false",
    )
    parser.add_argument(
        "--contrast",
        type=float,
        help="Contrast between 0 and 1, default: 0.0",
        default=0.0,
    )
    run(parser.parse_args())


def run(args: Namespace) -> None:
    colors = args.colors
    validate_colors(colors)

    is_dark = args.dark
    contrast = args.contrast

    generate(colors, is_dark, contrast)


def validate_colors(colors: list[str]) -> None:
    errors = [color for color in colors if not HEX_PATTERN.fullmatch(color)]
    if errors:
        for color in errors:
            print(f"Invalid color: {color}")
        sys.exit(1)


def generate(colors: list[str], dark: bool, contrast: float) -> None:
    spec_version: Literal["2021", "2025"] = "2021"
    color_map = {}

    for hex_color in colors:
        seed = hex_color.lower()
        hct = Hct.from_int(int("0xff" + seed[1:], 16))
        scheme = SchemeTonalSpot(hct, dark, contrast, spec_version=spec_version)
        mdc = MaterialDynamicColors(spec=spec_version)
        color_map[seed] = generate_palette_from(scheme, mdc)

    update_palette_catalog_file(color_map, dark)


def generate_palette_from(scheme: DynamicScheme, colors: MaterialDynamicColors) -> dict[str, str]:
    result = {}

    for color in colors.all_colors:
        color_name = color.name
        r, g, b, _ = color.get_hct(scheme).to_rgba()
        color_code = f"#{r:02x}{g:02x}{b:02x}"

        result[color_name] = color_code

    return result


def update_palette_catalog_file(color_map: dict[str, dict[str, str]], dark: bool) -> None:
    path = Path() / ".." / "data" / "palette-catalog.json"
    path = path.resolve()

    with Path(path).open(encoding="utf-8") as f:
        file = json.load(f)

    color_scheme = "dark" if dark else "light"

    for idx, item in enumerate(file):
        if color_scheme == item["color_scheme"]:
            file[idx]["palettes"] = [{"identifier": seed, "colors": palette} for seed, palette in color_map.items()]

    validate_default_accent_colors(file)

    Path(path).write_text(json.dumps(file, indent=4), encoding="utf-8")


def validate_default_accent_colors(palette_families: list[dict]) -> None:
    for palette_family in palette_families:
        accent_colors = {palette["identifier"] for palette in palette_family["palettes"]}
        if palette_family["default_accent_color"] not in accent_colors:
            print(
                f"The {palette_family['color_scheme']} palette family: "
                f"default_accent_color {palette_family['default_accent_color']} is not among its accent colors"
            )
            sys.exit(1)


if __name__ == "__main__":
    main()
