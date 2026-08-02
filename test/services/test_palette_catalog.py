# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import asdict

import inject
import pytest
from PySide6.QtGui import QColor

from mpvqc.appearance import AccentColor, EffectiveColorScheme
from mpvqc.services import PaletteCatalogService, ResourceService


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with):
    common_bindings_with()


@pytest.fixture
def catalog():
    return PaletteCatalogService()


@pytest.fixture
def catalog_with(common_bindings_with, make_resource_service):
    def _make(*palette_families: dict) -> PaletteCatalogService:
        fake = make_resource_service(*palette_families)

        def bind_fake(binder: inject.Binder):
            binder.bind(ResourceService, fake)

        common_bindings_with(bind_fake)
        return PaletteCatalogService()

    return _make


@pytest.fixture
def fake_catalog(catalog_with, make_palette_family_data):
    light = make_palette_family_data(
        color_scheme="light",
        preview="#f0f0f0",
        default_accent="#l2",
        accents=["#l1", "#l2"],
    )
    dark = make_palette_family_data(
        color_scheme="dark",
        preview="#101010",
        default_accent="#d1",
        accents=["#d1", "#d2", "#d3"],
    )
    return catalog_with(light, dark)


@pytest.mark.parametrize(
    ("color_scheme", "default_accent"),
    [
        (EffectiveColorScheme.LIGHT, "#l2"),
        (EffectiveColorScheme.DARK, "#d1"),
    ],
    ids=["light", "dark"],
)
def test_lookup_by_color_scheme_returns_the_family_tagged_with_it(fake_catalog, color_scheme, default_accent):
    assert fake_catalog.palette_family_for(color_scheme).default_accent == default_accent


@pytest.mark.parametrize(
    ("color_scheme", "preview"),
    [
        (EffectiveColorScheme.LIGHT, "#f0f0f0"),
        (EffectiveColorScheme.DARK, "#101010"),
    ],
    ids=["light", "dark"],
)
def test_preview_color_per_color_scheme(fake_catalog, color_scheme, preview):
    assert fake_catalog.preview_color_for(color_scheme) == preview


def test_color_scheme_tag_selects_the_palette_mapping(catalog_with, make_palette_family_data):
    light = make_palette_family_data(color_scheme="light", default_accent="#a", accents=["#a"])
    dark = make_palette_family_data(color_scheme="dark", default_accent="#a", accents=["#a"])
    colors = light["palettes"][0]["colors"]
    catalog = catalog_with(light, dark)

    light_palette = catalog.palette_family_for(EffectiveColorScheme.LIGHT).palette_for(None)
    dark_palette = catalog.palette_family_for(EffectiveColorScheme.DARK).palette_for(None)

    assert light_palette.background == colors["surfaceContainerLow"]
    assert dark_palette.background == colors["surface"]


def test_palette_for_resolves_by_accent_color(fake_catalog):
    palette_family = fake_catalog.palette_family_for(EffectiveColorScheme.DARK)
    expected = palette_family.palettes[2]

    assert palette_family.palette_for(expected.accent_color) is expected


def test_palette_index_returns_position(fake_catalog):
    palette_family = fake_catalog.palette_family_for(EffectiveColorScheme.DARK)
    target = palette_family.palettes[1]

    assert palette_family.palette_index(target.accent_color) == 1


@pytest.mark.parametrize("stored", [None, AccentColor("#stale")], ids=["none", "stale"])
def test_palette_resolves_missing_and_stale_to_the_declared_default(fake_catalog, stored):
    palette_family = fake_catalog.palette_family_for(EffectiveColorScheme.LIGHT)

    assert palette_family.palette_for(stored) is palette_family.palettes[1]
    assert palette_family.palette_index(stored) == 1


def test_the_first_family_tagged_with_a_scheme_wins(catalog_with, make_palette_family_data):
    first = make_palette_family_data(color_scheme="light", default_accent="#a", accents=["#a"])
    second = make_palette_family_data(color_scheme="light", default_accent="#b", accents=["#b"])

    catalog = catalog_with(first, second)

    assert catalog.palette_family_for(EffectiveColorScheme.LIGHT).default_accent == "#a"


def test_palette_count_counts_the_accent_palettes(fake_catalog):
    assert fake_catalog.palette_family_for(EffectiveColorScheme.LIGHT).palette_count == 2
    assert fake_catalog.palette_family_for(EffectiveColorScheme.DARK).palette_count == 3


def test_shipped_light_palette_family(catalog):
    light = catalog.palette_family_for(EffectiveColorScheme.LIGHT)

    assert light.preview == "#f5f2fa"
    assert light.palette_count == 17


def test_shipped_dark_palette_family(catalog):
    dark = catalog.palette_family_for(EffectiveColorScheme.DARK)

    assert dark.preview == "#121318"
    assert dark.palette_count == 17


def test_all_palette_colors_are_valid_colors(catalog):
    for palette_family in catalog.palette_families:
        for palette in palette_family.palettes:
            for role, color_str in asdict(palette).items():
                if role == "accent_color":
                    continue

                assert QColor(color_str).isValid(), (
                    f"Invalid color '{color_str}' in the {palette_family.color_scheme} palette family "
                    f"palette '{palette.accent_color}' role '{role}'"
                )


def test_palettes_have_accent_colors(catalog):
    for palette_family in catalog.palette_families:
        for palette in palette_family.palettes:
            assert palette.accent_color, (
                f"palette in the {palette_family.color_scheme} palette family is missing an accent color"
            )


def test_every_palette_family_declares_a_default_accent_from_its_own_accent_set(catalog):
    for palette_family in catalog.palette_families:
        accent_colors = {palette.accent_color for palette in palette_family.palettes}
        assert palette_family.default_accent in accent_colors, (
            f"the {palette_family.color_scheme} palette family declares default accent "
            f"{palette_family.default_accent!r} which is not among its own accent colors"
        )
