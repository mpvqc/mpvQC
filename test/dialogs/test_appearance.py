# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import inject
import pytest
from PySide6.QtCore import Qt

from mpvqc.appearance import (
    AccentColor,
    Appearance,
    ColorScheme,
    ColorSchemePreference,
    Dark,
    FollowSystem,
    Light,
)
from mpvqc.dialogs.appearance import (
    AppearanceDialogProps,
    MpvqcAppearanceDialogViewModel,
    derive_appearance_dialog_props,
)
from mpvqc.services import ColorSchemeService, PaletteCatalogService, ResourceService, SettingsService

SYSTEM = FollowSystem()
LIGHT = Light()
DARK = Dark()


@pytest.fixture
def style_hints(make_style_hints):
    return make_style_hints(Qt.ColorScheme.Dark)


@pytest.fixture(autouse=True)
def configure_injections(
    common_bindings_with, settings_service, style_hints, make_palette_family_data, make_resource_service
):
    light = make_palette_family_data(color_scheme="light", default_accent="#l2", accents=["#l1", "#l2"])
    dark = make_palette_family_data(color_scheme="dark", default_accent="#d1", accents=["#d1", "#d2", "#d3"])
    fake = make_resource_service(light, dark)

    def custom_bindings(binder: inject.Binder):
        binder.bind(ResourceService, fake)
        binder.bind(SettingsService, settings_service)
        binder.bind_to_constructor(PaletteCatalogService, PaletteCatalogService)
        binder.bind_to_constructor(ColorSchemeService, lambda: ColorSchemeService(style_hints))

    common_bindings_with(custom_bindings)


@pytest.fixture
def catalog() -> PaletteCatalogService:
    return inject.instance(PaletteCatalogService)


@pytest.fixture(autouse=True)
def qt_app_must_be_running(qt_app):
    pass


@pytest.fixture
def make_view_model():
    def _make() -> MpvqcAppearanceDialogViewModel:
        # noinspection PyCallingNonCallable
        return MpvqcAppearanceDialogViewModel()

    return _make


def _appearance(
    preference: ColorSchemePreference,
    *,
    light_accent: str | None = None,
    dark_accent: str | None = None,
) -> Appearance:
    return Appearance(
        color_scheme_preference=preference,
        light_accent_color=AccentColor(light_accent) if light_accent else None,
        dark_accent_color=AccentColor(dark_accent) if dark_accent else None,
    )


class DerivationCase(NamedTuple):
    name: str
    appearance: Appearance
    expected: AppearanceDialogProps


@pytest.mark.parametrize(
    "case",
    [
        DerivationCase(
            name="system offers no accent section",
            appearance=_appearance(SYSTEM),
            expected=AppearanceDialogProps(
                color_scheme_preference_index=0,
                accent_color_index=-1,
                accent_section_visible=False,
                accent_section_color_scheme=None,
            ),
        ),
        DerivationCase(
            name="system offers no accent section even with both accents stored",
            appearance=_appearance(SYSTEM, light_accent="#l1", dark_accent="#d3"),
            expected=AppearanceDialogProps(
                color_scheme_preference_index=0,
                accent_color_index=-1,
                accent_section_visible=False,
                accent_section_color_scheme=None,
            ),
        ),
        DerivationCase(
            name="light with stored accent",
            appearance=_appearance(LIGHT, light_accent="#l1"),
            expected=AppearanceDialogProps(
                color_scheme_preference_index=1,
                accent_color_index=0,
                accent_section_visible=True,
                accent_section_color_scheme=LIGHT,
            ),
        ),
        DerivationCase(
            name="light without stored accent resolves to its default",
            appearance=_appearance(LIGHT),
            expected=AppearanceDialogProps(
                color_scheme_preference_index=1,
                accent_color_index=1,
                accent_section_visible=True,
                accent_section_color_scheme=LIGHT,
            ),
        ),
        DerivationCase(
            name="light with stale accent resolves to its default",
            appearance=_appearance(LIGHT, light_accent="#gone"),
            expected=AppearanceDialogProps(
                color_scheme_preference_index=1,
                accent_color_index=1,
                accent_section_visible=True,
                accent_section_color_scheme=LIGHT,
            ),
        ),
        DerivationCase(
            name="light ignores the dark accent",
            appearance=_appearance(LIGHT, dark_accent="#d3"),
            expected=AppearanceDialogProps(
                color_scheme_preference_index=1,
                accent_color_index=1,
                accent_section_visible=True,
                accent_section_color_scheme=LIGHT,
            ),
        ),
        DerivationCase(
            name="dark with stored accent",
            appearance=_appearance(DARK, dark_accent="#d2"),
            expected=AppearanceDialogProps(
                color_scheme_preference_index=2,
                accent_color_index=1,
                accent_section_visible=True,
                accent_section_color_scheme=DARK,
            ),
        ),
        DerivationCase(
            name="dark without stored accent resolves to its default",
            appearance=_appearance(DARK),
            expected=AppearanceDialogProps(
                color_scheme_preference_index=2,
                accent_color_index=0,
                accent_section_visible=True,
                accent_section_color_scheme=DARK,
            ),
        ),
        DerivationCase(
            name="dark ignores the light accent",
            appearance=_appearance(DARK, light_accent="#l1"),
            expected=AppearanceDialogProps(
                color_scheme_preference_index=2,
                accent_color_index=0,
                accent_section_visible=True,
                accent_section_color_scheme=DARK,
            ),
        ),
    ],
    ids=lambda case: case.name,
)
def test_derivation(case: DerivationCase, catalog):
    def accent_color_index_for(color_scheme: ColorScheme, accent: AccentColor | None) -> int:
        return catalog.palette_family_for(color_scheme).palette_index(accent)

    props = derive_appearance_dialog_props(case.appearance, accent_color_index_for)

    assert props == case.expected


def test_initial_snapshot_reads_settings_at_construction(make_view_model, settings_service):
    settings_service.color_scheme_preference = LIGHT
    settings_service.set_accent_color(LIGHT, AccentColor("#l1"))

    view_model = make_view_model()

    assert view_model.colorSchemePreferenceIndex == 1
    assert view_model.accentColorIndex == 0
    assert view_model.accentSectionVisible is True
    assert view_model.accentColorModel.rowCount() == 2


def test_a_preference_write_unfolding_the_section_emits_every_changed_notify(
    make_view_model, settings_service, make_spy
):
    settings_service.set_accent_color(LIGHT, AccentColor("#l1"))
    view_model = make_view_model()
    preference_spy = make_spy(view_model.colorSchemePreferenceIndexChanged)
    accent_spy = make_spy(view_model.accentColorIndexChanged)
    visible_spy = make_spy(view_model.accentSectionVisibleChanged)
    assert view_model.accentColorModel.rowCount() == 0

    settings_service.color_scheme_preference = LIGHT

    assert preference_spy.count() == 1
    assert preference_spy.at(0, 0) == 1
    assert accent_spy.count() == 1
    assert accent_spy.at(0, 0) == 0
    assert visible_spy.count() == 1
    assert visible_spy.at(0, 0) is True
    assert view_model.accentColorModel.rowCount() == 2


def test_a_preference_write_between_two_schemes_keeps_the_section_open(make_view_model, settings_service, make_spy):
    settings_service.color_scheme_preference = LIGHT
    view_model = make_view_model()
    visible_spy = make_spy(view_model.accentSectionVisibleChanged)
    assert view_model.accentColorModel.rowCount() == 2

    settings_service.color_scheme_preference = DARK

    assert visible_spy.count() == 0
    assert view_model.accentColorModel.rowCount() == 3
    assert view_model.accentColorIndex == 0


def test_an_accent_write_for_the_selected_scheme_moves_the_accent_index(make_view_model, settings_service, make_spy):
    settings_service.color_scheme_preference = DARK
    view_model = make_view_model()
    preference_spy = make_spy(view_model.colorSchemePreferenceIndexChanged)
    accent_spy = make_spy(view_model.accentColorIndexChanged)

    settings_service.set_accent_color(DARK, AccentColor("#d3"))

    assert accent_spy.count() == 1
    assert accent_spy.at(0, 0) == 2
    assert view_model.accentColorIndex == 2
    assert preference_spy.count() == 0


def test_an_accent_write_for_the_other_scheme_emits_nothing(make_view_model, settings_service, make_spy):
    settings_service.color_scheme_preference = DARK
    view_model = make_view_model()
    preference_spy = make_spy(view_model.colorSchemePreferenceIndexChanged)
    accent_spy = make_spy(view_model.accentColorIndexChanged)

    settings_service.set_accent_color(LIGHT, AccentColor("#l1"))

    assert preference_spy.count() == 0
    assert accent_spy.count() == 0


@pytest.mark.parametrize(
    ("text", "preference", "expected_index", "expected_accent_count"),
    [
        ("system", SYSTEM, 0, 0),
        ("light", LIGHT, 1, 2),
        ("dark", DARK, 2, 3),
    ],
)
def test_set_color_scheme_preference_writes_the_setting(
    make_view_model, settings_service, text, preference, expected_index, expected_accent_count
):
    view_model = make_view_model()

    view_model.setColorSchemePreference(text)

    assert settings_service.color_scheme_preference == preference
    assert view_model.colorSchemePreferenceIndex == expected_index
    assert view_model.accentColorModel.rowCount() == expected_accent_count


def test_set_accent_color_writes_the_selected_schemes_entry_only(make_view_model, settings_service):
    settings_service.color_scheme_preference = DARK
    view_model = make_view_model()

    view_model.setAccentColor("#d2")

    assert settings_service.accent_color_for(DARK) == "#d2"
    assert settings_service.accent_color_for(LIGHT) is None
    assert view_model.accentColorIndex == 1


def test_set_accent_color_under_system_writes_nothing(make_view_model, settings_service):
    view_model = make_view_model()

    view_model.setAccentColor("#d2")

    assert settings_service.accent_color_for(DARK) is None
    assert settings_service.accent_color_for(LIGHT) is None


def test_a_desktop_flip_under_system_moves_nothing(make_view_model, style_hints, make_spy):
    inject.instance(ColorSchemeService)
    view_model = make_view_model()
    spies = [
        make_spy(view_model.colorSchemePreferenceIndexChanged),
        make_spy(view_model.accentColorIndexChanged),
        make_spy(view_model.accentSectionVisibleChanged),
    ]
    model_spy = make_spy(view_model.accentColorModel.modelReset)

    style_hints.system_reports(Qt.ColorScheme.Light)

    assert [spy.count() for spy in spies] == [0, 0, 0]
    assert model_spy.count() == 0
    assert view_model.colorSchemePreferenceIndex == 0
    assert view_model.accentSectionVisible is False
    assert view_model.accentColorModel.rowCount() == 0


def test_reject_restores_the_preference_and_both_accents(make_view_model, settings_service):
    settings_service.color_scheme_preference = DARK
    settings_service.set_accent_color(LIGHT, AccentColor("#l1"))
    view_model = make_view_model()
    assert view_model.colorSchemePreferenceIndex == 2
    assert view_model.accentColorIndex == 0

    view_model.setColorSchemePreference("light")
    view_model.setAccentColor("#l2")
    view_model.setColorSchemePreference("dark")
    view_model.setAccentColor("#d3")
    view_model.setColorSchemePreference("system")

    view_model.reject()

    assert settings_service.color_scheme_preference == DARK
    assert settings_service.accent_color_for(LIGHT) == "#l1"
    assert settings_service.accent_color_for(DARK) is None
    assert view_model.colorSchemePreferenceIndex == 2
    assert view_model.accentColorIndex == 0
    assert view_model.accentSectionVisible is True
    assert view_model.accentColorModel.rowCount() == 3
