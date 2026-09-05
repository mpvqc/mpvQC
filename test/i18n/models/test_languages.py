# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest

from mpvqc.i18n.models import LanguageModelBackend, MpvqcLanguageModel
from mpvqc.i18n.services import InternationalizationService


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, internationalization_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(InternationalizationService, internationalization_service)

    common_bindings_with(custom_bindings)


def _identifiers(model: MpvqcLanguageModel) -> list[str]:
    return [model.data(model.index(row, 0), LanguageModelBackend.IdentifierRole) for row in range(model.rowCount())]


def test_resorts_when_the_ui_language_changes(qt_app, internationalization_service) -> None:
    internationalization_service.retranslate(qt_app, "en-US")
    model = MpvqcLanguageModel()
    english_order = _identifiers(model)

    internationalization_service.retranslate(qt_app, "de-DE")
    german_order = _identifiers(model)

    assert english_order.index("en-US") < english_order.index("de-DE")
    assert german_order.index("de-DE") < german_order.index("en-US")
