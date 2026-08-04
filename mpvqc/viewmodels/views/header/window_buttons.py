# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass, replace

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import PlatformService, WindowButtonPreference

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@dataclass(frozen=True)
class WindowButtonsInputs:
    preference: WindowButtonPreference


@dataclass(frozen=True)
class WindowButtonsProps:
    show_minimize_button: bool
    show_maximize_button: bool
    show_close_button: bool


def derive_window_buttons_props(inputs: WindowButtonsInputs) -> WindowButtonsProps:
    return WindowButtonsProps(
        show_minimize_button=inputs.preference.minimize,
        show_maximize_button=inputs.preference.maximize,
        show_close_button=inputs.preference.close,
    )


@QmlElement
class MpvqcWindowButtonsViewModel(QObject):
    _platform = inject.attr(PlatformService)

    showMinimizeButtonChanged = Signal(bool)
    showMaximizeButtonChanged = Signal(bool)
    showCloseButtonChanged = Signal(bool)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._inputs = WindowButtonsInputs(preference=self._platform.window_button_preference)
        self._props = derive_window_buttons_props(self._inputs)

        self._platform.window_button_preference_changed.connect(self._fold_preference)

    @Slot(WindowButtonPreference)
    def _fold_preference(self, value: WindowButtonPreference) -> None:
        self._update(replace(self._inputs, preference=value))

    def _update(self, inputs: WindowButtonsInputs) -> None:
        self._inputs = inputs
        new, old = derive_window_buttons_props(self._inputs), self._props
        if new == old:
            return
        self._props = new
        if new.show_minimize_button != old.show_minimize_button:
            self.showMinimizeButtonChanged.emit(new.show_minimize_button)
        if new.show_maximize_button != old.show_maximize_button:
            self.showMaximizeButtonChanged.emit(new.show_maximize_button)
        if new.show_close_button != old.show_close_button:
            self.showCloseButtonChanged.emit(new.show_close_button)

    @Property(bool, notify=showMinimizeButtonChanged)
    def showMinimizeButton(self) -> bool:
        return self._props.show_minimize_button

    @Property(bool, notify=showMaximizeButtonChanged)
    def showMaximizeButton(self) -> bool:
        return self._props.show_maximize_button

    @Property(bool, notify=showCloseButtonChanged)
    def showCloseButton(self) -> bool:
        return self._props.show_close_button
