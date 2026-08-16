# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, assert_never, override

import inject
from PySide6.QtCore import QAbstractListModel, QByteArray, QCoreApplication, Qt, Slot
from PySide6.QtQml import QmlElement

from mpvqc.appearance.services import (
    COLOR_SCHEME_PREFERENCES,
    AppearancePreference,
    AppearanceSettingsService,
    Dark,
    FollowSystem,
    Light,
    PaletteCatalogService,
    format_color_scheme_preference,
)

if TYPE_CHECKING:
    from typing import Any

    from PySide6.QtCore import QModelIndex, QObject, QPersistentModelIndex

    from mpvqc.appearance.services import ColorSchemePreference


QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@dataclass(frozen=True)
class _Row:
    preference: ColorSchemePreference
    caption: str
    preview_color: str
    alternate_preview_color: str


@QmlElement
class MpvqcColorSchemePreferenceModel(QAbstractListModel):
    _catalog = inject.attr(PaletteCatalogService)
    _settings = inject.attr(AppearanceSettingsService)

    PreferenceRole = Qt.ItemDataRole.UserRole + 1
    CaptionRole = Qt.ItemDataRole.UserRole + 2
    PreviewColorRole = Qt.ItemDataRole.UserRole + 3
    AlternatePreviewColorRole = Qt.ItemDataRole.UserRole + 4
    AccentPreviewColorRole = Qt.ItemDataRole.UserRole + 5
    FollowsSystemRole = Qt.ItemDataRole.UserRole + 6

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._rows = self._build_rows()
        self._accent_preview_colors = self._accent_preview_colors_of(self._settings.appearance_preference)
        self._settings.appearance_preference_changed.connect(self._fold_appearance_preference)

    def _build_rows(self) -> tuple[_Row, ...]:
        return tuple(self._build_row(preference) for preference in COLOR_SCHEME_PREFERENCES)

    def _build_row(self, preference: ColorSchemePreference) -> _Row:
        translate = QCoreApplication.translate
        match preference:
            case FollowSystem():
                return _Row(
                    preference=preference,
                    caption=translate("AppearanceDialog", "System"),
                    preview_color=self._catalog.preview_color_for(Light()),
                    alternate_preview_color=self._catalog.preview_color_for(Dark()),
                )
            case Light():
                return _Row(
                    preference=preference,
                    caption=translate("AppearanceDialog", "Light"),
                    preview_color=self._catalog.preview_color_for(preference),
                    alternate_preview_color="transparent",
                )
            case Dark():
                return _Row(
                    preference=preference,
                    caption=translate("AppearanceDialog", "Dark"),
                    preview_color=self._catalog.preview_color_for(preference),
                    alternate_preview_color="transparent",
                )
            case _:
                assert_never(preference)

    @override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        if parent is not None and parent.isValid():
            return 0
        return len(self._rows)

    @override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        rows = self._rows
        if not index.isValid() or index.row() >= len(rows):
            return None

        row = rows[index.row()]

        match role:
            case self.PreferenceRole:
                return format_color_scheme_preference(row.preference)
            case self.CaptionRole:
                return row.caption
            case self.PreviewColorRole:
                return row.preview_color
            case self.AlternatePreviewColorRole:
                return row.alternate_preview_color
            case self.AccentPreviewColorRole:
                return self._accent_preview_colors[index.row()]
            case self.FollowsSystemRole:
                return isinstance(row.preference, FollowSystem)

        return None

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.PreferenceRole: QByteArray(b"preference"),
            self.CaptionRole: QByteArray(b"caption"),
            self.PreviewColorRole: QByteArray(b"previewColor"),
            self.AlternatePreviewColorRole: QByteArray(b"alternatePreviewColor"),
            self.AccentPreviewColorRole: QByteArray(b"accentPreviewColor"),
            self.FollowsSystemRole: QByteArray(b"followsSystem"),
        }

    @Slot(AppearancePreference)
    def _fold_appearance_preference(self, appearance_preference: AppearancePreference) -> None:
        new, old = self._accent_preview_colors_of(appearance_preference), self._accent_preview_colors
        self._accent_preview_colors = new
        for row, (new_accent_preview_color, old_accent_preview_color) in enumerate(zip(new, old, strict=True)):
            if new_accent_preview_color != old_accent_preview_color:
                index = self.index(row)
                self.dataChanged.emit(index, index, [self.AccentPreviewColorRole])

    def _accent_preview_colors_of(self, appearance_preference: AppearancePreference) -> tuple[str, ...]:
        return tuple(self._accent_preview_color_of(row.preference, appearance_preference) for row in self._rows)

    def _accent_preview_color_of(
        self,
        color_scheme_preference: ColorSchemePreference,
        appearance_preference: AppearancePreference,
    ) -> str:
        match color_scheme_preference:
            case FollowSystem():
                return "transparent"
            case Light() | Dark():
                family = self._catalog.palette_family_for(color_scheme_preference)
                return family.palette_of(appearance_preference).row_selected
            case _:
                assert_never(color_scheme_preference)
