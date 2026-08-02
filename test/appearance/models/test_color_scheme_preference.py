# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest
from PySide6.QtTest import QAbstractItemModelTester

from mpvqc.appearance.domain import (
    AccentColor,
    AppearancePreference,
    ColorScheme,
    Dark,
    FollowSystem,
    Light,
    NoPreference,
)
from mpvqc.appearance.models import MpvqcColorSchemePreferenceModel
from mpvqc.appearance.services import ColorSchemeService, PaletteCatalogService
from mpvqc.services import ResourceService, SettingsService

SYSTEM = FollowSystem()
LIGHT = Light()
DARK = Dark()
NO_PREFERENCE = NoPreference()

LIGHT_PREVIEW_COLOR = "#lightpreviewcolor"
DARK_PREVIEW_COLOR = "#darkpreviewcolor"


@pytest.fixture
def style_hints(make_style_hints):
    return make_style_hints(DARK)


@pytest.fixture(autouse=True)
def configure_injections(
    common_bindings_with, settings_service, style_hints, make_palette_family_data, make_resource_service
):
    light = make_palette_family_data(
        color_scheme="light", preview_color=LIGHT_PREVIEW_COLOR, default_accent_color="#l2", accents=["#l1", "#l2"]
    )
    dark = make_palette_family_data(
        color_scheme="dark", preview_color=DARK_PREVIEW_COLOR, default_accent_color="#d1", accents=["#d1", "#d2", "#d3"]
    )
    fake = make_resource_service(light, dark)

    def custom_bindings(binder: inject.Binder):
        binder.bind(ResourceService, fake)
        binder.bind(SettingsService, settings_service)
        binder.bind_to_constructor(PaletteCatalogService, PaletteCatalogService)
        binder.bind_to_constructor(ColorSchemeService, lambda: ColorSchemeService(style_hints))

    common_bindings_with(custom_bindings)


@pytest.fixture(autouse=True)
def qt_app_must_be_running(qt_app):
    pass


@pytest.fixture
def catalog() -> PaletteCatalogService:
    return inject.instance(PaletteCatalogService)


@pytest.fixture
def make_model():
    def _make() -> MpvqcColorSchemePreferenceModel:
        # noinspection PyCallingNonCallable
        return MpvqcColorSchemePreferenceModel()

    return _make


def _read(model: MpvqcColorSchemePreferenceModel, row: int, role: int):
    return model.data(model.index(row), role)


def _badge(catalog: PaletteCatalogService, color_scheme: ColorScheme, accent_color: str | None) -> str:
    preference = AccentColor(accent_color) if accent_color else NO_PREFERENCE
    appearance_preference = AppearancePreference(
        color_scheme_preference=SYSTEM,
        light_accent_color_preference=preference,
        dark_accent_color_preference=preference,
    )
    return catalog.palette_family_for(color_scheme).palette_of(appearance_preference).row_selected


def test_the_model_offers_the_three_preferences_in_order(make_model):
    model = make_model()

    assert model.rowCount() == 3
    assert [_read(model, row, MpvqcColorSchemePreferenceModel.PreferenceRole) for row in range(3)] == [
        "system",
        "light",
        "dark",
    ]


def test_every_row_is_captioned(make_model):
    model = make_model()

    assert [_read(model, row, MpvqcColorSchemePreferenceModel.CaptionRole) for row in range(3)] == [
        "System",
        "Light",
        "Dark",
    ]


def test_preview_colors_come_from_the_catalog_and_system_carries_both(make_model):
    model = make_model()

    preview_colors = [_read(model, row, MpvqcColorSchemePreferenceModel.PreviewColorRole) for row in range(3)]
    alternate_preview_colors = [
        _read(model, row, MpvqcColorSchemePreferenceModel.AlternatePreviewColorRole) for row in range(3)
    ]

    assert preview_colors == [LIGHT_PREVIEW_COLOR, LIGHT_PREVIEW_COLOR, DARK_PREVIEW_COLOR]
    assert alternate_preview_colors == [DARK_PREVIEW_COLOR, "", ""]


def test_badges_render_each_schemes_stored_pick_and_system_carries_none(make_model, settings_service, catalog):
    settings_service.set_accent_color_preference(LIGHT, AccentColor("#l1"))
    settings_service.set_accent_color_preference(DARK, AccentColor("#d3"))
    model = make_model()

    accent_preview_colors = [
        _read(model, row, MpvqcColorSchemePreferenceModel.AccentPreviewColorRole) for row in range(3)
    ]

    assert accent_preview_colors == ["", _badge(catalog, LIGHT, "#l1"), _badge(catalog, DARK, "#d3")]


def test_an_unstored_accent_renders_the_palette_familys_default(make_model, catalog):
    model = make_model()

    assert _read(model, 1, MpvqcColorSchemePreferenceModel.AccentPreviewColorRole) == _badge(catalog, LIGHT, None)
    assert _read(model, 2, MpvqcColorSchemePreferenceModel.AccentPreviewColorRole) == _badge(catalog, DARK, None)


def test_an_accent_write_changes_only_its_own_row(make_model, settings_service, catalog, make_spy):
    model = make_model()
    spy = make_spy(model.dataChanged)

    settings_service.set_accent_color_preference(LIGHT, AccentColor("#l1"))

    assert spy.count() == 1
    assert spy.at(0, 0).row() == 1
    assert spy.at(0, 1).row() == 1
    assert spy.at(0, 2) == [MpvqcColorSchemePreferenceModel.AccentPreviewColorRole]
    assert _read(model, 1, MpvqcColorSchemePreferenceModel.AccentPreviewColorRole) == _badge(catalog, LIGHT, "#l1")


def test_a_preference_write_leaves_the_rows_alone(make_model, settings_service, make_spy):
    model = make_model()
    spy = make_spy(model.dataChanged)

    settings_service.color_scheme_preference = LIGHT

    assert spy.count() == 0


def test_a_desktop_flip_under_system_leaves_the_badges_alone(make_model, style_hints, catalog, make_spy):
    inject.instance(ColorSchemeService)
    model = make_model()
    before = [_read(model, row, MpvqcColorSchemePreferenceModel.AccentPreviewColorRole) for row in range(3)]
    spy = make_spy(model.dataChanged)

    style_hints.system_reports(LIGHT)

    assert spy.count() == 0
    assert [_read(model, row, MpvqcColorSchemePreferenceModel.AccentPreviewColorRole) for row in range(3)] == before


def test_accent_writes_satisfy_the_item_model_protocol(make_model, settings_service):
    model = make_model()
    QAbstractItemModelTester(model, QAbstractItemModelTester.FailureReportingMode.Fatal, model)

    settings_service.set_accent_color_preference(LIGHT, AccentColor("#l1"))
    settings_service.set_accent_color_preference(DARK, AccentColor("#d3"))
    settings_service.set_accent_color_preference(LIGHT, NO_PREFERENCE)
