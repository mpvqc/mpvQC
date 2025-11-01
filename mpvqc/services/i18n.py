# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from PySide6.QtCore import QFile, QLibraryInfo, QLocale, QTranslator
from PySide6.QtGui import QGuiApplication

logger = logging.getLogger(__name__)


class InternationalizationService:
    def __init__(self):
        self._translator_mpvqc = QTranslator()
        self._translator_qt = QTranslator()
        self._translator_qt_overrides = QTranslator()

    def retranslate(self, app: QGuiApplication, language_code: str) -> None:
        app.removeTranslator(self._translator_mpvqc)
        app.removeTranslator(self._translator_qt_overrides)
        app.removeTranslator(self._translator_qt)

        locale: QLocale = create_locale_from(language_code)
        logger.debug("Loading mpvQC translation %s for locale %s", language_code, locale.name())

        qt_translations_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)

        if not self._translator_qt.load(locale, "qtbase", "_", qt_translations_path):
            logger.warning("Qt base translations not found for %s", locale.name())
        else:
            app.installTranslator(self._translator_qt)

        qt_overrides_path = f":/i18n/{language_code}-qt-overrides.qm"
        if QFile.exists(qt_overrides_path) and self._translator_qt_overrides.load(qt_overrides_path):
            app.installTranslator(self._translator_qt_overrides)
            logger.debug("Loaded Qt overrides for mpvQC translation %s", language_code)

        mpvqc_path = f":/i18n/{language_code}.qm"
        if not self._translator_mpvqc.load(mpvqc_path):
            logger.error("Failed to load app translations: %s", mpvqc_path)
        else:
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
