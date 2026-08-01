# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import dataclasses

import inject
import pytest
from PySide6.QtGui import QColor

from mpvqc.appearance import AccentColor, Palette, ThemeIdentifier
from mpvqc.services import ResourceService, SettingsService, ThemeService


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with):
    common_bindings_with()


@pytest.fixture
def theme_service():
    return ThemeService()


@pytest.fixture
def theme_service_with(common_bindings_with, make_resource_service):
    def _make(*themes: dict) -> ThemeService:
        fake = make_resource_service(*themes)

        def bind_fake(binder: inject.Binder):
            binder.bind(ResourceService, fake)

        common_bindings_with(bind_fake)
        return ThemeService()

    return _make


def test_material_you_theme(theme_service):
    material_you = next(t for t in theme_service.themes if t.identifier == "material-you")

    assert material_you.name == "Material You"
    assert material_you.preview == "#f5f2fa"
    assert material_you.is_dark is False
    assert len(material_you.palettes) == 17

    assert theme_service.theme_index(ThemeIdentifier("material-you")) == 0

    assert theme_service.theme(ThemeIdentifier("material-you")).palette_count == 17


def test_material_you_dark_theme(theme_service):
    material_you_dark = next(t for t in theme_service.themes if t.identifier == "material-you-dark")

    assert material_you_dark.name == "Material You Dark"
    assert material_you_dark.preview == "#121318"
    assert material_you_dark.is_dark is True
    assert len(material_you_dark.palettes) == 17

    assert theme_service.theme_index(ThemeIdentifier("material-you-dark")) == 1

    assert theme_service.theme(ThemeIdentifier("material-you-dark")).palette_count == 17


def test_theme_falls_back_to_default_theme_for_unknown_identifier(theme_service):
    assert theme_service.theme(ThemeIdentifier("does-not-exist")).identifier == "material-you-dark"


def test_theme_index_falls_back_to_default_theme_for_unknown_identifier(theme_service):
    assert theme_service.theme_index(ThemeIdentifier("does-not-exist")) == 1


def test_all_palette_colors_are_valid_colors(theme_service):
    color_attrs = [field.name for field in dataclasses.fields(Palette) if field.name != "accent_color"]

    for theme in theme_service.themes:
        for palette in theme.palettes:
            for attr in color_attrs:
                color_str = getattr(palette, attr)
                color = QColor(color_str)

                assert color.isValid(), (
                    f"Invalid color '{color_str}' in theme '{theme.identifier}' "
                    f"palette '{palette.accent_color}' attribute '{attr}'"
                )


def test_palettes_have_accent_colors(theme_service):
    for theme in theme_service.themes:
        for palette in theme.palettes:
            assert palette.accent_color, f"palette in theme {theme.identifier!r} is missing an accent color"


def test_palette_for_resolves_by_accent_color(theme_service):
    theme = theme_service.theme(ThemeIdentifier("material-you"))
    expected = theme.palettes[3]

    assert theme.palette_for(expected.accent_color) is expected


def test_palette_index_returns_position(theme_service):
    theme = theme_service.theme(ThemeIdentifier("material-you"))
    target = theme.palettes[7]

    assert theme.palette_index(target.accent_color) == 7


@pytest.mark.parametrize("stored", [None, AccentColor("#stale")], ids=["none", "stale"])
def test_palette_for_resolves_missing_and_stale_to_declared_default(theme_service_with, make_theme_data, stored):
    service = theme_service_with(make_theme_data(default_accent="#222222", accents=["#111111", "#222222"]))
    theme = service.themes[0]

    assert theme.palette_for(stored) is theme.palettes[1]


@pytest.mark.parametrize("stored", [None, AccentColor("#stale")], ids=["none", "stale"])
def test_palette_index_resolves_missing_and_stale_to_declared_default(theme_service_with, make_theme_data, stored):
    service = theme_service_with(make_theme_data(default_accent="#222222", accents=["#111111", "#222222"]))
    theme = service.themes[0]

    assert theme.palette_index(stored) == 1


def test_shipped_themes_declare_the_global_default_accent(theme_service):
    default = SettingsService.primary_color.default

    for theme in theme_service.themes:
        assert theme.default_accent == default, (
            f"theme {theme.identifier!r} declares {theme.default_accent!r} instead of the global default {default!r}"
        )


def test_every_theme_declares_a_default_accent_from_its_own_accent_set(theme_service):
    for theme in theme_service.themes:
        accent_colors = {palette.accent_color for palette in theme.palettes}
        assert theme.default_accent in accent_colors, (
            f"theme {theme.identifier!r} declares default accent {theme.default_accent!r} "
            f"which is not among its own accent colors"
        )
