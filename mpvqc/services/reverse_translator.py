# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import functools
import logging

from PySide6.QtCore import QDir, QTranslator

from .settings import default_comment_types

logger = logging.getLogger(__name__)


class ReverseTranslatorService:
    @staticmethod
    def lookup(comment_type_in_current_language: str) -> str:
        table = _lookup_table()
        return table.get(comment_type_in_current_language, comment_type_in_current_language)


@functools.cache
def _lookup_table() -> dict[str, str]:
    table: dict[str, str] = {}
    translator = QTranslator()

    for entry_info in QDir(":/i18n").entryInfoList():
        if not translator.load(entry_info.filePath()):
            msg = f"Cannot load language: {entry_info.baseName()}"
            raise ValueError(msg)

        for english in default_comment_types():
            translated = translator.translate("CommentTypes", english)
            if translated is None:
                msg = f"Failed to translate comment type: {english!r}"
                logger.error(msg)
                raise ValueError(msg)
            table[translated] = english

    return table
