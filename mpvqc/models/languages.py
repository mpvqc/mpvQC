# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import typing
from dataclasses import dataclass

from PySide6.QtCore import QT_TRANSLATE_NOOP, QAbstractListModel, QByteArray, Qt
from PySide6.QtQml import QmlElement

if typing.TYPE_CHECKING:
    from typing import Any

    from PySide6.QtCore import QModelIndex, QPersistentModelIndex


@dataclass(frozen=True)
class Language:
    language: str
    identifier: str
    translator: str | None = None


LANGUAGES = (
    Language(language=str(QT_TRANSLATE_NOOP("Languages", "German")), identifier="de-DE"),
    Language(language=str(QT_TRANSLATE_NOOP("Languages", "English")), identifier="en-US"),
    Language(language=str(QT_TRANSLATE_NOOP("Languages", "Spanish")), identifier="es-MX", translator="CiferrC"),
    Language(language=str(QT_TRANSLATE_NOOP("Languages", "Hebrew")), identifier="he-IL", translator="cN3rd"),
    Language(language=str(QT_TRANSLATE_NOOP("Languages", "Italian")), identifier="it-IT", translator="maddo"),
    Language(language=str(QT_TRANSLATE_NOOP("Languages", "Portuguese")), identifier="pt-PT", translator="Diogo_23"),
)

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcLanguageModel(QAbstractListModel):
    LanguageRole = Qt.ItemDataRole.UserRole + 1
    IdentifierRole = Qt.ItemDataRole.UserRole + 2
    TranslatorRole = Qt.ItemDataRole.UserRole + 3

    @typing.override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        return len(LANGUAGES)

    @typing.override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or index.row() >= len(LANGUAGES):
            return None

        language = LANGUAGES[index.row()]

        match role:
            case self.LanguageRole:
                return language.language
            case self.IdentifierRole:
                return language.identifier
            case self.TranslatorRole:
                return language.translator

        return None

    @typing.override
    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.LanguageRole: QByteArray(b"language"),
            self.IdentifierRole: QByteArray(b"identifier"),
            self.TranslatorRole: QByteArray(b"translator"),
        }
