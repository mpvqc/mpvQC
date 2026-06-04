# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
from dataclasses import dataclass
from functools import cached_property
from typing import Self

import inject

from .resource import ResourceService
from .settings import SettingsService


@dataclass(frozen=True)
class ThemePalette:
    identifier: str
    background: str
    foreground: str
    hint: str
    accent: str
    separator: str
    error: str
    error_text: str
    header_background: str
    popup_background: str
    popup_text: str
    menu_background: str
    dialog_background: str
    tooltip_background: str
    tooltip_text: str
    row_base: str
    row_base_text: str
    row_stripe: str
    row_stripe_text: str
    row_selected: str
    row_selected_text: str

    @classmethod
    def dark(cls, identifier: str, colors: dict[str, str]) -> Self:
        return cls(
            identifier=identifier,
            background=colors["surface"],
            foreground=colors["onSurfaceVariant"],
            hint=colors["outline"],
            accent=colors["primary"],
            separator=colors["surfaceVariant"],
            error=colors["error"],
            error_text=colors["onError"],
            header_background=colors["surfaceContainer"],
            popup_background=colors["surfaceContainerHigh"],
            popup_text=colors["onSurfaceVariant"],
            menu_background=colors["surfaceContainer"],
            dialog_background=colors["surfaceContainerHigh"],
            tooltip_background=colors["inverseSurface"],
            tooltip_text=colors["inverseOnSurface"],
            row_base=colors["surface"],
            row_base_text=colors["onSurfaceVariant"],
            row_stripe=colors["surfaceContainerLow"],
            row_stripe_text=colors["onSurfaceVariant"],
            row_selected=colors["inversePrimary"],
            row_selected_text=colors["onSurface"],
        )

    @classmethod
    def light(cls, identifier: str, colors: dict[str, str]) -> Self:
        return cls(
            identifier=identifier,
            background=colors["surfaceContainerLow"],
            foreground=colors["onSurfaceVariant"],
            hint=colors["outline"],
            accent=colors["secondary"],
            separator=colors["outlineVariant"],
            error=colors["error"],
            error_text=colors["onError"],
            header_background=colors["surfaceContainer"],
            popup_background=colors["secondaryContainer"],
            popup_text=colors["onSecondaryContainer"],
            menu_background=colors["surfaceContainer"],
            dialog_background=colors["surfaceContainerHigh"],
            tooltip_background=colors["inverseSurface"],
            tooltip_text=colors["inverseOnSurface"],
            row_base=colors["surfaceContainerLow"],
            row_base_text=colors["onSurfaceVariant"],
            row_stripe=colors["surfaceContainerHighest"],
            row_stripe_text=colors["onSurfaceVariant"],
            row_selected=colors["primary"],
            row_selected_text=colors["onPrimary"],
        )


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
    make_palette = ThemePalette.dark if data["is_dark"] else ThemePalette.light
    return Theme(
        identifier=data["identifier"],
        name=data["name"],
        preview=data["preview"],
        is_dark=data["is_dark"],
        palettes=tuple(make_palette(p["identifier"], p["colors"]) for p in data["palettes"]),
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
        theme = self._id_to_theme.get(theme_identifier) or self._id_to_theme.get(
            self._settings.default_theme_identifier()
        )
        if theme is None:
            msg = f"Theme identifier {theme_identifier} not found in themes.json"
            raise ValueError(msg)
        return theme

    def theme_index(self, theme_identifier: str | None = None) -> int:
        if theme_identifier is None:
            theme_identifier = self._settings.theme_identifier
        if (idx := self._id_to_index.get(theme_identifier)) is not None:
            return idx
        if (idx := self._id_to_index.get(self._settings.default_theme_identifier())) is not None:
            return idx
        msg = f"Theme identifier {theme_identifier} not found in themes.json"
        raise ValueError(msg)
