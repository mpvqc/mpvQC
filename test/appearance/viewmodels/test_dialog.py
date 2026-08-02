# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import inject
import pytest

from mpvqc.appearance.domain import (
    AccentColor,
    Appearance,
    ColorSchemePreference,
    Dark,
    FollowSystem,
    Light,
    NoPreference,
)
from mpvqc.appearance.services import ColorSchemeService, PaletteCatalogService
from mpvqc.appearance.viewmodels import (
    AppearanceDialogInputs,
    AppearanceDialogProps,
    MpvqcAppearanceDialogViewModel,
    derive_appearance_dialog_props,
)
from mpvqc.services import ResourceService, SettingsService

SYSTEM = FollowSystem()
LIGHT = Light()
DARK = Dark()
NO_PREFERENCE = NoPreference()


@pytest.fixture
def style_hints(make_style_hints):
    return make_style_hints(DARK)


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


def _inputs(
    preference: ColorSchemePreference,
    *,
    light_accent: str | None = None,
    dark_accent: str | None = None,
) -> AppearanceDialogInputs:
    return AppearanceDialogInputs(
        appearance=Appearance(
            color_scheme_preference=preference,
            light_accent_color_preference=AccentColor(light_accent) if light_accent else NO_PREFERENCE,
            dark_accent_color_preference=AccentColor(dark_accent) if dark_accent else NO_PREFERENCE,
        )
    )


class DerivationCase(NamedTuple):
    name: str
    inputs: AppearanceDialogInputs
    expected: AppearanceDialogProps


@pytest.mark.parametrize(
    "case",
    [
        DerivationCase(
            name="system offers no accent section",
            inputs=_inputs(SYSTEM),
            expected=AppearanceDialogProps(
                color_scheme_preference_index=0,
                accent_color_index=-1,
                accent_section_visible=False,
            ),
        ),
        DerivationCase(
            name="system offers no accent section even with both accents stored",
            inputs=_inputs(SYSTEM, light_accent="#l1", dark_accent="#d3"),
            expected=AppearanceDialogProps(
                color_scheme_preference_index=0,
                accent_color_index=-1,
                accent_section_visible=False,
            ),
        ),
        DerivationCase(
            name="light with stored accent",
            inputs=_inputs(LIGHT, light_accent="#l1"),
            expected=AppearanceDialogProps(
                color_scheme_preference_index=1,
                accent_color_index=0,
                accent_section_visible=True,
            ),
        ),
        DerivationCase(
            name="light without stored accent resolves to its default",
            inputs=_inputs(LIGHT),
            expected=AppearanceDialogProps(
                color_scheme_preference_index=1,
                accent_color_index=1,
                accent_section_visible=True,
            ),
        ),
        DerivationCase(
            name="light with stale accent resolves to its default",
            inputs=_inputs(LIGHT, light_accent="#gone"),
            expected=AppearanceDialogProps(
                color_scheme_preference_index=1,
                accent_color_index=1,
                accent_section_visible=True,
            ),
        ),
        DerivationCase(
            name="light ignores the dark accent",
            inputs=_inputs(LIGHT, dark_accent="#d3"),
            expected=AppearanceDialogProps(
                color_scheme_preference_index=1,
                accent_color_index=1,
                accent_section_visible=True,
            ),
        ),
        DerivationCase(
            name="dark with stored accent",
            inputs=_inputs(DARK, dark_accent="#d2"),
            expected=AppearanceDialogProps(
                color_scheme_preference_index=2,
                accent_color_index=1,
                accent_section_visible=True,
            ),
        ),
        DerivationCase(
            name="dark without stored accent resolves to its default",
            inputs=_inputs(DARK),
            expected=AppearanceDialogProps(
                color_scheme_preference_index=2,
                accent_color_index=0,
                accent_section_visible=True,
            ),
        ),
        DerivationCase(
            name="dark ignores the light accent",
            inputs=_inputs(DARK, light_accent="#l1"),
            expected=AppearanceDialogProps(
                color_scheme_preference_index=2,
                accent_color_index=0,
                accent_section_visible=True,
            ),
        ),
    ],
    ids=lambda case: case.name,
)
def test_derivation(case: DerivationCase, catalog):
    props = derive_appearance_dialog_props(case.inputs, catalog.palette_family_for)

    assert props == case.expected


def test_initial_snapshot_reads_settings_at_construction(make_view_model, settings_service):
    settings_service.color_scheme_preference = LIGHT
    settings_service.set_accent_color_preference(LIGHT, AccentColor("#l1"))

    view_model = make_view_model()

    assert view_model.colorSchemePreferenceIndex == 1
    assert view_model.accentColorIndex == 0
    assert view_model.accentSectionVisible is True
    assert view_model.accentColorModel.rowCount() == 2


def test_a_preference_write_unfolding_the_section_emits_every_changed_notify(
    make_view_model, settings_service, make_spy
):
    settings_service.set_accent_color_preference(LIGHT, AccentColor("#l1"))
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

    settings_service.set_accent_color_preference(DARK, AccentColor("#d3"))

    assert accent_spy.count() == 1
    assert accent_spy.at(0, 0) == 2
    assert view_model.accentColorIndex == 2
    assert preference_spy.count() == 0


def test_an_accent_write_for_the_other_scheme_emits_nothing(make_view_model, settings_service, make_spy):
    settings_service.color_scheme_preference = DARK
    view_model = make_view_model()
    preference_spy = make_spy(view_model.colorSchemePreferenceIndexChanged)
    accent_spy = make_spy(view_model.accentColorIndexChanged)

    settings_service.set_accent_color_preference(LIGHT, AccentColor("#l1"))

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

    assert settings_service.accent_color_preference_for(DARK) == AccentColor("#d2")
    assert settings_service.accent_color_preference_for(LIGHT) == NO_PREFERENCE
    assert view_model.accentColorIndex == 1


def test_set_accent_color_under_system_writes_nothing(make_view_model, settings_service):
    view_model = make_view_model()

    view_model.setAccentColor("#d2")

    assert settings_service.accent_color_preference_for(DARK) == NO_PREFERENCE
    assert settings_service.accent_color_preference_for(LIGHT) == NO_PREFERENCE


def test_props_swap_completes_before_the_first_emission(make_view_model, settings_service):
    view_model = make_view_model()
    observed: list[tuple[int, int, bool]] = []
    view_model.accentSectionVisibleChanged.connect(
        lambda _: observed.append(
            (view_model.colorSchemePreferenceIndex, view_model.accentColorIndex, view_model.accentSectionVisible)
        )
    )

    settings_service.color_scheme_preference = DARK

    assert observed == [(2, 0, True)]


def test_a_desktop_flip_under_system_moves_nothing(make_view_model, style_hints, make_spy):
    inject.instance(ColorSchemeService)
    view_model = make_view_model()
    spies = [
        make_spy(view_model.colorSchemePreferenceIndexChanged),
        make_spy(view_model.accentColorIndexChanged),
        make_spy(view_model.accentSectionVisibleChanged),
    ]
    model_spy = make_spy(view_model.accentColorModel.modelReset)

    style_hints.system_reports(LIGHT)

    assert [spy.count() for spy in spies] == [0, 0, 0]
    assert model_spy.count() == 0
    assert view_model.colorSchemePreferenceIndex == 0
    assert view_model.accentSectionVisible is False
    assert view_model.accentColorModel.rowCount() == 0


def test_reject_restores_the_preference_and_both_accents(make_view_model, settings_service):
    settings_service.color_scheme_preference = DARK
    settings_service.set_accent_color_preference(LIGHT, AccentColor("#l1"))
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
    assert settings_service.accent_color_preference_for(LIGHT) == AccentColor("#l1")
    assert settings_service.accent_color_preference_for(DARK) == NO_PREFERENCE
    assert view_model.colorSchemePreferenceIndex == 2
    assert view_model.accentColorIndex == 0
    assert view_model.accentSectionVisible is True
    assert view_model.accentColorModel.rowCount() == 3
