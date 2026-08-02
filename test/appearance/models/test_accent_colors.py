# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest
from PySide6.QtTest import QAbstractItemModelTester

from mpvqc.appearance.domain import ColorSchemePreference, Dark, FollowSystem, Light
from mpvqc.appearance.models import MpvqcAccentColorModel
from mpvqc.appearance.services import PaletteCatalogService
from mpvqc.services import ResourceService

SYSTEM = FollowSystem()
LIGHT = Light()
DARK = Dark()


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, make_palette_family_data, make_resource_service):
    light = make_palette_family_data(color_scheme="light", default_accent="#l1", accents=["#l1", "#l2"])
    dark = make_palette_family_data(color_scheme="dark", default_accent="#d1", accents=["#d1", "#d2", "#d3", "#d4"])
    fake = make_resource_service(light, dark)

    def custom_bindings(binder: inject.Binder):
        binder.bind(ResourceService, fake)
        binder.bind_to_constructor(PaletteCatalogService, PaletteCatalogService)

    common_bindings_with(custom_bindings)


@pytest.fixture
def catalog() -> PaletteCatalogService:
    return inject.instance(PaletteCatalogService)


@pytest.fixture
def equal_sized_catalog(common_bindings_with, make_palette_family_data, make_resource_service) -> PaletteCatalogService:
    """The shipped families hold the same number of palettes, so switching between them resizes nothing."""
    light = make_palette_family_data(color_scheme="light", default_accent="#l1", accents=["#l1", "#l2"])
    dark = make_palette_family_data(color_scheme="dark", default_accent="#d1", accents=["#d1", "#d2"])
    fake = make_resource_service(light, dark)

    def custom_bindings(binder: inject.Binder):
        binder.bind(ResourceService, fake)
        binder.bind_to_constructor(PaletteCatalogService, PaletteCatalogService)

    common_bindings_with(custom_bindings)
    return inject.instance(PaletteCatalogService)


@pytest.fixture
def make_model():
    def _make(preference: ColorSchemePreference = SYSTEM) -> MpvqcAccentColorModel:
        # noinspection PyCallingNonCallable
        model = MpvqcAccentColorModel()
        model.set_preference(preference)
        return model

    return _make


def test_under_system_the_model_is_empty(make_model):
    assert make_model().rowCount() == 0


def test_rowcount_reflects_the_preferences_palette_family(make_model):
    assert make_model(LIGHT).rowCount() == 2
    assert make_model(DARK).rowCount() == 4


def test_falling_back_to_system_empties_the_model(make_model):
    model = make_model(DARK)

    model.set_preference(SYSTEM)

    assert model.rowCount() == 0


def test_the_rows_carry_the_preferences_accents_and_preview_colors(make_model, catalog):
    model = make_model(LIGHT)

    palettes = catalog.palette_family_for(LIGHT).palettes
    accents = [model.data(model.index(row), MpvqcAccentColorModel.AccentColorRole) for row in range(model.rowCount())]
    preview_colors = [
        model.data(model.index(row), MpvqcAccentColorModel.PreviewColorRole) for row in range(model.rowCount())
    ]

    assert accents == [palette.accent_color.identifier for palette in palettes]
    assert preview_colors == [palette.row_selected for palette in palettes]


def test_switching_between_equal_sized_families_repaints_every_row(qt_app, equal_sized_catalog, make_model, make_spy):
    model = make_model(LIGHT)
    spy = make_spy(model.dataChanged)

    model.set_preference(DARK)

    palettes = equal_sized_catalog.palette_family_for(DARK).palettes
    accents = [model.data(model.index(row), MpvqcAccentColorModel.AccentColorRole) for row in range(model.rowCount())]
    preview_colors = [
        model.data(model.index(row), MpvqcAccentColorModel.PreviewColorRole) for row in range(model.rowCount())
    ]

    assert accents == [palette.accent_color.identifier for palette in palettes]
    assert preview_colors == [palette.row_selected for palette in palettes]
    assert spy.count() == 1
    assert spy.at(0, 0).row() == 0
    assert spy.at(0, 1).row() == 1


def test_setting_the_same_preference_changes_nothing(qt_app, make_model, make_spy):
    model = make_model(DARK)
    spy = make_spy(model.dataChanged)

    model.set_preference(DARK)

    assert spy.count() == 0


def test_preference_changes_satisfy_the_item_model_protocol(qt_app, make_model):
    model = make_model(LIGHT)
    QAbstractItemModelTester(model, QAbstractItemModelTester.FailureReportingMode.Fatal, model)

    model.set_preference(DARK)  # grow: 2 -> 4
    model.set_preference(LIGHT)  # shrink: 4 -> 2
    model.set_preference(SYSTEM)  # empty: 2 -> 0
    model.set_preference(DARK)  # grow: 0 -> 4
