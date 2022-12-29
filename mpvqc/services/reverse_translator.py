#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import Callable

from PySide6.QtCore import QCoreApplication

DEFAULT_COMMENT_TYPES_ENGLISH = [
    'Translation',
    'Spelling',
    'Punctuation',
    'Phrasing',
    'Timing',
    'Typeset',
    'Note',
]

# Must be kept in sync with available languages in qml/models/MpvqcLanguageModel.qml
SUPPORTED_LANGUAGES = [
    'en-US',
    'de-DE',
    'he-IL',
    'it-IT',
    'es-ES',
]


class ReverseTranslatorService:

    def __init__(self):
        self._combined_lookup_table: dict[str, str] = {}
        self._language_lookup_table: dict[str, dict[str, str]] = {}

    def lookup(self, non_english: str) -> str:
        return self._combined_lookup_table.get(non_english, non_english)

    def lookup_specific_language(self, language: str, non_english: str) -> str:
        language_lookup = self._language_lookup_table.get(language, {})
        return language_lookup.get(non_english, non_english)

    def set_up(self, translate_into: Callable[[str], None]) -> None:
        for language in SUPPORTED_LANGUAGES:
            translate_into(language)
            self._add_to_combined_lookup_table()
            self._add_to_lookup_table_for(language)

    def _add_to_combined_lookup_table(self) -> None:
        for english in DEFAULT_COMMENT_TYPES_ENGLISH:
            # noinspection PyTypeChecker
            translated = QCoreApplication.translate("CommentTypes", english)
            self._combined_lookup_table[translated] = english

    def _add_to_lookup_table_for(self, language: str) -> None:
        language_lookup: dict[str, str] = {}
        for english in DEFAULT_COMMENT_TYPES_ENGLISH:
            # noinspection PyTypeChecker
            translated = QCoreApplication.translate("CommentTypes", english)
            language_lookup[translated] = english
        self._language_lookup_table[language] = language_lookup
