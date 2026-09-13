# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import inject
from PySide6.QtCore import QCoreApplication, QDeadlineTimer, QObject, QThreadPool
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlContext, QQmlEngine, QQmlExpression

from mpvqc.appearance.viewmodels import MpvqcPaletteViewModel
from mpvqc.comments.viewmodels import MpvqcCommentLabelWidthCalculatorViewModel, MpvqcCommentTableTimeFormatViewModel
from mpvqc.exporting.services import ExportService
from mpvqc.window.services import MainWindowService
from mpvqc.window.viewmodels import MpvqcPlatformViewModel, MpvqcWindowControlsViewModel
from testqml.injections import configure_injections, current_platform

_BACKGROUND_JOBS_TIMEOUT_MS = 10_000


class _SwappedViewModel(NamedTuple):
    module_uri: str
    singleton_name: str
    property_name: str
    view_model_class: type[QObject]


_PLATFORM_VIEW_MODEL = _SwappedViewModel(
    "io.github.mpvqc.mpvQC.Utility",
    "MpvqcPlatform",
    "_viewModel",
    MpvqcPlatformViewModel,
)

# Singleton-held view models subscribe to service signals or snapshot service
# state when constructed, so reset_state() swaps in fresh instances wired to the
# freshly configured services.
_SWAPPED_VIEW_MODELS = (
    _PLATFORM_VIEW_MODEL,
    _SwappedViewModel(
        "io.github.mpvqc.mpvQC.Utility",
        "MpvqcWindowUtility",
        "_viewModel",
        MpvqcWindowControlsViewModel,
    ),
    _SwappedViewModel(
        "io.github.mpvqc.mpvQC.Utility",
        "MpvqcAppearance",
        "_viewModel",
        MpvqcPaletteViewModel,
    ),
    _SwappedViewModel(
        "io.github.mpvqc.mpvQC.Utility",
        "MpvqcLabelWidthCalculator",
        "viewModel",
        MpvqcCommentLabelWidthCalculatorViewModel,
    ),
    _SwappedViewModel(
        "io.github.mpvqc.mpvQC.Views.Table",
        "MpvqcTableUtility",
        "viewModel",
        MpvqcCommentTableTimeFormatViewModel,
    ),
)


def reset_state(engine: QQmlEngine) -> None:
    configure_injections()
    _rebind_main_window()
    _recreate_and_replace_singleton_view_models(engine, _SWAPPED_VIEW_MODELS)


def switch_platform(engine: QQmlEngine, name: str) -> None:
    current_platform.switch(name)
    _recreate_and_replace_singleton_view_models(engine, (_PLATFORM_VIEW_MODEL,))


def _rebind_main_window() -> None:
    # The Quick Test runner owns the engine; its first window hosts the TestCase.
    test_window = QGuiApplication.topLevelWindows()[0]
    inject.instance(MainWindowService).initialize(test_window)


def _recreate_and_replace_singleton_view_models(engine: QQmlEngine, entries: tuple[_SwappedViewModel, ...]) -> None:
    for entry in entries:
        singleton = engine.singletonInstance(entry.module_uri, entry.singleton_name)
        if not isinstance(singleton, QObject):
            msg = f"Cannot resolve singleton {entry.singleton_name}"
            raise TypeError(msg)
        previous = [child for child in singleton.children() if isinstance(child, entry.view_model_class)]
        view_model = entry.view_model_class()
        view_model.setParent(singleton)
        # Assign through a JS expression, not QQmlProperty.write: only a JS
        # assignment removes the property's declarative initializer. Left in
        # place, it re-fires when the previous view model is destroyed and
        # stomps the fresh one with null.
        swap_context = QQmlContext(engine.rootContext())
        swap_context.setContextProperty("__freshViewModel", view_model)
        expression = QQmlExpression(swap_context, singleton, f"{entry.property_name} = __freshViewModel")
        expression.evaluate()
        if expression.hasError():
            msg = f"Cannot swap {entry.property_name} on {entry.singleton_name}: {expression.error()}"
            raise RuntimeError(msg)
        for old in previous:
            old.deleteLater()


def wait_for_background_jobs() -> None:
    exporter = inject.instance(ExportService)
    deadline = QDeadlineTimer(_BACKGROUND_JOBS_TIMEOUT_MS)
    while True:
        QThreadPool.globalInstance().waitForDone(deadline.remainingTime())
        QCoreApplication.processEvents()
        if exporter.is_idle:
            return
        if deadline.hasExpired():
            msg = f"Background jobs still pending after {_BACKGROUND_JOBS_TIMEOUT_MS} ms"
            raise TimeoutError(msg)
