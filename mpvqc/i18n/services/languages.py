# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass

from PySide6.QtCore import QT_TRANSLATE_NOOP, QLocale


@dataclass(frozen=True)
class Language:
    language: str
    identifier: str
    translators: tuple[str, ...] = ()


LANGUAGES = (
    Language(
        language=str(QT_TRANSLATE_NOOP("Languages", "German")),
        identifier="de-DE",
    ),
    Language(
        language=str(QT_TRANSLATE_NOOP("Languages", "English")),
        identifier="en-US",
    ),
    Language(
        language=str(QT_TRANSLATE_NOOP("Languages", "Spanish")),
        identifier="es-MX",
        translators=("CiferrC",),
    ),
    Language(
        language=str(QT_TRANSLATE_NOOP("Languages", "Hebrew")),
        identifier="he-IL",
        translators=("cN3rd",),
    ),
    Language(
        language=str(QT_TRANSLATE_NOOP("Languages", "Italian")),
        identifier="it-IT",
        translators=("maddo",),
    ),
    Language(
        language=str(QT_TRANSLATE_NOOP("Languages", "Portuguese")),
        identifier="pt-PT",
        translators=("Diogo_23",),
    ),
)


def default_language(locale: QLocale | None = None) -> str:
    if locale is None:
        locale = QLocale.system()

    system_languages = locale.uiLanguages()

    for language in LANGUAGES:
        if language.identifier in system_languages:
            return language.identifier

    return "en-US"
