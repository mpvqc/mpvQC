# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import dataclasses

import pytest
from PySide6.QtGui import QColor

from mpvqc.services import SettingsService, ThemeService
from mpvqc.services.theme import ThemePalette


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with):
    common_bindings_with()


@pytest.fixture
def theme_service():
    return ThemeService()


def test_material_you_theme(theme_service):
    material_you = next(t for t in theme_service.previews if t.identifier == "material-you")

    assert material_you.name == "Material You"
    assert material_you.preview == "#f5f2fa"
    assert material_you.is_dark is False
    assert len(material_you.palettes) == 17

    assert theme_service.theme_index("material-you") == 0

    assert theme_service.theme("material-you").palette_count == 17


def test_material_you_dark_theme(theme_service):
    material_you_dark = next(t for t in theme_service.previews if t.identifier == "material-you-dark")

    assert material_you_dark.name == "Material You Dark"
    assert material_you_dark.preview == "#121318"
    assert material_you_dark.is_dark is True
    assert len(material_you_dark.palettes) == 17

    assert theme_service.theme_index("material-you-dark") == 1

    assert theme_service.theme("material-you-dark").palette_count == 17


def test_all_palette_colors_are_valid_colors(theme_service):
    color_attrs = [field.name for field in dataclasses.fields(ThemePalette) if field.name != "identifier"]

    for theme in theme_service.previews:
        for palette in theme.palettes:
            for attr in color_attrs:
                color_str = getattr(palette, attr)
                color = QColor(color_str)

                assert color.isValid(), (
                    f"Invalid color '{color_str}' in theme '{theme.identifier}' "
                    f"palette '{palette.identifier}' attribute '{attr}'"
                )


def test_palettes_have_identifiers(theme_service):
    for theme in theme_service.previews:
        for palette in theme.palettes:
            assert palette.identifier, f"palette in theme {theme.identifier!r} is missing an identifier"


def test_palette_for_resolves_by_identifier(theme_service):
    theme = theme_service.theme("material-you")
    expected = theme.palettes[3]

    assert theme.palette_for(expected.identifier) is expected


def test_palette_for_falls_back_to_first_when_unknown(theme_service):
    theme = theme_service.theme("material-you")

    assert theme.palette_for("#unknown") is theme.palettes[0]


def test_palette_index_returns_position(theme_service):
    theme = theme_service.theme("material-you")
    target = theme.palettes[7]

    assert theme.palette_index(target.identifier) == 7


def test_palette_index_falls_back_to_zero_when_unknown(theme_service):
    assert theme_service.theme("material-you").palette_index("#unknown") == 0


def test_default_primary_color_exists_in_every_theme(theme_service):
    default = SettingsService.primary_color.default

    for theme in theme_service.previews:
        identifiers = {palette.identifier for palette in theme.palettes}
        assert default in identifiers, f"default primary_color {default!r} is missing from theme {theme.identifier!r}"
