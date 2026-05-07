# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
from dataclasses import dataclass
from functools import cached_property

import inject

from .resource import ResourceService
from .settings import SettingsService

DEFAULT_THEME_IDENTIFIER = "material-you-dark"


@dataclass(frozen=True)
class ThemePalette:
    identifier: str
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

    @cached_property
    def _palette_by_identifier(self) -> dict[str, ThemePalette]:
        return {palette.identifier: palette for palette in self.palettes}

    @cached_property
    def _index_by_identifier(self) -> dict[str, int]:
        return {palette.identifier: idx for idx, palette in enumerate(self.palettes)}

    def palette_for(self, palette_identifier: str) -> ThemePalette:
        return self._palette_by_identifier.get(palette_identifier, self.palettes[0])

    def palette_index(self, palette_identifier: str) -> int:
        return self._index_by_identifier.get(palette_identifier, 0)


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
    _settings = inject.attr(SettingsService)

    def __init__(self) -> None:
        raw = json.loads(self._resource.themes_json)
        self._themes = tuple(_parse_theme(t) for t in raw)
        self._id_to_theme: dict[str, Theme] = {t.identifier: t for t in self._themes}
        self._id_to_index: dict[str, int] = {t.identifier: idx for idx, t in enumerate(self._themes)}

    @property
    def previews(self) -> tuple[Theme, ...]:
        return self._themes

    def theme(self, theme_identifier: str | None = None) -> Theme:
        if theme_identifier is None:
            theme_identifier = self._settings.theme_identifier
        theme = self._id_to_theme.get(theme_identifier) or self._id_to_theme.get(DEFAULT_THEME_IDENTIFIER)
        if theme is None:
            msg = f"Theme identifier {theme_identifier} not found in themes.json"
            raise ValueError(msg)
        return theme

    def theme_index(self, theme_identifier: str | None = None) -> int:
        if theme_identifier is None:
            theme_identifier = self._settings.theme_identifier
        if (idx := self._id_to_index.get(theme_identifier)) is not None:
            return idx
        if (idx := self._id_to_index.get(DEFAULT_THEME_IDENTIFIER)) is not None:
            return idx
        msg = f"Theme identifier {theme_identifier} not found in themes.json"
        raise ValueError(msg)
