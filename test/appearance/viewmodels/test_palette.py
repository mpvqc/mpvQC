# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import replace
from typing import NamedTuple

import inject
import pytest

from mpvqc.appearance.domain import (
    AccentColor,
    AppearancePreference,
    ColorSchemePreference,
    Dark,
    FollowSystem,
    Light,
    NoPreference,
    Palette,
    Unknown,
)
from mpvqc.appearance.services import AppearanceSettingsService, ColorSchemeService, PaletteCatalogService
from mpvqc.appearance.viewmodels import (
    MpvqcPalette,
    MpvqcPaletteViewModel,
    PaletteInputs,
    derive_palette_props,
)
from mpvqc.services import ResourceService

SYSTEM = FollowSystem()
LIGHT = Light()
DARK = Dark()
UNKNOWN = Unknown()
NO_PREFERENCE = NoPreference()


@pytest.fixture
def style_hints(make_style_hints):
    return make_style_hints(DARK)


@pytest.fixture(autouse=True)
def configure_injections(
    common_bindings_with, appearance_settings_service, style_hints, make_palette_family_data, make_resource_service
):
    light = make_palette_family_data(color_scheme="light", default_accent_color="#l2", accents=["#l1", "#l2"])
    dark = make_palette_family_data(color_scheme="dark", default_accent_color="#d1", accents=["#d1", "#d2", "#d3"])
    fake = make_resource_service(light, dark)

    def custom_bindings(binder: inject.Binder):
        binder.bind(ResourceService, fake)
        binder.bind(AppearanceSettingsService, appearance_settings_service)
        binder.bind_to_constructor(PaletteCatalogService, PaletteCatalogService)
        binder.bind_to_constructor(ColorSchemeService, lambda: ColorSchemeService(style_hints))

    common_bindings_with(custom_bindings)


@pytest.fixture
def catalog() -> PaletteCatalogService:
    return inject.instance(PaletteCatalogService)


@pytest.fixture(autouse=True)
def qt_app_must_be_running(qt_app):
    pass


def _appearance_preference(
    *,
    preference: ColorSchemePreference = SYSTEM,
    light_accent: str | None = None,
    dark_accent: str | None = None,
) -> AppearancePreference:
    return AppearancePreference(
        color_scheme_preference=preference,
        light_accent_color_preference=AccentColor(light_accent) if light_accent else NO_PREFERENCE,
        dark_accent_color_preference=AccentColor(dark_accent) if dark_accent else NO_PREFERENCE,
    )


BASE_INPUTS = PaletteInputs(appearance_preference=_appearance_preference(), color_scheme=DARK)


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
            inputs=replace(BASE_INPUTS, appearance_preference=_appearance_preference(dark_accent="#d2")),
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
            inputs=replace(BASE_INPUTS, appearance_preference=_appearance_preference(dark_accent="#gone")),
            resolves_to=AccentColor("#d1"),
            is_dark=True,
        ),
        DerivationCase(
            name="dark scheme ignores the light accent",
            inputs=replace(BASE_INPUTS, appearance_preference=_appearance_preference(light_accent="#l1")),
            resolves_to=AccentColor("#d1"),
            is_dark=True,
        ),
        DerivationCase(
            name="light scheme with stored accent",
            inputs=replace(
                BASE_INPUTS, appearance_preference=_appearance_preference(light_accent="#l1"), color_scheme=LIGHT
            ),
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
            inputs=replace(
                BASE_INPUTS, appearance_preference=_appearance_preference(light_accent="#gone"), color_scheme=LIGHT
            ),
            resolves_to=AccentColor("#l2"),
            is_dark=False,
        ),
        DerivationCase(
            name="light scheme ignores the dark accent",
            inputs=replace(
                BASE_INPUTS, appearance_preference=_appearance_preference(dark_accent="#d2"), color_scheme=LIGHT
            ),
            resolves_to=AccentColor("#l2"),
            is_dark=False,
        ),
        DerivationCase(
            name="the preference never enters the derivation",
            inputs=replace(
                BASE_INPUTS,
                appearance_preference=_appearance_preference(preference=LIGHT, dark_accent="#d2"),
            ),
            resolves_to=AccentColor("#d2"),
            is_dark=True,
        ),
    ],
    ids=lambda case: case.name,
)
def test_derivation(case: DerivationCase, catalog):
    props = derive_palette_props(case.inputs, catalog.palette_family_for)

    assert props.palette in catalog.palette_family_for(case.inputs.color_scheme).palettes
    assert props.palette.accent_color == case.resolves_to
    assert props.is_dark is case.is_dark


@pytest.fixture
def make_view_model():
    def _make() -> MpvqcPaletteViewModel:
        # noinspection PyCallingNonCallable
        return MpvqcPaletteViewModel()

    return _make


@pytest.fixture
def spy_on(make_spy):
    def _spy(view_model) -> tuple:
        return make_spy(view_model.isDarkChanged), make_spy(view_model.palette.changed)

    return _spy


def _assert_nothing_emitted(is_dark_spy, palette_spy) -> None:
    assert is_dark_spy.count() == 0
    assert palette_spy.count() == 0


def _assert_renders(view_model, palette: Palette, *, is_dark: bool) -> None:
    assert view_model.isDark is is_dark
    assert view_model.palette.background == palette.background
    assert view_model.palette.accent == palette.accent
    assert view_model.palette.rowSelectedText == palette.row_selected_text


@pytest.mark.parametrize(
    ("desktop_reports", "expected_color_scheme"),
    [
        (LIGHT, LIGHT),
        (DARK, DARK),
        (UNKNOWN, LIGHT),
    ],
    ids=["light", "dark", "unknown-is-light"],
)
def test_initial_snapshot_renders_the_desktops_scheme(
    make_view_model, style_hints, catalog, desktop_reports, expected_color_scheme
):
    style_hints.system_reports(desktop_reports)

    view_model = make_view_model()

    palette = catalog.palette_family_for(expected_color_scheme).palette_of(_appearance_preference())
    _assert_renders(view_model, palette, is_dark=expected_color_scheme == DARK)


def test_initial_snapshot_renders_an_explicit_preference_over_the_desktop(
    make_view_model, appearance_settings_service, style_hints, catalog
):
    appearance_settings_service.color_scheme_preference = LIGHT
    style_hints.system_reports(DARK)

    view_model = make_view_model()

    _assert_renders(view_model, catalog.palette_family_for(LIGHT).palette_of(_appearance_preference()), is_dark=False)


def test_initial_snapshot_renders_the_accent_stored_for_the_apps_scheme(
    make_view_model, appearance_settings_service, catalog
):
    appearance_settings_service.set_accent_color_preference(LIGHT, AccentColor("#l1"))
    appearance_settings_service.set_accent_color_preference(DARK, AccentColor("#d2"))

    view_model = make_view_model()

    _assert_renders(
        view_model, catalog.palette_family_for(DARK).palette_of(_appearance_preference(dark_accent="#d2")), is_dark=True
    )


def test_desktop_flip_pushes_the_palette_and_emits_is_dark_once(make_view_model, style_hints, catalog, spy_on):
    view_model = make_view_model()
    is_dark_spy, palette_spy = spy_on(view_model)

    style_hints.system_reports(LIGHT)

    assert is_dark_spy.count() == 1
    assert is_dark_spy.at(0, 0) is False
    assert palette_spy.count() == 1
    _assert_renders(view_model, catalog.palette_family_for(LIGHT).palette_of(_appearance_preference()), is_dark=False)


def test_desktop_flip_swaps_to_the_other_schemes_remembered_accent(
    make_view_model, appearance_settings_service, style_hints, catalog
):
    appearance_settings_service.set_accent_color_preference(LIGHT, AccentColor("#l1"))
    appearance_settings_service.set_accent_color_preference(DARK, AccentColor("#d2"))
    view_model = make_view_model()

    style_hints.system_reports(LIGHT)

    _assert_renders(
        view_model,
        catalog.palette_family_for(LIGHT).palette_of(_appearance_preference(light_accent="#l1")),
        is_dark=False,
    )


def test_desktop_flip_under_an_explicit_preference_emits_nothing(
    make_view_model, appearance_settings_service, style_hints, spy_on
):
    appearance_settings_service.color_scheme_preference = DARK
    view_model = make_view_model()
    is_dark_spy, palette_spy = spy_on(view_model)

    style_hints.system_reports(LIGHT)

    _assert_nothing_emitted(is_dark_spy, palette_spy)


def test_preference_change_switching_the_scheme_pushes_the_palette_and_emits_is_dark_once(
    make_view_model, appearance_settings_service, catalog, spy_on
):
    view_model = make_view_model()
    is_dark_spy, palette_spy = spy_on(view_model)

    appearance_settings_service.color_scheme_preference = LIGHT

    assert is_dark_spy.count() == 1
    assert is_dark_spy.at(0, 0) is False
    assert palette_spy.count() == 1
    _assert_renders(view_model, catalog.palette_family_for(LIGHT).palette_of(_appearance_preference()), is_dark=False)


def test_preference_change_keeping_the_scheme_emits_nothing(make_view_model, appearance_settings_service, spy_on):
    view_model = make_view_model()
    is_dark_spy, palette_spy = spy_on(view_model)

    appearance_settings_service.color_scheme_preference = DARK

    _assert_nothing_emitted(is_dark_spy, palette_spy)


def test_accent_write_for_the_apps_scheme_pushes_the_palette_without_is_dark(
    make_view_model, appearance_settings_service, catalog, spy_on
):
    view_model = make_view_model()
    is_dark_spy, palette_spy = spy_on(view_model)

    appearance_settings_service.set_accent_color_preference(DARK, AccentColor("#d2"))

    assert is_dark_spy.count() == 0
    assert palette_spy.count() == 1
    _assert_renders(
        view_model,
        catalog.palette_family_for(DARK).palette_of(_appearance_preference(dark_accent="#d2")),
        is_dark=True,
    )


def test_accent_write_for_the_other_scheme_emits_nothing(make_view_model, appearance_settings_service, spy_on):
    view_model = make_view_model()
    is_dark_spy, palette_spy = spy_on(view_model)

    appearance_settings_service.set_accent_color_preference(LIGHT, AccentColor("#l1"))

    _assert_nothing_emitted(is_dark_spy, palette_spy)


def test_props_swap_completes_before_the_first_emission(make_view_model, style_hints, catalog):
    view_model = make_view_model()
    observed: list[tuple[str, bool, str]] = []

    def observe(notify: str) -> None:
        observed.append((notify, view_model.isDark, view_model.palette.background))

    view_model.palette.changed.connect(lambda: observe("palette"))
    view_model.isDarkChanged.connect(lambda _: observe("isDark"))

    style_hints.system_reports(LIGHT)

    palette = catalog.palette_family_for(LIGHT).palette_of(_appearance_preference())
    assert observed == [("palette", False, palette.background), ("isDark", False, palette.background)]


SELF_NAMING = Palette(
    accent_color=AccentColor("#accent"),
    background="background",
    foreground="foreground",
    hint="hint",
    accent="accent",
    separator="separator",
    error="error",
    error_text="error_text",
    header_background="header_background",
    popup_background="popup_background",
    popup_text="popup_text",
    menu_background="menu_background",
    dialog_background="dialog_background",
    section_card="section_card",
    tooltip_background="tooltip_background",
    tooltip_text="tooltip_text",
    row_base="row_base",
    row_base_text="row_base_text",
    row_stripe="row_stripe",
    row_stripe_text="row_stripe_text",
    row_selected="row_selected",
    row_selected_text="row_selected_text",
)


@pytest.fixture
def palette_object() -> MpvqcPalette:
    # noinspection PyCallingNonCallable
    return MpvqcPalette(SELF_NAMING)


def test_every_role_reads_its_own_field(palette_object):
    assert palette_object.background == "background"
    assert palette_object.foreground == "foreground"
    assert palette_object.hint == "hint"
    assert palette_object.accent == "accent"
    assert palette_object.separator == "separator"
    assert palette_object.error == "error"
    assert palette_object.errorText == "error_text"
    assert palette_object.headerBackground == "header_background"
    assert palette_object.popupBackground == "popup_background"
    assert palette_object.popupText == "popup_text"
    assert palette_object.menuBackground == "menu_background"
    assert palette_object.dialogBackground == "dialog_background"
    assert palette_object.sectionCard == "section_card"
    assert palette_object.tooltipBackground == "tooltip_background"
    assert palette_object.tooltipText == "tooltip_text"
    assert palette_object.rowBase == "row_base"
    assert palette_object.rowBaseText == "row_base_text"
    assert palette_object.rowStripe == "row_stripe"
    assert palette_object.rowStripeText == "row_stripe_text"
    assert palette_object.rowSelected == "row_selected"
    assert palette_object.rowSelectedText == "row_selected_text"


def test_a_push_renders_the_new_palette_and_emits_changed(palette_object, make_spy):
    spy = make_spy(palette_object.changed)

    palette_object.set_palette(replace(SELF_NAMING, background="pushed"))

    assert spy.count() == 1
    assert palette_object.background == "pushed"
