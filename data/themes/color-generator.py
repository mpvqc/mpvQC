# Copyright 2024
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import re
import sys
from dataclasses import dataclass

from materialyoucolor.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
from materialyoucolor.hct import Hct
from materialyoucolor.scheme.dynamic_scheme import DynamicScheme
from materialyoucolor.scheme.scheme_tonal_spot import SchemeTonalSpot

HEX_PATTERN = re.compile(r"^#[A-Fa-f0-9]{6}$")


@dataclass(frozen=True)
class Color:
    name: str
    value: str


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

    for hex_color, palette in color_map.items():
        print(f"[[colors]]  # base color: {hex_color}")
        for color in palette:
            print(f'{color.name} = "{color.value}"')
        print()


def generate_palette_from(scheme: DynamicScheme) -> list[Color]:
    colors = []

    for attribute in sorted(vars(MaterialDynamicColors).keys()):
        attribute_value = getattr(MaterialDynamicColors, attribute)

        is_color = hasattr(attribute_value, "get_hct")
        is_palette_key_color = bool("_paletteKeyColor" in attribute)

        if is_color and not is_palette_key_color:
            r, g, b, _ = attribute_value.get_hct(scheme).to_rgba()
            color = Color(attribute, f"#{r:02x}{g:02x}{b:02x}")
            colors.append(color)

    return colors


if __name__ == "__main__":
    main()
