# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest

from mpvqc.models.languages import MpvqcLanguageModel, MpvqcLanguageModelBackend
from mpvqc.services import InternationalizationService


@pytest.fixture
def service() -> InternationalizationService:
    return InternationalizationService()


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(InternationalizationService, service)

    common_bindings_with(custom_bindings)


def _identifiers(model: MpvqcLanguageModel) -> list[str]:
    return [
        model.data(model.index(row, 0), MpvqcLanguageModelBackend.IdentifierRole) for row in range(model.rowCount())
    ]


def test_resorts_when_the_ui_language_changes(qt_app, service) -> None:
    service.retranslate(qt_app, "en-US")
    model = MpvqcLanguageModel()
    english_order = _identifiers(model)

    service.retranslate(qt_app, "de-DE")
    german_order = _identifiers(model)

    assert english_order.index("en-US") < english_order.index("de-DE")
    assert german_order.index("de-DE") < german_order.index("en-US")
