# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import asdict
from typing import NamedTuple

import inject
import pytest

from mpvqc.appearance import AccentColor, Appearance, Palette, ThemeIdentifier
from mpvqc.services import ResourceService, SettingsService, ThemeService
from mpvqc.viewmodels.utility.palette import MpvqcPaletteViewModel, PaletteProps, derive_palette_props

LIGHT = ThemeIdentifier("material-you")
DARK = ThemeIdentifier("material-you-dark")


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, settings_service, make_theme_data, make_resource_service):
    light = make_theme_data(identifier=str(LIGHT), is_dark=False, default_accent="#l2", accents=["#l1", "#l2"])
    dark = make_theme_data(identifier=str(DARK), is_dark=True, default_accent="#d1", accents=["#d1", "#d2", "#d3"])
    fake = make_resource_service(light, dark)

    def custom_bindings(binder: inject.Binder):
        binder.bind(ResourceService, fake)
        binder.bind(SettingsService, settings_service)
        binder.bind_to_constructor(ThemeService, ThemeService)

    common_bindings_with(custom_bindings)


@pytest.fixture
def theme_service() -> ThemeService:
    return inject.instance(ThemeService)


@pytest.fixture(autouse=True)
def qt_app_must_be_running(qt_app):
    pass


def _props_from(palette: Palette, *, is_dark: bool) -> PaletteProps:
    roles = asdict(palette)
    del roles["accent_color"]
    return PaletteProps(is_dark=is_dark, **roles)


class DerivationCase(NamedTuple):
    name: str
    appearance: Appearance
    resolves_to: AccentColor
    is_dark: bool


@pytest.mark.parametrize(
    "case",
    [
        DerivationCase(
            name="dark theme with stored accent",
            appearance=Appearance(theme_identifier=DARK, stored_accent=AccentColor("#d2")),
            resolves_to=AccentColor("#d2"),
            is_dark=True,
        ),
        DerivationCase(
            name="dark theme without stored accent resolves to its default",
            appearance=Appearance(theme_identifier=DARK, stored_accent=None),
            resolves_to=AccentColor("#d1"),
            is_dark=True,
        ),
        DerivationCase(
            name="dark theme with stale accent resolves to its default",
            appearance=Appearance(theme_identifier=DARK, stored_accent=AccentColor("#gone")),
            resolves_to=AccentColor("#d1"),
            is_dark=True,
        ),
        DerivationCase(
            name="light theme with stored accent",
            appearance=Appearance(theme_identifier=LIGHT, stored_accent=AccentColor("#l1")),
            resolves_to=AccentColor("#l1"),
            is_dark=False,
        ),
        DerivationCase(
            name="light theme without stored accent resolves to its default",
            appearance=Appearance(theme_identifier=LIGHT, stored_accent=None),
            resolves_to=AccentColor("#l2"),
            is_dark=False,
        ),
        DerivationCase(
            name="light theme with stale accent resolves to its default",
            appearance=Appearance(theme_identifier=LIGHT, stored_accent=AccentColor("#gone")),
            resolves_to=AccentColor("#l2"),
            is_dark=False,
        ),
    ],
    ids=lambda case: case.name,
)
def test_derivation(case: DerivationCase, theme_service):
    props = derive_palette_props(case.appearance, theme_service.theme)

    palette = theme_service.theme(case.appearance.theme_identifier).palette_for(case.resolves_to)
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


def test_initial_snapshot_reads_settings_at_construction(make_view_model, settings_service, theme_service):
    settings_service.theme_identifier = str(LIGHT)
    settings_service.set_accent_color(LIGHT, AccentColor("#l1"))

    view_model = make_view_model()

    palette = theme_service.theme(LIGHT).palette_for(AccentColor("#l1"))
    assert view_model.isDark is False
    assert view_model.background == palette.background
    assert view_model.accent == palette.accent
    assert view_model.rowSelectedText == palette.row_selected_text


def test_theme_switch_emits_is_dark_once_and_only_the_changed_roles(
    make_view_model, settings_service, theme_service, make_spy, spy_roles
):
    view_model = make_view_model()
    is_dark_spy = make_spy(view_model.isDarkChanged)
    spies = spy_roles(view_model)

    settings_service.theme_identifier = str(LIGHT)

    changed = _changed_roles(theme_service.theme(DARK).palette_for(None), theme_service.theme(LIGHT).palette_for(None))
    assert changed, "the fake themes must differ in at least one color role"
    assert is_dark_spy.count() == 1
    assert is_dark_spy.at(0, 0) is False
    for name, spy in spies.items():
        if name in changed:
            assert spy.count() == 1, name
            assert spy.at(0, 0) == changed[name], name
        else:
            assert spy.count() == 0, name


def test_current_theme_accent_write_emits_a_color_subset_and_no_is_dark(
    make_view_model, settings_service, theme_service, make_spy, spy_roles
):
    view_model = make_view_model()
    is_dark_spy = make_spy(view_model.isDarkChanged)
    spies = spy_roles(view_model)

    settings_service.set_accent_color(DARK, AccentColor("#d2"))

    theme = theme_service.theme(DARK)
    changed = _changed_roles(theme.palette_for(None), theme.palette_for(AccentColor("#d2")))
    assert changed, "the fake accents must differ in at least one color role"
    assert is_dark_spy.count() == 0
    for name, spy in spies.items():
        if name in changed:
            assert spy.count() == 1, name
            assert spy.at(0, 0) == changed[name], name
        else:
            assert spy.count() == 0, name


def test_accent_write_for_another_theme_emits_nothing(make_view_model, settings_service, make_spy, spy_roles):
    view_model = make_view_model()
    is_dark_spy = make_spy(view_model.isDarkChanged)
    spies = spy_roles(view_model)

    settings_service.set_accent_color(LIGHT, AccentColor("#l1"))

    assert is_dark_spy.count() == 0
    for name, spy in spies.items():
        assert spy.count() == 0, name


def test_props_swap_completes_before_the_first_emission(make_view_model, settings_service, theme_service):
    view_model = make_view_model()
    observed: list[tuple[bool, str]] = []
    view_model.isDarkChanged.connect(lambda _: observed.append((view_model.isDark, view_model.background)))

    settings_service.theme_identifier = str(LIGHT)

    palette = theme_service.theme(LIGHT).palette_for(None)
    assert observed == [(False, palette.background)]
