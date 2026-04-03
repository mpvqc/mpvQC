# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
from dataclasses import dataclass

import inject

from .resource import ResourceService


@dataclass(frozen=True)
class ThemePalette:
    background: str
    background_alternate: str
    foreground: str
    foreground_alternate: str
    control: str
    row_highlight: str
    row_highlight_text: str
    row_base: str
    row_base_text: str
    row_base_alternate: str
    row_base_alternate_text: str


@dataclass(frozen=True)
class Theme:
    identifier: str
    name: str
    preview: str
    is_dark: bool
    palettes: tuple[ThemePalette, ...]

    @property
    def palette_count(self) -> int:
        return len(self.palettes)


def _parse_theme(data: dict) -> Theme:
    return Theme(
        identifier=data["identifier"],
        name=data["name"],
        preview=data["preview"],
        is_dark=data["is_dark"],
        palettes=tuple(ThemePalette(**p) for p in data["palettes"]),
    )


class ThemeService:
    _resource = inject.attr(ResourceService)

    def __init__(self) -> None:
        raw = json.loads(self._resource.themes_json)
        self._themes = tuple(_parse_theme(t) for t in raw)
        self._id_to_theme: dict[str, Theme] = {t.identifier: t for t in self._themes}
        self._id_to_index: dict[str, int] = {t.identifier: idx for idx, t in enumerate(self._themes)}

    @property
    def previews(self) -> tuple[Theme, ...]:
        return self._themes

    def theme(self, theme_identifier: str) -> Theme:
        theme = self._id_to_theme.get(theme_identifier) or self._id_to_theme.get("material-you-dark")
        if theme is None:
            msg = f"Theme identifier {theme_identifier} not found in themes.json"
            raise ValueError(msg)
        return theme

    def palette_at(self, theme_identifier: str, index: int) -> ThemePalette:
        theme = self.theme(theme_identifier)
        if not 0 <= index < theme.palette_count:
            msg = f"Palette index {index} out of range for theme '{theme_identifier}' ({theme.palette_count} palettes)"
            raise ValueError(msg)
        return theme.palettes[index]

    def theme_index(self, theme_identifier: str) -> int:
        if (idx := self._id_to_index.get(theme_identifier)) is not None:
            return idx
        if (idx := self._id_to_index.get("material-you-dark")) is not None:
            return idx
        return 1
