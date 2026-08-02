# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtGui import QGuiApplication

from mpvqc.appearance.services import ColorSchemeService, PaletteCatalogService, QtStyleHints


def _color_scheme_service() -> ColorSchemeService:
    return ColorSchemeService(QtStyleHints(QGuiApplication.styleHints()))


def bindings(binder: inject.Binder) -> None:
    binder.bind_to_constructor(ColorSchemeService, _color_scheme_service)
    binder.bind_to_constructor(PaletteCatalogService, PaletteCatalogService)
