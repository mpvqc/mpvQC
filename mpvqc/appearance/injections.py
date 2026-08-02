# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtGui import QGuiApplication

from mpvqc.appearance.services.color_scheme import ColorSchemeService, QtStyleHints
from mpvqc.appearance.services.palette_catalog import PaletteCatalogService


def _color_scheme_service() -> ColorSchemeService:
    return ColorSchemeService(QtStyleHints(QGuiApplication.styleHints()))


def bindings(binder: inject.Binder) -> None:
    binder.bind_to_constructor(ColorSchemeService, _color_scheme_service)
    binder.bind_to_constructor(PaletteCatalogService, PaletteCatalogService)
