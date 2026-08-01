# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import inject
import pytest

from mpvqc.appearance import AccentColor, Appearance, ThemeIdentifier
from mpvqc.dialogs.appearance import (
    AppearanceDialogProps,
    MpvqcAppearanceDialogViewModel,
    derive_appearance_dialog_props,
)
from mpvqc.services import ResourceService, SettingsService, ThemeService

LIGHT = ThemeIdentifier("material-you")
DARK = ThemeIdentifier("material-you-dark")


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, settings_service, make_theme_data, make_resource_service):
    light = make_theme_data(identifier=str(LIGHT), default_accent="#l2", accents=["#l1", "#l2"])
    dark = make_theme_data(identifier=str(DARK), default_accent="#d1", accents=["#d1", "#d2", "#d3"])
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


@pytest.fixture
def make_view_model():
    def _make() -> MpvqcAppearanceDialogViewModel:
        # noinspection PyCallingNonCallable
        return MpvqcAppearanceDialogViewModel()

    return _make


class DerivationCase(NamedTuple):
    name: str
    appearance: Appearance
    expected: AppearanceDialogProps


@pytest.mark.parametrize(
    "case",
    [
        DerivationCase(
            name="dark theme with stored accent",
            appearance=Appearance(theme_identifier=DARK, stored_accent=AccentColor("#d2")),
            expected=AppearanceDialogProps(theme_index=1, accent_color_index=1),
        ),
        DerivationCase(
            name="dark theme without stored accent resolves to its default",
            appearance=Appearance(theme_identifier=DARK, stored_accent=None),
            expected=AppearanceDialogProps(theme_index=1, accent_color_index=0),
        ),
        DerivationCase(
            name="dark theme with stale accent resolves to its default",
            appearance=Appearance(theme_identifier=DARK, stored_accent=AccentColor("#gone")),
            expected=AppearanceDialogProps(theme_index=1, accent_color_index=0),
        ),
        DerivationCase(
            name="light theme with stored accent",
            appearance=Appearance(theme_identifier=LIGHT, stored_accent=AccentColor("#l1")),
            expected=AppearanceDialogProps(theme_index=0, accent_color_index=0),
        ),
        DerivationCase(
            name="light theme without stored accent resolves to its default",
            appearance=Appearance(theme_identifier=LIGHT, stored_accent=None),
            expected=AppearanceDialogProps(theme_index=0, accent_color_index=1),
        ),
        DerivationCase(
            name="light theme with stale accent resolves to its default",
            appearance=Appearance(theme_identifier=LIGHT, stored_accent=AccentColor("#gone")),
            expected=AppearanceDialogProps(theme_index=0, accent_color_index=1),
        ),
    ],
    ids=lambda case: case.name,
)
def test_derivation(case: DerivationCase, theme_service):
    def accent_color_index_for(theme_identifier: ThemeIdentifier, accent: AccentColor | None) -> int:
        return theme_service.theme(theme_identifier).palette_index(accent)

    props = derive_appearance_dialog_props(case.appearance, theme_service.theme_index, accent_color_index_for)

    assert props == case.expected


def test_initial_snapshot_reads_settings_at_construction(make_view_model, settings_service):
    settings_service.theme_identifier = str(LIGHT)
    settings_service.set_accent_color(LIGHT, AccentColor("#l1"))

    view_model = make_view_model()

    assert view_model.themeIndex == 0
    assert view_model.accentColorIndex == 0


def test_theme_write_moving_both_indices_emits_both_notifies_once(make_view_model, settings_service, make_spy):
    settings_service.set_accent_color(DARK, AccentColor("#d2"))
    settings_service.set_accent_color(LIGHT, AccentColor("#l1"))
    view_model = make_view_model()
    theme_spy = make_spy(view_model.themeIndexChanged)
    accent_spy = make_spy(view_model.accentColorIndexChanged)

    settings_service.theme_identifier = str(LIGHT)

    assert theme_spy.count() == 1
    assert theme_spy.at(0, 0) == 0
    assert accent_spy.count() == 1
    assert accent_spy.at(0, 0) == 0


def test_theme_write_keeping_the_accent_index_emits_only_the_theme_notify(make_view_model, settings_service, make_spy):
    settings_service.set_accent_color(LIGHT, AccentColor("#l1"))
    view_model = make_view_model()
    assert view_model.accentColorIndex == 0
    theme_spy = make_spy(view_model.themeIndexChanged)
    accent_spy = make_spy(view_model.accentColorIndexChanged)

    settings_service.theme_identifier = str(LIGHT)

    assert theme_spy.count() == 1
    assert theme_spy.at(0, 0) == 0
    assert accent_spy.count() == 0


def test_external_accent_write_for_the_current_theme_moves_the_accent_index(
    make_view_model, settings_service, make_spy
):
    view_model = make_view_model()
    theme_spy = make_spy(view_model.themeIndexChanged)
    accent_spy = make_spy(view_model.accentColorIndexChanged)

    settings_service.set_accent_color(DARK, AccentColor("#d3"))

    assert accent_spy.count() == 1
    assert accent_spy.at(0, 0) == 2
    assert view_model.accentColorIndex == 2
    assert theme_spy.count() == 0


def test_accent_write_for_another_theme_emits_nothing(make_view_model, settings_service, make_spy):
    view_model = make_view_model()
    theme_spy = make_spy(view_model.themeIndexChanged)
    accent_spy = make_spy(view_model.accentColorIndexChanged)

    settings_service.set_accent_color(LIGHT, AccentColor("#l1"))

    assert theme_spy.count() == 0
    assert accent_spy.count() == 0


def test_set_theme_writes_the_identifier_and_moves_the_indices(make_view_model, settings_service):
    view_model = make_view_model()

    view_model.setTheme(str(LIGHT))

    assert settings_service.theme_identifier == str(LIGHT)
    assert view_model.themeIndex == 0
    assert view_model.accentColorIndex == 1


def test_set_accent_color_writes_the_current_theme_entry_and_the_legacy_global(make_view_model, settings_service):
    view_model = make_view_model()

    view_model.setAccentColor("#d2")

    assert settings_service.accent_color_for(DARK) == "#d2"
    assert settings_service.accent_color_for(LIGHT) is None
    assert settings_service.primary_color == "#d2"
    assert view_model.accentColorIndex == 1


def test_reject_restores_every_entry_and_both_indices(make_view_model, settings_service):
    settings_service.set_accent_color(LIGHT, AccentColor("#l1"))
    legacy_accent = settings_service.primary_color
    view_model = make_view_model()
    assert view_model.themeIndex == 1
    assert view_model.accentColorIndex == 0

    view_model.setTheme(str(LIGHT))
    view_model.setAccentColor("#l2")
    view_model.setTheme(str(DARK))
    view_model.setAccentColor("#d3")

    view_model.reject()

    assert settings_service.theme_identifier == str(DARK)
    assert settings_service.accent_color_for(DARK) is None
    assert settings_service.accent_color_for(LIGHT) == "#l1"
    assert settings_service.primary_color == legacy_accent
    assert view_model.themeIndex == 1
    assert view_model.accentColorIndex == 0
