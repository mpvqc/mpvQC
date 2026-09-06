# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import inject


def bindings(binder: inject.Binder) -> None:
    import inject
    from PySide6.QtCore import QSettings

    from mpvqc.i18n.services import I18nSettingsService, InternationalizationService

    def i18n_settings_service() -> I18nSettingsService:
        return I18nSettingsService(inject.instance(QSettings))

    binder.bind_to_constructor(I18nSettingsService, i18n_settings_service)
    binder.bind_to_constructor(InternationalizationService, InternationalizationService)


def register_qml_types() -> None:
    import mpvqc.i18n.models  # ruff: ignore[unused-import]
