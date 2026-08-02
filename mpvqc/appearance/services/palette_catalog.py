# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
from dataclasses import dataclass
from functools import cached_property
from typing import assert_never

import inject

from mpvqc.appearance.domain import (
    AccentColor,
    Appearance,
    ColorScheme,
    Dark,
    Light,
    NoPreference,
    Palette,
    parse_color_scheme,
)
from mpvqc.services.resource import ResourceService


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
        section_card=colors["surfaceContainerHighest"],
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
        section_card=colors["surfaceContainerLowest"],
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
class PaletteFamily:
    preview: str
    color_scheme: ColorScheme
    default_accent: AccentColor
    palettes: tuple[Palette, ...]

    @cached_property
    def _palette_by_accent(self) -> dict[AccentColor, Palette]:
        return {palette.accent_color: palette for palette in self.palettes}

    @cached_property
    def _index_by_accent(self) -> dict[AccentColor, int]:
        return {palette.accent_color: idx for idx, palette in enumerate(self.palettes)}

    def palette_of(self, appearance: Appearance) -> Palette:
        return self._palette_by_accent[self._resolve(appearance)]

    def palette_index_of(self, appearance: Appearance) -> int:
        return self._index_by_accent[self._resolve(appearance)]

    def _resolve(self, appearance: Appearance) -> AccentColor:
        preference = appearance.accent_color_preference_for(self.color_scheme)
        match preference:
            case NoPreference():
                return self.default_accent
            case AccentColor():
                return preference if preference in self._palette_by_accent else self.default_accent
            case _:
                assert_never(preference)


def _parse_palette_family(data: dict) -> PaletteFamily:
    color_scheme = parse_color_scheme(data["color_scheme"])
    match color_scheme:
        case Light():
            make_palette = _light_palette
        case Dark():
            make_palette = _dark_palette
        case _:
            assert_never(color_scheme)
    return PaletteFamily(
        preview=data["preview"],
        color_scheme=color_scheme,
        default_accent=AccentColor(data["default_accent"]),
        palettes=tuple(make_palette(AccentColor(p["identifier"]), p["colors"]) for p in data["palettes"]),
    )


class PaletteCatalogService:
    _resource = inject.attr(ResourceService)

    def __init__(self) -> None:
        raw = json.loads(self._resource.palette_catalog_json)
        self._palette_families = tuple(_parse_palette_family(entry) for entry in raw)
        self._by_scheme: dict[ColorScheme, PaletteFamily] = {}
        for palette_family in self._palette_families:
            self._by_scheme.setdefault(palette_family.color_scheme, palette_family)

    @property
    def palette_families(self) -> tuple[PaletteFamily, ...]:
        return self._palette_families

    def palette_family_for(self, color_scheme: ColorScheme) -> PaletteFamily:
        return self._by_scheme[color_scheme]

    def preview_color_for(self, color_scheme: ColorScheme) -> str:
        return self.palette_family_for(color_scheme).preview
