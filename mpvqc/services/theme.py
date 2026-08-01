# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
from dataclasses import dataclass
from functools import cached_property

import inject

from mpvqc.appearance import AccentColor, Palette, ThemeIdentifier

from .resource import ResourceService
from .settings import default_theme_identifier


def _dark_palette(accent_color: AccentColor, colors: dict[str, str]) -> Palette:
    return Palette(
        accent_color=accent_color,
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


def _light_palette(accent_color: AccentColor, colors: dict[str, str]) -> Palette:
    return Palette(
        accent_color=accent_color,
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
    identifier: ThemeIdentifier
    name: str
    preview: str
    is_dark: bool
    default_accent: AccentColor
    palettes: tuple[Palette, ...]

    @property
    def palette_count(self) -> int:
        return len(self.palettes)

    @cached_property
    def _palette_by_accent(self) -> dict[AccentColor, Palette]:
        return {palette.accent_color: palette for palette in self.palettes}

    @cached_property
    def _index_by_accent(self) -> dict[AccentColor, int]:
        return {palette.accent_color: idx for idx, palette in enumerate(self.palettes)}

    def palette_for(self, accent_color: AccentColor | None) -> Palette:
        return self._palette_by_accent[self._resolve(accent_color)]

    def palette_index(self, accent_color: AccentColor | None) -> int:
        return self._index_by_accent[self._resolve(accent_color)]

    def _resolve(self, accent_color: AccentColor | None) -> AccentColor:
        if accent_color is None or accent_color not in self._palette_by_accent:
            return self.default_accent
        return accent_color


def _parse_theme(data: dict) -> Theme:
    make_palette = _dark_palette if data["is_dark"] else _light_palette
    return Theme(
        identifier=ThemeIdentifier(data["identifier"]),
        name=data["name"],
        preview=data["preview"],
        is_dark=data["is_dark"],
        default_accent=AccentColor(data["default_accent"]),
        palettes=tuple(make_palette(AccentColor(p["identifier"]), p["colors"]) for p in data["palettes"]),
    )


class ThemeService:
    _resource = inject.attr(ResourceService)

    def __init__(self) -> None:
        raw = json.loads(self._resource.themes_json)
        self._themes = tuple(_parse_theme(t) for t in raw)
        self._id_to_theme: dict[ThemeIdentifier, Theme] = {t.identifier: t for t in self._themes}
        self._id_to_index: dict[ThemeIdentifier, int] = {t.identifier: idx for idx, t in enumerate(self._themes)}

    @property
    def themes(self) -> tuple[Theme, ...]:
        return self._themes

    def theme(self, theme_identifier: ThemeIdentifier) -> Theme:
        theme = self._id_to_theme.get(theme_identifier)
        if theme is None:
            return self._id_to_theme[default_theme_identifier()]
        return theme

    def theme_index(self, theme_identifier: ThemeIdentifier) -> int:
        index = self._id_to_index.get(theme_identifier)
        if index is None:
            return self._id_to_index[default_theme_identifier()]
        return index
