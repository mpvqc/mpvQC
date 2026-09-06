# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
from dataclasses import asdict

import pytest
from PySide6.QtGui import QColor

from mpvqc.appearance.services import (
    AccentColor,
    AppearancePreference,
    Dark,
    FollowSystem,
    Light,
    NoPreference,
    PaletteCatalogService,
    read_palette_catalog,
)

SYSTEM = FollowSystem()
NO_PREFERENCE = NoPreference()


def _appearance_preference(*, light_accent: str | None = None, dark_accent: str | None = None) -> AppearancePreference:
    return AppearancePreference(
        color_scheme_preference=SYSTEM,
        light_accent_color_preference=AccentColor(light_accent) if light_accent else NO_PREFERENCE,
        dark_accent_color_preference=AccentColor(dark_accent) if dark_accent else NO_PREFERENCE,
    )


@pytest.fixture
def catalog():
    return PaletteCatalogService(read_palette_catalog())


@pytest.fixture
def catalog_with():
    def _make(*palette_families: dict) -> PaletteCatalogService:
        return PaletteCatalogService(json.dumps(palette_families))

    return _make


@pytest.fixture
def fake_catalog(catalog_with, make_palette_family_data):
    light = make_palette_family_data(
        color_scheme="light",
        preview_color="#f0f0f0",
        default_accent_color="#l2",
        accents=["#l1", "#l2"],
    )
    dark = make_palette_family_data(
        color_scheme="dark",
        preview_color="#101010",
        default_accent_color="#d1",
        accents=["#d1", "#d2", "#d3"],
    )
    return catalog_with(light, dark)


@pytest.mark.parametrize(
    ("color_scheme", "default_accent_color"),
    [
        (Light(), "#l2"),
        (Dark(), "#d1"),
    ],
    ids=["light", "dark"],
)
def test_lookup_by_color_scheme_returns_the_family_tagged_with_it(fake_catalog, color_scheme, default_accent_color):
    assert fake_catalog.palette_family_for(color_scheme).default_accent_color == AccentColor(default_accent_color)


@pytest.mark.parametrize(
    ("color_scheme", "preview_color"),
    [
        (Light(), "#f0f0f0"),
        (Dark(), "#101010"),
    ],
    ids=["light", "dark"],
)
def test_preview_color_per_color_scheme(fake_catalog, color_scheme, preview_color):
    assert fake_catalog.preview_color_for(color_scheme) == preview_color


def test_color_scheme_tag_selects_the_palette_mapping(catalog_with, make_palette_family_data):
    light = make_palette_family_data(color_scheme="light", default_accent_color="#a", accents=["#a"])
    dark = make_palette_family_data(color_scheme="dark", default_accent_color="#a", accents=["#a"])
    colors = light["palettes"][0]["colors"]
    catalog = catalog_with(light, dark)

    light_palette = catalog.palette_family_for(Light()).palette_of(_appearance_preference())
    dark_palette = catalog.palette_family_for(Dark()).palette_of(_appearance_preference())

    assert light_palette.background == colors["surfaceContainerLow"]
    assert dark_palette.background == colors["surface"]


def test_palette_of_resolves_by_accent_color(fake_catalog):
    palette_family = fake_catalog.palette_family_for(Dark())
    expected = palette_family.palettes[2]

    assert palette_family.palette_of(_appearance_preference(dark_accent="#d3")) is expected


def test_palette_index_of_returns_position(fake_catalog):
    palette_family = fake_catalog.palette_family_for(Dark())

    assert palette_family.palette_index_of(_appearance_preference(dark_accent="#d2")) == 1


def test_each_family_reads_only_its_own_schemes_accent(fake_catalog):
    appearance_preference = _appearance_preference(light_accent="#l1", dark_accent="#d3")

    assert fake_catalog.palette_family_for(Light()).palette_index_of(appearance_preference) == 0
    assert fake_catalog.palette_family_for(Dark()).palette_index_of(appearance_preference) == 2


@pytest.mark.parametrize("stored", [None, "#stale"], ids=["no-preference", "stale"])
def test_palette_resolves_missing_and_stale_to_the_declared_default(fake_catalog, stored):
    palette_family = fake_catalog.palette_family_for(Light())
    appearance_preference = _appearance_preference(light_accent=stored)

    assert palette_family.palette_of(appearance_preference) is palette_family.palettes[1]
    assert palette_family.palette_index_of(appearance_preference) == 1


def test_the_first_family_tagged_with_a_scheme_wins(catalog_with, make_palette_family_data):
    first = make_palette_family_data(color_scheme="light", default_accent_color="#a", accents=["#a"])
    second = make_palette_family_data(color_scheme="light", default_accent_color="#b", accents=["#b"])

    catalog = catalog_with(first, second)

    assert catalog.palette_family_for(Light()).default_accent_color == AccentColor("#a")


@pytest.mark.parametrize(
    ("color_scheme", "preview_color"),
    [
        (Light(), "#f5f2fa"),
        (Dark(), "#121318"),
    ],
    ids=["light", "dark"],
)
def test_shipped_palette_families(catalog, color_scheme, preview_color):
    palette_family = catalog.palette_family_for(color_scheme)

    assert palette_family.preview_color == preview_color
    assert len(palette_family.palettes) == 17


@pytest.mark.parametrize("color_scheme", [Light(), Dark()], ids=["light", "dark"])
def test_all_palette_colors_are_valid_colors(catalog, color_scheme):
    palette_family = catalog.palette_family_for(color_scheme)

    for palette in palette_family.palettes:
        for role, color_str in asdict(palette).items():
            if role == "accent_color":
                continue

            assert QColor(color_str).isValid(), (
                f"Invalid color '{color_str}' in the {palette_family.color_scheme} palette family "
                f"palette '{palette.accent_color.identifier}' role '{role}'"
            )


@pytest.mark.parametrize("color_scheme", [Light(), Dark()], ids=["light", "dark"])
def test_every_palette_carries_an_accent_color_unique_within_its_family(catalog, color_scheme):
    palette_family = catalog.palette_family_for(color_scheme)
    identifiers = [palette.accent_color.identifier for palette in palette_family.palettes]

    assert all(identifiers), f"a palette in the {palette_family.color_scheme} palette family is missing an accent color"
    assert len(set(identifiers)) == len(identifiers), (
        f"the {palette_family.color_scheme} palette family declares an accent color twice, "
        f"so it holds fewer palettes than accents"
    )


@pytest.mark.parametrize("color_scheme", [Light(), Dark()], ids=["light", "dark"])
def test_every_palette_family_declares_a_default_accent_color_from_its_own_accent_set(catalog, color_scheme):
    palette_family = catalog.palette_family_for(color_scheme)
    accent_colors = {palette.accent_color for palette in palette_family.palettes}

    assert palette_family.default_accent_color in accent_colors, (
        f"the {palette_family.color_scheme} palette family declares default accent color "
        f"{palette_family.default_accent_color!r} which is not among its own accent colors"
    )
