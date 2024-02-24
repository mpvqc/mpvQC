# mpvQC
#
# Copyright (C) 2022 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from functools import cached_property

from PySide6.QtCore import QDir, QTranslator


class LookupTable:

    def __init__(self):
        self._combined_lookup_table: dict[str, str] = {}
        self._language_lookup_table: dict[str, dict[str, str]] = {}

        self._translator = QTranslator()
        try:
            self._create_lookup_tables()
        finally:
            del self._translator

    def _create_lookup_tables(self) -> None:
        for identifier in self._language_identifiers():
            assert self._translator.load(f':/i18n/{identifier}.qm'), f'Cannot load language: {identifier}'
            self._add_to_combined_lookup_table()
            self._add_to_language_lookup_table(language=identifier)

    @staticmethod
    def _language_identifiers() -> list[str]:
        identifiers = []
        for identifier_qm in QDir(':/i18n').entryList():
            identifier, _, _ = identifier_qm.partition('.')
            identifiers.append(identifier)
        return identifiers

    @property
    def _default_comment_types(self) -> list[str]:
        return ['Translation', 'Spelling', 'Punctuation', 'Phrasing', 'Timing', 'Typeset', 'Note']

    def _add_to_combined_lookup_table(self) -> None:
        for english in self._default_comment_types:
            translated = self._translator.translate("CommentTypes", english)
            self._combined_lookup_table[translated] = english

    def _add_to_language_lookup_table(self, language: str) -> None:
        language_lookup: dict[str, str] = {}
        for english in self._default_comment_types:
            translated = self._translator.translate("CommentTypes", english)
            language_lookup[translated] = english
        self._language_lookup_table[language] = language_lookup

    def lookup(self, comment_type: str, language: str or None = None) -> str:
        if language is None:
            return self._combined_lookup_table.get(comment_type, comment_type)

        mapping = self._language_lookup_table.get(language, {})
        return mapping.get(comment_type, comment_type)


class ReverseTranslatorService:
    """Service that offers reverse translation of comment types.
    It provides comment type identifiers mpvQC internally uses for the comment type model"""

    @cached_property
    def _lookup_table(self):
        return LookupTable()

    def lookup(self, comment_type_in_current_language: str) -> str:
        return self._lookup_table.lookup(comment_type_in_current_language)

    def lookup_specific_language(self, comment_type_in_current_language: str, language: str) -> str:
        return self._lookup_table.lookup(comment_type_in_current_language, language)
