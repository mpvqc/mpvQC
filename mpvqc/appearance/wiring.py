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
    from PySide6.QtGui import QGuiApplication

    from mpvqc.appearance.services import (
        AppearanceSettingsService,
        ColorSchemeService,
        PaletteCatalogService,
        QtStyleHints,
        read_palette_catalog,
    )

    def appearance_settings_service() -> AppearanceSettingsService:
        return AppearanceSettingsService(inject.instance(QSettings))

    def color_scheme_service() -> ColorSchemeService:
        return ColorSchemeService(QtStyleHints(QGuiApplication.styleHints()))

    def palette_catalog_service() -> PaletteCatalogService:
        return PaletteCatalogService(read_palette_catalog())

    binder.bind_to_constructor(AppearanceSettingsService, appearance_settings_service)
    binder.bind_to_constructor(ColorSchemeService, color_scheme_service)
    binder.bind_to_constructor(PaletteCatalogService, palette_catalog_service)


def register_qml_types() -> None:
    import mpvqc.appearance.models  # ruff: ignore[unused-import]
    import mpvqc.appearance.viewmodels  # ruff: ignore[unused-import]
