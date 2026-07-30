# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest
from PySide6.QtGui import QFontMetricsF

from mpvqc.services import FontLoaderService, LabelWidthCalculatorService


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with):
    def custom_bindings(binder: inject.Binder):
        binder.bind_to_constructor(FontLoaderService, FontLoaderService)

    common_bindings_with(custom_bindings)


@pytest.fixture(autouse=True)
def qt_app_must_be_running(qt_app):
    pass


@pytest.fixture
def calculator() -> LabelWidthCalculatorService:
    return LabelWidthCalculatorService()


def test_empty_input_yields_zero(calculator):
    assert calculator.calculate_width_for([]) == 0


def test_empty_generator_yields_zero(calculator):
    empty: list[str] = []
    assert calculator.calculate_width_for(text for text in empty) == 0


def test_one_shot_generator_measures_like_a_list(calculator):
    expected = calculator.calculate_width_for(["i", "Wwwwwwwwww"])

    assert calculator.calculate_width_for(text for text in ["i", "Wwwwwwwwww"]) == expected


def test_width_is_the_advance_width_rounded_up(calculator):
    advance = QFontMetricsF(inject.instance(FontLoaderService).application_font()).horizontalAdvance("Translation")

    width = calculator.calculate_width_for(["Translation"])

    assert advance <= width < advance + 1


def test_widest_text_wins(calculator):
    widest = calculator.calculate_width_for(["Wwwwwwwwww"])

    assert calculator.calculate_width_for(["i", "Wwwwwwwwww"]) == widest
