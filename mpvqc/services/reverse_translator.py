# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from functools import cached_property

from PySide6.QtCore import QDir, QTranslator


class LookupTable:
    """"""

    def __init__(self):
        self._combined_lookup_table: dict[str, str] = {}

        self._translator = QTranslator()
        try:
            self._create_lookup_tables()
        finally:
            del self._translator

    def _create_lookup_tables(self) -> None:
        for entry_info in QDir(":/i18n").entryInfoList():
            identifier = entry_info.baseName()
            resource_path = entry_info.filePath()
            if not self._translator.load(resource_path):
                msg = f"Cannot load language: {identifier}"
                raise ValueError(msg)
            self._add_to_combined_lookup_table()

    @property
    def _default_comment_types(self) -> list[str]:
        return ["Translation", "Spelling", "Punctuation", "Phrasing", "Timing", "Typeset", "Note"]

    def _add_to_combined_lookup_table(self) -> None:
        for english in self._default_comment_types:
            translated = self._translator.translate("CommentTypes", english)
            self._combined_lookup_table[translated] = english

    def lookup(self, comment_type: str) -> str:
        return self._combined_lookup_table.get(comment_type, comment_type)


class ReverseTranslatorService:
    """Service that offers reverse translation of comment types.
    It provides comment type identifiers mpvQC internally uses for the comment type model"""

    @cached_property
    def _lookup_table(self):
        return LookupTable()

    def lookup(self, comment_type_in_current_language: str) -> str:
        return self._lookup_table.lookup(comment_type_in_current_language)
