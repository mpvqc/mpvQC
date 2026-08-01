# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import asdict, replace
from typing import NamedTuple

import inject
import pytest
from PySide6.QtCore import Qt

from mpvqc.appearance import AccentColor, Appearance, ColorSchemePreference, EffectiveColorScheme, Palette
from mpvqc.services import ColorSchemeService, PaletteCatalogService, ResourceService, SettingsService
from mpvqc.viewmodels.utility.palette import (
    MpvqcPaletteViewModel,
    PaletteInputs,
    PaletteProps,
    derive_palette_props,
)

LIGHT = EffectiveColorScheme.LIGHT
DARK = EffectiveColorScheme.DARK


@pytest.fixture
def style_hints(make_style_hints):
    return make_style_hints(Qt.ColorScheme.Dark)


@pytest.fixture(autouse=True)
def configure_injections(
    common_bindings_with, settings_service, style_hints, make_palette_family_data, make_resource_service
):
    light = make_palette_family_data(
        identifier="fake-light", color_scheme="light", default_accent="#l2", accents=["#l1", "#l2"]
    )
    dark = make_palette_family_data(
        identifier="fake-dark", color_scheme="dark", default_accent="#d1", accents=["#d1", "#d2", "#d3"]
    )
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


def _appearance(
    *,
    preference: ColorSchemePreference = ColorSchemePreference.SYSTEM,
    light_accent: str | None = None,
    dark_accent: str | None = None,
) -> Appearance:
    return Appearance(
        color_scheme_preference=preference,
        light_accent_color=AccentColor(light_accent) if light_accent else None,
        dark_accent_color=AccentColor(dark_accent) if dark_accent else None,
    )


def _props_from(palette: Palette, *, is_dark: bool) -> PaletteProps:
    roles = asdict(palette)
    del roles["accent_color"]
    return PaletteProps(is_dark=is_dark, **roles)


BASE_INPUTS = PaletteInputs(appearance=_appearance(), color_scheme=DARK)


class DerivationCase(NamedTuple):
    name: str
    inputs: PaletteInputs
    resolves_to: AccentColor
    is_dark: bool


@pytest.mark.parametrize(
    "case",
    [
        DerivationCase(
            name="dark scheme with stored accent",
            inputs=replace(BASE_INPUTS, appearance=_appearance(dark_accent="#d2")),
            resolves_to=AccentColor("#d2"),
            is_dark=True,
        ),
        DerivationCase(
            name="dark scheme without stored accent resolves to its default",
            inputs=BASE_INPUTS,
            resolves_to=AccentColor("#d1"),
            is_dark=True,
        ),
        DerivationCase(
            name="dark scheme with stale accent resolves to its default",
            inputs=replace(BASE_INPUTS, appearance=_appearance(dark_accent="#gone")),
            resolves_to=AccentColor("#d1"),
            is_dark=True,
        ),
        DerivationCase(
            name="dark scheme ignores the light accent",
            inputs=replace(BASE_INPUTS, appearance=_appearance(light_accent="#l1")),
            resolves_to=AccentColor("#d1"),
            is_dark=True,
        ),
        DerivationCase(
            name="light scheme with stored accent",
            inputs=replace(BASE_INPUTS, appearance=_appearance(light_accent="#l1"), color_scheme=LIGHT),
            resolves_to=AccentColor("#l1"),
            is_dark=False,
        ),
        DerivationCase(
            name="light scheme without stored accent resolves to its default",
            inputs=replace(BASE_INPUTS, color_scheme=LIGHT),
            resolves_to=AccentColor("#l2"),
            is_dark=False,
        ),
        DerivationCase(
            name="light scheme with stale accent resolves to its default",
            inputs=replace(BASE_INPUTS, appearance=_appearance(light_accent="#gone"), color_scheme=LIGHT),
            resolves_to=AccentColor("#l2"),
            is_dark=False,
        ),
        DerivationCase(
            name="light scheme ignores the dark accent",
            inputs=replace(BASE_INPUTS, appearance=_appearance(dark_accent="#d2"), color_scheme=LIGHT),
            resolves_to=AccentColor("#l2"),
            is_dark=False,
        ),
        DerivationCase(
            name="the preference never enters the derivation",
            inputs=replace(
                BASE_INPUTS,
                appearance=_appearance(preference=ColorSchemePreference.LIGHT, dark_accent="#d2"),
            ),
            resolves_to=AccentColor("#d2"),
            is_dark=True,
        ),
    ],
    ids=lambda case: case.name,
)
def test_derivation(case: DerivationCase, catalog):
    props = derive_palette_props(case.inputs, catalog.palette_family_for)

    palette = catalog.palette_family_for(case.inputs.color_scheme).palette_for(case.resolves_to)
    assert props == _props_from(palette, is_dark=case.is_dark)


@pytest.fixture
def make_view_model():
    def _make() -> MpvqcPaletteViewModel:
        # noinspection PyCallingNonCallable
        return MpvqcPaletteViewModel()

    return _make


@pytest.fixture
def spy_roles(make_spy):
    def _spy(view_model: MpvqcPaletteViewModel) -> dict:
        return {
            "background": make_spy(view_model.backgroundChanged),
            "foreground": make_spy(view_model.foregroundChanged),
            "hint": make_spy(view_model.hintChanged),
            "accent": make_spy(view_model.accentChanged),
            "separator": make_spy(view_model.separatorChanged),
            "error": make_spy(view_model.errorChanged),
            "error_text": make_spy(view_model.errorTextChanged),
            "header_background": make_spy(view_model.headerBackgroundChanged),
            "popup_background": make_spy(view_model.popupBackgroundChanged),
            "popup_text": make_spy(view_model.popupTextChanged),
            "menu_background": make_spy(view_model.menuBackgroundChanged),
            "dialog_background": make_spy(view_model.dialogBackgroundChanged),
            "tooltip_background": make_spy(view_model.tooltipBackgroundChanged),
            "tooltip_text": make_spy(view_model.tooltipTextChanged),
            "row_base": make_spy(view_model.rowBaseChanged),
            "row_base_text": make_spy(view_model.rowBaseTextChanged),
            "row_stripe": make_spy(view_model.rowStripeChanged),
            "row_stripe_text": make_spy(view_model.rowStripeTextChanged),
            "row_selected": make_spy(view_model.rowSelectedChanged),
            "row_selected_text": make_spy(view_model.rowSelectedTextChanged),
        }

    return _spy


def _changed_roles(before: Palette, after: Palette) -> dict[str, str]:
    before_roles, after_roles = asdict(before), asdict(after)
    return {
        name: after_roles[name]
        for name in before_roles
        if name != "accent_color" and before_roles[name] != after_roles[name]
    }


def _assert_only_changed_roles_emitted(spies: dict, changed: dict[str, str]) -> None:
    assert changed, "the fake palettes must differ in at least one color role"
    for name, spy in spies.items():
        if name in changed:
            assert spy.count() == 1, name
            assert spy.at(0, 0) == changed[name], name
        else:
            assert spy.count() == 0, name


def _assert_nothing_emitted(is_dark_spy, spies: dict) -> None:
    assert is_dark_spy.count() == 0
    for name, spy in spies.items():
        assert spy.count() == 0, name


def _assert_renders(view_model: MpvqcPaletteViewModel, palette: Palette, *, is_dark: bool) -> None:
    assert view_model.isDark is is_dark
    assert view_model.background == palette.background
    assert view_model.accent == palette.accent
    assert view_model.rowSelectedText == palette.row_selected_text


@pytest.mark.parametrize(
    ("desktop_reports", "expected_color_scheme"),
    [
        (Qt.ColorScheme.Light, LIGHT),
        (Qt.ColorScheme.Dark, DARK),
        (Qt.ColorScheme.Unknown, DARK),
    ],
)
def test_initial_snapshot_renders_the_desktops_scheme(
    make_view_model, style_hints, catalog, desktop_reports, expected_color_scheme
):
    style_hints.system_reports(desktop_reports)

    view_model = make_view_model()

    palette = catalog.palette_family_for(expected_color_scheme).palette_for(None)
    _assert_renders(view_model, palette, is_dark=expected_color_scheme is DARK)


def test_initial_snapshot_renders_an_explicit_preference_over_the_desktop(
    make_view_model, settings_service, style_hints, catalog
):
    settings_service.color_scheme_preference = ColorSchemePreference.LIGHT
    style_hints.system_reports(Qt.ColorScheme.Dark)

    view_model = make_view_model()

    _assert_renders(view_model, catalog.palette_family_for(LIGHT).palette_for(None), is_dark=False)


def test_initial_snapshot_renders_the_accent_stored_for_the_effective_scheme(
    make_view_model, settings_service, catalog
):
    settings_service.set_accent_color(LIGHT, AccentColor("#l1"))
    settings_service.set_accent_color(DARK, AccentColor("#d2"))

    view_model = make_view_model()

    _assert_renders(view_model, catalog.palette_family_for(DARK).palette_for(AccentColor("#d2")), is_dark=True)


def test_desktop_flip_emits_is_dark_once_and_only_the_changed_roles(
    make_view_model, style_hints, catalog, make_spy, spy_roles
):
    view_model = make_view_model()
    is_dark_spy = make_spy(view_model.isDarkChanged)
    spies = spy_roles(view_model)

    style_hints.system_reports(Qt.ColorScheme.Light)

    assert is_dark_spy.count() == 1
    assert is_dark_spy.at(0, 0) is False
    _assert_only_changed_roles_emitted(
        spies,
        _changed_roles(
            catalog.palette_family_for(DARK).palette_for(None),
            catalog.palette_family_for(LIGHT).palette_for(None),
        ),
    )


def test_desktop_flip_swaps_to_the_other_schemes_remembered_accent(
    make_view_model, settings_service, style_hints, catalog
):
    settings_service.set_accent_color(LIGHT, AccentColor("#l1"))
    settings_service.set_accent_color(DARK, AccentColor("#d2"))
    view_model = make_view_model()

    style_hints.system_reports(Qt.ColorScheme.Light)

    _assert_renders(view_model, catalog.palette_family_for(LIGHT).palette_for(AccentColor("#l1")), is_dark=False)


def test_desktop_flip_under_an_explicit_preference_emits_nothing(
    make_view_model, settings_service, style_hints, make_spy, spy_roles
):
    settings_service.color_scheme_preference = ColorSchemePreference.DARK
    view_model = make_view_model()
    is_dark_spy = make_spy(view_model.isDarkChanged)
    spies = spy_roles(view_model)

    style_hints.system_reports(Qt.ColorScheme.Light)

    _assert_nothing_emitted(is_dark_spy, spies)


def test_preference_change_switching_the_scheme_emits_is_dark_once_and_only_the_changed_roles(
    make_view_model, settings_service, catalog, make_spy, spy_roles
):
    view_model = make_view_model()
    is_dark_spy = make_spy(view_model.isDarkChanged)
    spies = spy_roles(view_model)

    settings_service.color_scheme_preference = ColorSchemePreference.LIGHT

    assert is_dark_spy.count() == 1
    assert is_dark_spy.at(0, 0) is False
    _assert_only_changed_roles_emitted(
        spies,
        _changed_roles(
            catalog.palette_family_for(DARK).palette_for(None),
            catalog.palette_family_for(LIGHT).palette_for(None),
        ),
    )


def test_preference_change_keeping_the_scheme_emits_nothing(make_view_model, settings_service, make_spy, spy_roles):
    view_model = make_view_model()
    is_dark_spy = make_spy(view_model.isDarkChanged)
    spies = spy_roles(view_model)

    settings_service.color_scheme_preference = ColorSchemePreference.DARK

    _assert_nothing_emitted(is_dark_spy, spies)


def test_accent_write_for_the_effective_scheme_emits_a_color_subset_and_no_is_dark(
    make_view_model, settings_service, catalog, make_spy, spy_roles
):
    view_model = make_view_model()
    is_dark_spy = make_spy(view_model.isDarkChanged)
    spies = spy_roles(view_model)

    settings_service.set_accent_color(DARK, AccentColor("#d2"))

    palette_family = catalog.palette_family_for(DARK)
    assert is_dark_spy.count() == 0
    _assert_only_changed_roles_emitted(
        spies, _changed_roles(palette_family.palette_for(None), palette_family.palette_for(AccentColor("#d2")))
    )


def test_accent_write_for_the_other_scheme_emits_nothing(make_view_model, settings_service, make_spy, spy_roles):
    view_model = make_view_model()
    is_dark_spy = make_spy(view_model.isDarkChanged)
    spies = spy_roles(view_model)

    settings_service.set_accent_color(LIGHT, AccentColor("#l1"))

    _assert_nothing_emitted(is_dark_spy, spies)


def test_props_swap_completes_before_the_first_emission(make_view_model, style_hints, catalog):
    view_model = make_view_model()
    observed: list[tuple[bool, str]] = []
    view_model.isDarkChanged.connect(lambda _: observed.append((view_model.isDark, view_model.background)))

    style_hints.system_reports(Qt.ColorScheme.Light)

    palette = catalog.palette_family_for(LIGHT).palette_for(None)
    assert observed == [(False, palette.background)]
