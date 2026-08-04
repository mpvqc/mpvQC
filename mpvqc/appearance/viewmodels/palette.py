# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement, QmlUncreatable

from mpvqc.appearance.domain import AppearancePreference, ColorScheme, Dark
from mpvqc.appearance.services import AppearanceSettingsService, ColorSchemeService, PaletteCatalogService

if TYPE_CHECKING:
    from collections.abc import Callable

    from mpvqc.appearance.domain import Palette
    from mpvqc.appearance.services import PaletteFamily

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@dataclass(frozen=True)
class PaletteInputs:
    appearance_preference: AppearancePreference
    color_scheme: ColorScheme


@dataclass(frozen=True)
class PaletteProps:
    is_dark: bool
    palette: Palette


def derive_palette_props(
    inputs: PaletteInputs,
    palette_family_for: Callable[[ColorScheme], PaletteFamily],
) -> PaletteProps:
    return PaletteProps(
        is_dark=isinstance(inputs.color_scheme, Dark),
        palette=palette_family_for(inputs.color_scheme).palette_of(inputs.appearance_preference),
    )


@QmlElement
@QmlUncreatable("constructed by MpvqcPaletteViewModel")
class MpvqcPalette(QObject):
    changed = Signal()

    def __init__(self, palette: Palette, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._palette = palette

    def set_palette(self, palette: Palette) -> None:
        self._palette = palette
        self.changed.emit()

    @Property(str, notify=changed)
    def background(self) -> str:
        return self._palette.background

    @Property(str, notify=changed)
    def foreground(self) -> str:
        return self._palette.foreground

    @Property(str, notify=changed)
    def hint(self) -> str:
        return self._palette.hint

    @Property(str, notify=changed)
    def accent(self) -> str:
        return self._palette.accent

    @Property(str, notify=changed)
    def separator(self) -> str:
        return self._palette.separator

    @Property(str, notify=changed)
    def error(self) -> str:
        return self._palette.error

    @Property(str, notify=changed)
    def errorText(self) -> str:
        return self._palette.error_text

    @Property(str, notify=changed)
    def headerBackground(self) -> str:
        return self._palette.header_background

    @Property(str, notify=changed)
    def popupBackground(self) -> str:
        return self._palette.popup_background

    @Property(str, notify=changed)
    def popupText(self) -> str:
        return self._palette.popup_text

    @Property(str, notify=changed)
    def menuBackground(self) -> str:
        return self._palette.menu_background

    @Property(str, notify=changed)
    def dialogBackground(self) -> str:
        return self._palette.dialog_background

    @Property(str, notify=changed)
    def sectionCard(self) -> str:
        return self._palette.section_card

    @Property(str, notify=changed)
    def tooltipBackground(self) -> str:
        return self._palette.tooltip_background

    @Property(str, notify=changed)
    def tooltipText(self) -> str:
        return self._palette.tooltip_text

    @Property(str, notify=changed)
    def rowBase(self) -> str:
        return self._palette.row_base

    @Property(str, notify=changed)
    def rowBaseText(self) -> str:
        return self._palette.row_base_text

    @Property(str, notify=changed)
    def rowStripe(self) -> str:
        return self._palette.row_stripe

    @Property(str, notify=changed)
    def rowStripeText(self) -> str:
        return self._palette.row_stripe_text

    @Property(str, notify=changed)
    def rowSelected(self) -> str:
        return self._palette.row_selected

    @Property(str, notify=changed)
    def rowSelectedText(self) -> str:
        return self._palette.row_selected_text


@QmlElement
class MpvqcPaletteViewModel(QObject):
    _catalog = inject.attr(PaletteCatalogService)
    _color_scheme_service = inject.attr(ColorSchemeService)
    _settings = inject.attr(AppearanceSettingsService)

    isDarkChanged = Signal(bool)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self._inputs = PaletteInputs(
            appearance_preference=self._settings.appearance_preference,
            color_scheme=self._color_scheme_service.color_scheme,
        )
        self._props = self._derive()
        self._palette = MpvqcPalette(self._props.palette, self)

        self._settings.appearance_preference_changed.connect(self._fold_appearance_preference)
        self._color_scheme_service.color_scheme_changed.connect(self._fold_color_scheme)

    def _derive(self) -> PaletteProps:
        return derive_palette_props(self._inputs, self._catalog.palette_family_for)

    @Slot(AppearancePreference)
    def _fold_appearance_preference(self, value: AppearancePreference) -> None:
        self._update(replace(self._inputs, appearance_preference=value))

    @Slot(object)
    def _fold_color_scheme(self, value: ColorScheme) -> None:
        self._update(replace(self._inputs, color_scheme=value))

    def _update(self, inputs: PaletteInputs) -> None:
        self._inputs = inputs
        new, old = self._derive(), self._props
        if new == old:
            return
        self._props = new
        # Unconditional behind the guard above: is_dark cannot move while the palette holds still,
        # since flipping the color scheme swaps the palette family.
        self._palette.set_palette(new.palette)
        if new.is_dark != old.is_dark:
            self.isDarkChanged.emit(new.is_dark)

    @Property(bool, notify=isDarkChanged)
    def isDark(self) -> bool:
        return self._props.is_dark

    @Property(MpvqcPalette, constant=True, final=True)
    def palette(self) -> MpvqcPalette:
        return self._palette
