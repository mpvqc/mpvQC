# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtTest import QAbstractItemModelTester

from mpvqc.models import MpvqcAccentColorModel
from mpvqc.services import PaletteCatalogService, SettingsService

PALETTE_COUNTS = {"small": 1, "medium": 2, "large": 4}


def _palette_family(palette_count: int) -> MagicMock:
    palette_family = MagicMock()
    palette_family.palette_count = palette_count
    palette_family.palettes = [MagicMock(accent_color=f"p{i}", row_selected="#000000") for i in range(palette_count)]
    return palette_family


@pytest.fixture
def catalog_mock():
    mock = MagicMock(spec_set=PaletteCatalogService)
    mock.palette_family_for_identifier.side_effect = lambda identifier: _palette_family(PALETTE_COUNTS[identifier])
    return mock


@pytest.fixture
def settings_service_mock():
    return MagicMock(spec_set=SettingsService)


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, catalog_mock, settings_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PaletteCatalogService, catalog_mock)
        binder.bind(SettingsService, settings_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def make_model(settings_service_mock):
    def _make(initial: str) -> MpvqcAccentColorModel:
        settings_service_mock.theme_identifier = initial
        # noinspection PyCallingNonCallable
        return MpvqcAccentColorModel()

    return _make


def test_rowcount_reflects_the_active_palette_family(make_model):
    assert make_model("large").rowCount() == 4


def test_palette_count_changes_satisfy_item_model_protocol(qt_app, make_model):
    model = make_model("medium")
    QAbstractItemModelTester(model, QAbstractItemModelTester.FailureReportingMode.Fatal, model)

    model._set_theme_identifier("large")  # grow: 2 -> 4
    model._set_theme_identifier("small")  # shrink: 4 -> 1
    model._set_theme_identifier("large")  # grow: 1 -> 4
