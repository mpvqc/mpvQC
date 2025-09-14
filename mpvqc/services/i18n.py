# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from PySide6.QtCore import QLibraryInfo, QLocale, QTranslator
from PySide6.QtGui import QGuiApplication


class InternationalizationService:
    def __init__(self):
        self._translator_mpvqc = QTranslator()
        self._translator_qt = QTranslator()

    def retranslate(self, app: QGuiApplication, language_code: str) -> None:
        app.removeTranslator(self._translator_qt)
        app.removeTranslator(self._translator_mpvqc)

        locale: QLocale = create_locale_from(language_code)

        self._translator_qt.load(
            locale, "qtbase", "_", QLibraryInfo.location(QLibraryInfo.LibraryPath.TranslationsPath)
        )
        self._translator_mpvqc.load(f":/i18n/{language_code}.qm")

        app.installTranslator(self._translator_qt)
        app.installTranslator(self._translator_mpvqc)

        app.setLayoutDirection(locale.textDirection())


def create_locale_from(language_code: str) -> QLocale:
    match language_code:
        case "pt-PT":
            # As of Qt6.9 there aren't any official pt-PT translations available:
            # https://code.qt.io/cgit/qt/qttranslations.git/tree/translations
            # However, there are Brazilian Portuguese translations available
            return QLocale("pt-BR")
        case _:
            return QLocale(language_code)
