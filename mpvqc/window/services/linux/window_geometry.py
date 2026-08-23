# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Wayland-only: declare the window geometry inside the surface, so the
compositor aligns and snaps against what the user sees rather than against the
drop shadow margin. QWaylandWindow::setCustomMargins takes the inset and
QWaylandWindow::windowStates answers the states the compositor has applied
(QWindow::windowStates lags behind it by one queued event). Both are private
Qt API, reached through ctypes.

DELETE WHEN: PySide6 exposes a public window-geometry inset (a real QWindow
API) or ships the QtWaylandClient module. Then replace the bodies of
apply_wayland_content_margins and wayland_window_states with the public calls
and drop the ctypes code.

The mangled symbol names below are regenerated from the bundled Qt by the
dependency updater script (`just update-python-dependencies`); do not edit
them by hand. _QOBJECT_BASE_OFFSET is sizeof(QObject), two pointers, so it is
correct on both 32- and 64-bit builds.
"""

from __future__ import annotations

import ctypes
import logging
from ctypes import Structure, byref, c_double, c_int, c_void_p
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, NamedTuple

import PySide6
import shiboken6
from PySide6.QtCore import Qt

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtGui import QWindow

logger = logging.getLogger(__name__)

# QWindow::handle() const -> QPlatformWindow*
_HANDLE_SYMBOL = "_ZNK7QWindow6handleEv"
# QtWaylandClient::QWaylandWindow::setCustomMargins(QMargins const&)
_SET_CUSTOM_MARGINS_SYMBOL = "_ZN15QtWaylandClient14QWaylandWindow16setCustomMarginsERK8QMargins"
# QtWaylandClient::QWaylandWindow::windowStates() const
_WINDOW_STATES_SYMBOL = "_ZNK15QtWaylandClient14QWaylandWindow12windowStatesEv"
# QHighDpiScaling::scaleAndOrigin(QWindow const*, QHighDpiScaling::Point)
_SCALE_AND_ORIGIN_SYMBOL = "_ZN15QHighDpiScaling14scaleAndOriginEPK7QWindowNS_5PointE"

_QOBJECT_BASE_OFFSET = 2 * ctypes.sizeof(c_void_p)


class _QMargins(Structure):
    _fields_ = (("left", c_int), ("top", c_int), ("right", c_int), ("bottom", c_int))


class _QHighDpiPoint(Structure):
    # QHighDpiScaling::Point; kind 0 is Invalid, which resolves against the window's screen.
    _fields_ = (("kind", c_int), ("x", c_int), ("y", c_int))


class _QScaleAndOrigin(Structure):
    _fields_ = (("factor", c_double), ("origin_x", c_int), ("origin_y", c_int))


class _WaylandSymbols(NamedTuple):
    handle: Callable[..., int | None]
    set_custom_margins: Callable[..., None]
    window_states: Callable[..., int]


def _qt_lib(name: str) -> str:
    lib_dir = Path(PySide6.__file__).parent / "Qt" / "lib"
    matches = sorted(lib_dir.glob(f"lib{name}.so*"))
    if not matches:
        msg = f"could not find lib{name} under {lib_dir}"
        raise OSError(msg)
    return str(matches[0])


@lru_cache(maxsize=1)
def _resolve_symbols() -> _WaylandSymbols | None:
    # Cached so a missing symbol warns once, not on every margin or visibility change.
    try:
        gui = ctypes.CDLL(_qt_lib("Qt6Gui"))
        wayland = ctypes.CDLL(_qt_lib("Qt6WaylandClient"))
        handle = gui[_HANDLE_SYMBOL]
        set_custom_margins = wayland[_SET_CUSTOM_MARGINS_SYMBOL]
        window_states = wayland[_WINDOW_STATES_SYMBOL]
    except (OSError, AttributeError):
        logger.warning(
            "Wayland window-geometry symbols unavailable; content margins not applied, window states read from QWindow"
        )
        return None

    handle.argtypes = [c_void_p]
    handle.restype = c_void_p
    set_custom_margins.argtypes = [c_void_p, c_void_p]
    set_custom_margins.restype = None
    # Qt::WindowStates is a QFlags<int>, which the ABI returns like a plain int.
    window_states.argtypes = [c_void_p]
    window_states.restype = c_int
    return _WaylandSymbols(handle=handle, set_custom_margins=set_custom_margins, window_states=window_states)


@lru_cache(maxsize=1)
def _resolve_scale_and_origin() -> Callable[..., _QScaleAndOrigin] | None:
    try:
        gui = ctypes.CDLL(_qt_lib("Qt6Gui"))
        scale_and_origin = gui[_SCALE_AND_ORIGIN_SYMBOL]
    except (OSError, AttributeError):
        logger.warning("High-DPI factor symbol unavailable; content margins assume factor 1")
        return None

    scale_and_origin.argtypes = [c_void_p, _QHighDpiPoint]
    scale_and_origin.restype = _QScaleAndOrigin
    return scale_and_origin


def _wayland_window_ptr(window: QWindow, handle: Callable[..., int | None]) -> int | None:
    qwindow_ptr = shiboken6.Shiboken.getCppPointer(window)[0]
    platform_ptr = handle(c_void_p(qwindow_ptr))
    if not platform_ptr:
        # Platform window not created yet.
        return None
    return platform_ptr - _QOBJECT_BASE_OFFSET


def high_dpi_factor(window: QWindow) -> float:
    # Not devicePixelRatio: compositor scaling sits below Qt and is already
    # native. This is only the layer the env scale factors insert.
    scale_and_origin = _resolve_scale_and_origin()
    if scale_and_origin is None:
        return 1.0

    qwindow_ptr = shiboken6.Shiboken.getCppPointer(window)[0]
    return scale_and_origin(c_void_p(qwindow_ptr), _QHighDpiPoint(0, 0, 0)).factor


def native_margin(margin: int, factor: float) -> int:
    return int(margin * factor + 0.5)


def apply_wayland_content_margins(window: QWindow, margin: int) -> None:
    symbols = _resolve_symbols()
    if symbols is None:
        return

    wayland_window_ptr = _wayland_window_ptr(window, symbols.handle)
    if wayland_window_ptr is None:
        return

    native = native_margin(margin, high_dpi_factor(window))
    margins = _QMargins(native, native, native, native)
    symbols.set_custom_margins(c_void_p(wayland_window_ptr), byref(margins))


def wayland_window_states(window: QWindow) -> Qt.WindowState | None:
    """The states the compositor has applied; None without a platform window
    or the symbol to ask."""
    symbols = _resolve_symbols()
    if symbols is None:
        return None

    wayland_window_ptr = _wayland_window_ptr(window, symbols.handle)
    if wayland_window_ptr is None:
        return None

    states = symbols.window_states(c_void_p(wayland_window_ptr))
    # The platform tracks activation in the same flags; QWindow::windowStates never reports it.
    return Qt.WindowState(states) & ~Qt.WindowState.WindowActive
