# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import functools

from PySide6.QtCore import QCoreApplication, QDir, QTranslator

from .settings import default_comment_types


def translate_comment_type(comment_type: str) -> str:
    return QCoreApplication.translate("CommentTypes", comment_type)


def reverse_translate_comment_type(translated_comment_type: str) -> str:
    table = _lookup_table()
    return table.get(translated_comment_type, translated_comment_type)


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
            if translated:
                table[translated] = english

    return table
