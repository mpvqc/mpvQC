# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest
from PySide6.QtTest import QAbstractItemModelTester

from mpvqc.appearance import ColorScheme, Dark, Light
from mpvqc.models import MpvqcAccentColorModel
from mpvqc.services import PaletteCatalogService, ResourceService

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
def make_model():
    def _make(color_scheme: ColorScheme | None = None) -> MpvqcAccentColorModel:
        # noinspection PyCallingNonCallable
        model = MpvqcAccentColorModel()
        model.set_color_scheme(color_scheme)
        return model

    return _make


def test_without_a_color_scheme_the_model_is_empty(make_model):
    assert make_model().rowCount() == 0


def test_rowcount_reflects_the_schemes_palette_family(make_model):
    assert make_model(LIGHT).rowCount() == 2
    assert make_model(DARK).rowCount() == 4


def test_clearing_the_color_scheme_empties_the_model(make_model):
    model = make_model(DARK)

    model.set_color_scheme(None)

    assert model.rowCount() == 0


def test_the_rows_carry_the_schemes_accents_and_display_colors(make_model, catalog):
    model = make_model(LIGHT)

    palettes = catalog.palette_family_for(LIGHT).palettes
    accents = [model.data(model.index(row), MpvqcAccentColorModel.AccentColorRole) for row in range(model.rowCount())]
    displays = [model.data(model.index(row), MpvqcAccentColorModel.DisplayColorRole) for row in range(model.rowCount())]

    assert accents == [palette.accent_color.identifier for palette in palettes]
    assert displays == [palette.row_selected for palette in palettes]


def test_setting_the_same_color_scheme_changes_nothing(qt_app, make_model, make_spy):
    model = make_model(DARK)
    spy = make_spy(model.dataChanged)

    model.set_color_scheme(DARK)

    assert spy.count() == 0


def test_color_scheme_changes_satisfy_the_item_model_protocol(qt_app, make_model):
    model = make_model(LIGHT)
    QAbstractItemModelTester(model, QAbstractItemModelTester.FailureReportingMode.Fatal, model)

    model.set_color_scheme(DARK)  # grow: 2 -> 4
    model.set_color_scheme(LIGHT)  # shrink: 4 -> 2
    model.set_color_scheme(None)  # empty: 2 -> 0
    model.set_color_scheme(DARK)  # grow: 0 -> 4
