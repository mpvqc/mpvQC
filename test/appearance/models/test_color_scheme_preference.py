# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest
from PySide6.QtTest import QAbstractItemModelTester

from mpvqc.appearance.domain import AccentColor, Appearance, ColorScheme, Dark, FollowSystem, Light, NoPreference
from mpvqc.appearance.models import MpvqcColorSchemePreferenceModel
from mpvqc.appearance.services.color_scheme import ColorSchemeService
from mpvqc.appearance.services.palette_catalog import PaletteCatalogService
from mpvqc.services import ResourceService, SettingsService

SYSTEM = FollowSystem()
LIGHT = Light()
DARK = Dark()
NO_PREFERENCE = NoPreference()

LIGHT_PREVIEW = "#lightpreview"
DARK_PREVIEW = "#darkpreview"


@pytest.fixture
def style_hints(make_style_hints):
    return make_style_hints(DARK)


@pytest.fixture(autouse=True)
def configure_injections(
    common_bindings_with, settings_service, style_hints, make_palette_family_data, make_resource_service
):
    light = make_palette_family_data(
        color_scheme="light", preview=LIGHT_PREVIEW, default_accent="#l2", accents=["#l1", "#l2"]
    )
    dark = make_palette_family_data(
        color_scheme="dark", preview=DARK_PREVIEW, default_accent="#d1", accents=["#d1", "#d2", "#d3"]
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


def _badge(catalog: PaletteCatalogService, color_scheme: ColorScheme, accent: str | None) -> str:
    preference = AccentColor(accent) if accent else NO_PREFERENCE
    appearance = Appearance(
        color_scheme_preference=SYSTEM,
        light_accent_color_preference=preference,
        dark_accent_color_preference=preference,
    )
    return catalog.palette_family_for(color_scheme).palette_of(appearance).row_selected


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


def test_previews_come_from_the_catalog_and_system_carries_both(make_model):
    model = make_model()

    previews = [_read(model, row, MpvqcColorSchemePreferenceModel.PreviewRole) for row in range(3)]
    alternates = [_read(model, row, MpvqcColorSchemePreferenceModel.AlternatePreviewRole) for row in range(3)]

    assert previews == [LIGHT_PREVIEW, LIGHT_PREVIEW, DARK_PREVIEW]
    assert alternates == [DARK_PREVIEW, "", ""]


def test_accents_render_each_schemes_stored_pick_and_system_carries_none(make_model, settings_service, catalog):
    settings_service.set_accent_color_preference(LIGHT, AccentColor("#l1"))
    settings_service.set_accent_color_preference(DARK, AccentColor("#d3"))
    model = make_model()

    accents = [_read(model, row, MpvqcColorSchemePreferenceModel.AccentRole) for row in range(3)]

    assert accents == ["", _badge(catalog, LIGHT, "#l1"), _badge(catalog, DARK, "#d3")]


def test_an_unstored_accent_renders_the_palette_familys_default(make_model, catalog):
    model = make_model()

    assert _read(model, 1, MpvqcColorSchemePreferenceModel.AccentRole) == _badge(catalog, LIGHT, None)
    assert _read(model, 2, MpvqcColorSchemePreferenceModel.AccentRole) == _badge(catalog, DARK, None)


def test_an_accent_write_changes_only_its_own_row(make_model, settings_service, catalog, make_spy):
    model = make_model()
    spy = make_spy(model.dataChanged)

    settings_service.set_accent_color_preference(LIGHT, AccentColor("#l1"))

    assert spy.count() == 1
    assert spy.at(0, 0).row() == 1
    assert spy.at(0, 1).row() == 1
    assert spy.at(0, 2) == [MpvqcColorSchemePreferenceModel.AccentRole]
    assert _read(model, 1, MpvqcColorSchemePreferenceModel.AccentRole) == _badge(catalog, LIGHT, "#l1")


def test_a_preference_write_leaves_the_rows_alone(make_model, settings_service, make_spy):
    model = make_model()
    spy = make_spy(model.dataChanged)

    settings_service.color_scheme_preference = LIGHT

    assert spy.count() == 0


def test_a_desktop_flip_under_system_leaves_the_badges_alone(make_model, style_hints, catalog, make_spy):
    inject.instance(ColorSchemeService)
    model = make_model()
    before = [_read(model, row, MpvqcColorSchemePreferenceModel.AccentRole) for row in range(3)]
    spy = make_spy(model.dataChanged)

    style_hints.system_reports(LIGHT)

    assert spy.count() == 0
    assert [_read(model, row, MpvqcColorSchemePreferenceModel.AccentRole) for row in range(3)] == before


def test_accent_writes_satisfy_the_item_model_protocol(make_model, settings_service):
    model = make_model()
    QAbstractItemModelTester(model, QAbstractItemModelTester.FailureReportingMode.Fatal, model)

    settings_service.set_accent_color_preference(LIGHT, AccentColor("#l1"))
    settings_service.set_accent_color_preference(DARK, AccentColor("#d3"))
    settings_service.set_accent_color_preference(LIGHT, NO_PREFERENCE)
