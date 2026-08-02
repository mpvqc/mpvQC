# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, assert_never, override

import inject
from PySide6.QtCore import QAbstractListModel, QByteArray, QCoreApplication, Qt, Slot
from PySide6.QtQml import QmlElement

from mpvqc.appearance.domain import (
    COLOR_SCHEME_PREFERENCES,
    Appearance,
    Dark,
    FollowSystem,
    Light,
    format_color_scheme_preference,
)
from mpvqc.appearance.services import PaletteCatalogService
from mpvqc.services import SettingsService

if TYPE_CHECKING:
    from typing import Any

    from PySide6.QtCore import QModelIndex, QObject, QPersistentModelIndex

    from mpvqc.appearance.domain import ColorSchemePreference


QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@dataclass(frozen=True)
class _Row:
    preference: ColorSchemePreference
    caption: str
    preview: str
    alternate_preview: str


@QmlElement
class MpvqcColorSchemePreferenceModel(QAbstractListModel):
    """Every color scheme preference, in the order the appearance dialog offers them in.

    Following the system owns no color scheme: it carries both previews for the split swatch and no accent.
    """

    _catalog = inject.attr(PaletteCatalogService)
    _settings = inject.attr(SettingsService)

    PreferenceRole = Qt.ItemDataRole.UserRole + 1
    CaptionRole = Qt.ItemDataRole.UserRole + 2
    PreviewRole = Qt.ItemDataRole.UserRole + 3
    AlternatePreviewRole = Qt.ItemDataRole.UserRole + 4
    AccentRole = Qt.ItemDataRole.UserRole + 5

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._rows = self._build_rows()
        self._accents = self._accents_of(self._settings.appearance)
        self._settings.appearance_changed.connect(self._fold_appearance)

    def _build_rows(self) -> tuple[_Row, ...]:
        return tuple(self._build_row(preference) for preference in COLOR_SCHEME_PREFERENCES)

    def _build_row(self, preference: ColorSchemePreference) -> _Row:
        translate = QCoreApplication.translate
        match preference:
            case FollowSystem():
                return _Row(
                    preference=preference,
                    caption=translate("AppearanceDialog", "System"),
                    preview=self._catalog.preview_color_for(Light()),
                    alternate_preview=self._catalog.preview_color_for(Dark()),
                )
            case Light():
                return _Row(
                    preference=preference,
                    caption=translate("AppearanceDialog", "Light"),
                    preview=self._catalog.preview_color_for(preference),
                    alternate_preview="",
                )
            case Dark():
                return _Row(
                    preference=preference,
                    caption=translate("AppearanceDialog", "Dark"),
                    preview=self._catalog.preview_color_for(preference),
                    alternate_preview="",
                )
            case _:
                assert_never(preference)

    def _accents_of(self, appearance: Appearance) -> tuple[str, ...]:
        return tuple(self._accent_of(row.preference, appearance) for row in self._rows)

    def _accent_of(self, preference: ColorSchemePreference, appearance: Appearance) -> str:
        match preference:
            case FollowSystem():
                return ""
            case Light() | Dark():
                return self._catalog.palette_family_for(preference).palette_of(appearance).row_selected
            case _:
                assert_never(preference)

    @Slot(Appearance)
    def _fold_appearance(self, appearance: Appearance) -> None:
        new, old = self._accents_of(appearance), self._accents
        self._accents = new
        for row, (new_accent, old_accent) in enumerate(zip(new, old, strict=True)):
            if new_accent != old_accent:
                index = self.index(row)
                self.dataChanged.emit(index, index, [self.AccentRole])

    @override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        if parent is not None and parent.isValid():
            return 0
        return len(self._rows)

    @override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or index.row() >= self.rowCount():
            return None

        row = self._rows[index.row()]

        match role:
            case self.PreferenceRole:
                return format_color_scheme_preference(row.preference)
            case self.CaptionRole:
                return row.caption
            case self.PreviewRole:
                return row.preview
            case self.AlternatePreviewRole:
                return row.alternate_preview
            case self.AccentRole:
                return self._accents[index.row()]

        return None

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.PreferenceRole: QByteArray(b"preference"),
            self.CaptionRole: QByteArray(b"caption"),
            self.PreviewRole: QByteArray(b"preview"),
            self.AlternatePreviewRole: QByteArray(b"alternatePreview"),
            self.AccentRole: QByteArray(b"accent"),
        }
