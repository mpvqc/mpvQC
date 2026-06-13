# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, override

import inject
from PySide6.QtCore import (
    QAbstractListModel,
    QByteArray,
    QCollator,
    QCoreApplication,
    QSortFilterProxyModel,
    Qt,
    Slot,
)
from PySide6.QtQml import QmlElement

from mpvqc.datamodels import LANGUAGES
from mpvqc.services import InternationalizationService

if TYPE_CHECKING:
    from typing import Any

    from PySide6.QtCore import QModelIndex, QObject, QPersistentModelIndex


QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


class MpvqcLanguageModelBackend(QAbstractListModel):
    LanguageRole = Qt.ItemDataRole.UserRole + 1
    IdentifierRole = Qt.ItemDataRole.UserRole + 2
    TranslatorsRole = Qt.ItemDataRole.UserRole + 3

    @override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        if parent is not None and parent.isValid():
            return 0
        return len(LANGUAGES)

    @override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or index.row() >= self.rowCount():
            return None

        language = LANGUAGES[index.row()]

        match role:
            case self.LanguageRole:
                return language.language
            case self.IdentifierRole:
                return language.identifier
            case self.TranslatorsRole:
                return list(language.translators)

        return None

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.LanguageRole: QByteArray(b"language"),
            self.IdentifierRole: QByteArray(b"identifier"),
            self.TranslatorsRole: QByteArray(b"translators"),
        }


@QmlElement
class MpvqcLanguageModel(QSortFilterProxyModel):
    _i18n = inject.attr(InternationalizationService)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._collator = QCollator()
        self.setSourceModel(MpvqcLanguageModelBackend(self))
        self.sort(0)
        self._i18n.retranslated.connect(self._resort)

    @Slot()
    def _resort(self) -> None:
        self._collator = QCollator()
        self.invalidate()

    @override
    def lessThan(
        self,
        source_left: QModelIndex | QPersistentModelIndex,
        source_right: QModelIndex | QPersistentModelIndex,
    ) -> bool:
        left = QCoreApplication.translate("Languages", source_left.data(MpvqcLanguageModelBackend.LanguageRole))
        right = QCoreApplication.translate("Languages", source_right.data(MpvqcLanguageModelBackend.LanguageRole))
        return self._collator.compare(left, right) < 0
