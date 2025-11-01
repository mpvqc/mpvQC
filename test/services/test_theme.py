# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest
from PySide6.QtGui import QColor

from mpvqc.services import ResourceReaderService, ThemeService


@pytest.fixture
def theme_service():
    def configure(binder):
        binder.bind(ResourceReaderService, ResourceReaderService())

    inject.clear_and_configure(configure)
    service = ThemeService()
    yield service
    inject.clear()


def test_material_you_theme(theme_service):
    material_you = next(t for t in theme_service.previews if t["identifier"] == "material-you")

    assert material_you["name"] == "Material You"
    assert material_you["preview"] == "#f4f4e9"
    assert material_you["isDark"] is False
    assert len(material_you["palettes"]) == 15

    assert theme_service.index("material-you") == 0

    palettes = theme_service.palette("material-you")
    assert len(palettes) == 15


def test_material_you_dark_theme(theme_service):
    material_you_dark = next(t for t in theme_service.previews if t["identifier"] == "material-you-dark")

    assert material_you_dark["name"] == "Material You Dark"
    assert material_you_dark["preview"] == "#121212"
    assert material_you_dark["isDark"] is True
    assert len(material_you_dark["palettes"]) == 15

    assert theme_service.index("material-you-dark") == 1

    palettes = theme_service.palette("material-you-dark")
    assert len(palettes) == 15


def test_all_palette_colors_are_valid_colors(theme_service):
    color_keys = [
        "background",
        "foreground",
        "control",
        "rowHighlight",
        "rowHighlightText",
        "rowBase",
        "rowBaseText",
        "rowBaseAlternate",
        "rowBaseAlternateText",
    ]

    for theme in theme_service.previews:
        palettes = theme_service.palette(theme["identifier"])

        for palette_idx, palette in enumerate(palettes):
            for color_key in color_keys:
                color_str = palette[color_key]
                color = QColor(color_str)

                assert color.isValid(), (
                    f"Invalid color '{color_str}' in theme '{theme['identifier']}' "
                    f"palette {palette_idx} key '{color_key}'"
                )
