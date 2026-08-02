# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, override

import inject
from PySide6.QtCore import QAbstractListModel, QByteArray, QCoreApplication, Qt, Slot
from PySide6.QtQml import QmlElement

from mpvqc.appearance import Appearance, ColorSchemePreference, EffectiveColorScheme
from mpvqc.services import PaletteCatalogService, SettingsService

if TYPE_CHECKING:
    from typing import Any

    from PySide6.QtCore import QModelIndex, QObject, QPersistentModelIndex


QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1

LIGHT = EffectiveColorScheme.LIGHT
DARK = EffectiveColorScheme.DARK


@dataclass(frozen=True)
class _Row:
    preference: ColorSchemePreference
    caption: str
    preview: str
    alternate_preview: str
    color_scheme: EffectiveColorScheme | None


@QmlElement
class MpvqcColorSchemeModel(QAbstractListModel):
    """The three color scheme preferences, in System, Light, Dark order.

    System owns no color scheme: it carries both previews for the split swatch and no accent.
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
        translate = QCoreApplication.translate
        light = self._catalog.preview_color_for(LIGHT)
        dark = self._catalog.preview_color_for(DARK)
        return (
            _Row(
                preference=ColorSchemePreference.SYSTEM,
                caption=translate("AppearanceDialog", "System"),
                preview=light,
                alternate_preview=dark,
                color_scheme=None,
            ),
            _Row(
                preference=ColorSchemePreference.LIGHT,
                caption=translate("AppearanceDialog", "Light"),
                preview=light,
                alternate_preview="",
                color_scheme=LIGHT,
            ),
            _Row(
                preference=ColorSchemePreference.DARK,
                caption=translate("AppearanceDialog", "Dark"),
                preview=dark,
                alternate_preview="",
                color_scheme=DARK,
            ),
        )

    def _accents_of(self, appearance: Appearance) -> tuple[str, ...]:
        return tuple(self._accent_of(row, appearance) for row in self._rows)

    def _accent_of(self, row: _Row, appearance: Appearance) -> str:
        if row.color_scheme is None:
            return ""
        palette_family = self._catalog.palette_family_for(row.color_scheme)
        return palette_family.palette_for(appearance.accent_color_for(row.color_scheme)).row_selected

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
                return row.preference.value
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
