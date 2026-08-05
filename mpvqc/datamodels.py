# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass

from PySide6.QtCore import QT_TRANSLATE_NOOP


@dataclass(frozen=True, slots=True)
class Comment:
    time: int  # milliseconds
    comment_type: str
    comment: str


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
