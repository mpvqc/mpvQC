# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.appearance import Appearance, ColorScheme, Dark
from mpvqc.services import ColorSchemeService, PaletteCatalogService, SettingsService

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtCore import SignalInstance

    from mpvqc.services.palette_catalog import PaletteFamily

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@dataclass(frozen=True)
class PaletteInputs:
    appearance: Appearance
    color_scheme: ColorScheme


@dataclass(frozen=True)
class PaletteProps:
    is_dark: bool
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
    section_card: str
    tooltip_background: str
    tooltip_text: str
    row_base: str
    row_base_text: str
    row_stripe: str
    row_stripe_text: str
    row_selected: str
    row_selected_text: str


def derive_palette_props(
    inputs: PaletteInputs,
    palette_family_for: Callable[[ColorScheme], PaletteFamily],
) -> PaletteProps:
    palette = palette_family_for(inputs.color_scheme).palette_of(inputs.appearance)
    return PaletteProps(
        is_dark=isinstance(inputs.color_scheme, Dark),
        background=palette.background,
        foreground=palette.foreground,
        hint=palette.hint,
        accent=palette.accent,
        separator=palette.separator,
        error=palette.error,
        error_text=palette.error_text,
        header_background=palette.header_background,
        popup_background=palette.popup_background,
        popup_text=palette.popup_text,
        menu_background=palette.menu_background,
        dialog_background=palette.dialog_background,
        section_card=palette.section_card,
        tooltip_background=palette.tooltip_background,
        tooltip_text=palette.tooltip_text,
        row_base=palette.row_base,
        row_base_text=palette.row_base_text,
        row_stripe=palette.row_stripe,
        row_stripe_text=palette.row_stripe_text,
        row_selected=palette.row_selected,
        row_selected_text=palette.row_selected_text,
    )


@QmlElement
class MpvqcPaletteViewModel(QObject):
    _catalog = inject.attr(PaletteCatalogService)
    _color_scheme_service = inject.attr(ColorSchemeService)
    _settings = inject.attr(SettingsService)

    isDarkChanged = Signal(bool)
    backgroundChanged = Signal(str)
    foregroundChanged = Signal(str)
    hintChanged = Signal(str)
    accentChanged = Signal(str)
    separatorChanged = Signal(str)
    errorChanged = Signal(str)
    errorTextChanged = Signal(str)
    headerBackgroundChanged = Signal(str)
    popupBackgroundChanged = Signal(str)
    popupTextChanged = Signal(str)
    menuBackgroundChanged = Signal(str)
    dialogBackgroundChanged = Signal(str)
    sectionCardChanged = Signal(str)
    tooltipBackgroundChanged = Signal(str)
    tooltipTextChanged = Signal(str)
    rowBaseChanged = Signal(str)
    rowBaseTextChanged = Signal(str)
    rowStripeChanged = Signal(str)
    rowStripeTextChanged = Signal(str)
    rowSelectedChanged = Signal(str)
    rowSelectedTextChanged = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self._inputs = PaletteInputs(
            appearance=self._settings.appearance,
            color_scheme=self._color_scheme_service.color_scheme,
        )
        self._props = self._derive()

        self._settings.appearance_changed.connect(self._fold_appearance)
        self._color_scheme_service.color_scheme_changed.connect(self._fold_color_scheme)

    def _derive(self) -> PaletteProps:
        return derive_palette_props(self._inputs, self._catalog.palette_family_for)

    @Slot(Appearance)
    def _fold_appearance(self, value: Appearance) -> None:
        self._update(replace(self._inputs, appearance=value))

    @Slot(object)
    def _fold_color_scheme(self, value: ColorScheme) -> None:
        self._update(replace(self._inputs, color_scheme=value))

    def _update(self, inputs: PaletteInputs) -> None:
        self._inputs = inputs
        new, old = self._derive(), self._props
        if new == old:
            return
        self._props = new
        self._emit_if_changed(self.isDarkChanged, new.is_dark, old.is_dark)
        self._emit_if_changed(self.backgroundChanged, new.background, old.background)
        self._emit_if_changed(self.foregroundChanged, new.foreground, old.foreground)
        self._emit_if_changed(self.hintChanged, new.hint, old.hint)
        self._emit_if_changed(self.accentChanged, new.accent, old.accent)
        self._emit_if_changed(self.separatorChanged, new.separator, old.separator)
        self._emit_if_changed(self.errorChanged, new.error, old.error)
        self._emit_if_changed(self.errorTextChanged, new.error_text, old.error_text)
        self._emit_if_changed(self.headerBackgroundChanged, new.header_background, old.header_background)
        self._emit_if_changed(self.popupBackgroundChanged, new.popup_background, old.popup_background)
        self._emit_if_changed(self.popupTextChanged, new.popup_text, old.popup_text)
        self._emit_if_changed(self.menuBackgroundChanged, new.menu_background, old.menu_background)
        self._emit_if_changed(self.dialogBackgroundChanged, new.dialog_background, old.dialog_background)
        self._emit_if_changed(self.sectionCardChanged, new.section_card, old.section_card)
        self._emit_if_changed(self.tooltipBackgroundChanged, new.tooltip_background, old.tooltip_background)
        self._emit_if_changed(self.tooltipTextChanged, new.tooltip_text, old.tooltip_text)
        self._emit_if_changed(self.rowBaseChanged, new.row_base, old.row_base)
        self._emit_if_changed(self.rowBaseTextChanged, new.row_base_text, old.row_base_text)
        self._emit_if_changed(self.rowStripeChanged, new.row_stripe, old.row_stripe)
        self._emit_if_changed(self.rowStripeTextChanged, new.row_stripe_text, old.row_stripe_text)
        self._emit_if_changed(self.rowSelectedChanged, new.row_selected, old.row_selected)
        self._emit_if_changed(self.rowSelectedTextChanged, new.row_selected_text, old.row_selected_text)

    @staticmethod
    def _emit_if_changed(notify: SignalInstance, new_value: str | bool, old_value: str | bool) -> None:
        if new_value != old_value:
            notify.emit(new_value)

    @Property(bool, notify=isDarkChanged)
    def isDark(self) -> bool:
        return self._props.is_dark

    @Property(str, notify=backgroundChanged)
    def background(self) -> str:
        return self._props.background

    @Property(str, notify=foregroundChanged)
    def foreground(self) -> str:
        return self._props.foreground

    @Property(str, notify=hintChanged)
    def hint(self) -> str:
        return self._props.hint

    @Property(str, notify=accentChanged)
    def accent(self) -> str:
        return self._props.accent

    @Property(str, notify=separatorChanged)
    def separator(self) -> str:
        return self._props.separator

    @Property(str, notify=errorChanged)
    def error(self) -> str:
        return self._props.error

    @Property(str, notify=errorTextChanged)
    def errorText(self) -> str:
        return self._props.error_text

    @Property(str, notify=headerBackgroundChanged)
    def headerBackground(self) -> str:
        return self._props.header_background

    @Property(str, notify=popupBackgroundChanged)
    def popupBackground(self) -> str:
        return self._props.popup_background

    @Property(str, notify=popupTextChanged)
    def popupText(self) -> str:
        return self._props.popup_text

    @Property(str, notify=menuBackgroundChanged)
    def menuBackground(self) -> str:
        return self._props.menu_background

    @Property(str, notify=dialogBackgroundChanged)
    def dialogBackground(self) -> str:
        return self._props.dialog_background

    @Property(str, notify=sectionCardChanged)
    def sectionCard(self) -> str:
        return self._props.section_card

    @Property(str, notify=tooltipBackgroundChanged)
    def tooltipBackground(self) -> str:
        return self._props.tooltip_background

    @Property(str, notify=tooltipTextChanged)
    def tooltipText(self) -> str:
        return self._props.tooltip_text

    @Property(str, notify=rowBaseChanged)
    def rowBase(self) -> str:
        return self._props.row_base

    @Property(str, notify=rowBaseTextChanged)
    def rowBaseText(self) -> str:
        return self._props.row_base_text

    @Property(str, notify=rowStripeChanged)
    def rowStripe(self) -> str:
        return self._props.row_stripe

    @Property(str, notify=rowStripeTextChanged)
    def rowStripeText(self) -> str:
        return self._props.row_stripe_text

    @Property(str, notify=rowSelectedChanged)
    def rowSelected(self) -> str:
        return self._props.row_selected

    @Property(str, notify=rowSelectedTextChanged)
    def rowSelectedText(self) -> str:
        return self._props.row_selected_text
