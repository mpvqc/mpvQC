# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: MIT

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from materialyoucolor.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
from materialyoucolor.hct import Hct
from materialyoucolor.scheme.dynamic_scheme import DynamicScheme
from materialyoucolor.scheme.scheme_tonal_spot import SchemeTonalSpot

HEX_PATTERN = re.compile(r"^#[A-Fa-f0-9]{6}$")


@dataclass(frozen=True)
class Color:
    name: str
    value: str


@dataclass(frozen=True)
class MpvqcColorSet:
    background: str
    backgroundAlternate: str
    foreground: str
    foregroundAlternate: str
    control: str
    rowHighlight: str
    rowHighlightText: str
    rowBase: str
    rowBaseText: str
    rowBaseAlternate: str
    rowBaseAlternateText: str


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
        help="Contrast between 0 and 1, default: 1/3",
        default=1 / 3,
    )
    run(parser.parse_args())


def run(args) -> None:
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
    color_map = {}

    for hex_color in colors:
        hct = Hct.from_int(int("0xff" + hex_color[1:], 16))
        scheme = SchemeTonalSpot(hct, dark, contrast)
        color_map[hex_color] = generate_palette_from(scheme)

    mpvqc_colors = map_to_mpvqc_colors(color_map, dark)
    update_theme_file(mpvqc_colors, dark)


def generate_palette_from(scheme: DynamicScheme) -> dict:
    colors = {}

    for attribute in sorted(vars(MaterialDynamicColors).keys()):
        attribute_value = getattr(MaterialDynamicColors, attribute)

        is_color = hasattr(attribute_value, "get_hct")
        is_palette_key_color = bool("_paletteKeyColor" in attribute)

        if is_color and not is_palette_key_color:
            r, g, b, _ = attribute_value.get_hct(scheme).to_rgba()
            color = Color(attribute, f"#{r:02x}{g:02x}{b:02x}")

            if color.name in colors:
                msg = f"Duplicate color name: {color.name}"
                raise ValueError(msg)

            colors[color.name] = color.value

    return colors


def map_to_mpvqc_colors(color_map: dict, dark: bool):
    colors = []
    for palette in color_map.values():
        if dark:
            colors.append(
                MpvqcColorSet(
                    background=palette["surface"],
                    backgroundAlternate=palette["surfaceContainerHigh"],
                    foreground=palette["onSurfaceVariant"],
                    foregroundAlternate=palette["onSurfaceVariant"],
                    control=palette["primary"],
                    rowHighlight=palette["inversePrimary"],
                    rowHighlightText=palette["onSurface"],
                    rowBase=palette["surface"],
                    rowBaseText=palette["onSurfaceVariant"],
                    rowBaseAlternate=palette["surfaceContainerLow"],
                    rowBaseAlternateText=palette["onSurfaceVariant"],
                )
            )
        else:
            colors.append(
                MpvqcColorSet(
                    background=palette["surfaceContainerLow"],
                    backgroundAlternate=palette["secondaryContainer"],
                    foreground=palette["onSurfaceVariant"],
                    foregroundAlternate=palette["onSecondaryContainer"],
                    control=palette["secondary"],
                    rowHighlight=palette["primary"],
                    rowHighlightText=palette["onPrimary"],
                    rowBase=palette["surfaceContainerLow"],
                    rowBaseText=palette["onSurfaceVariant"],
                    rowBaseAlternate=palette["surfaceContainerHighest"],
                    rowBaseAlternateText=palette["onSurfaceVariant"],
                )
            )
    return colors


def update_theme_file(colors: list[MpvqcColorSet], dark: bool) -> None:
    path = Path() / ".." / ".." / "data" / "themes.json"
    path = path.resolve()

    with Path(path).open(encoding="utf-8") as f:
        file = json.load(f)

    theme = "material-you-dark" if dark else "material-you"

    for idx, item in enumerate(file):
        if theme == item["identifier"]:
            file[idx]["palettes"] = [asdict(c) for c in colors]

    with Path(path).open("w", encoding="utf-8") as f:
        f.write(json.dumps(file, indent=4))


if __name__ == "__main__":
    main()
