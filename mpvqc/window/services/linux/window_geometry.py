# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Wayland-only: declare the window geometry inside the surface, so the
compositor aligns and snaps against what the user sees rather than against the
drop shadow margin. QWaylandWindow::setCustomMargins takes the inset. It is
private Qt API, reached through ctypes.

DELETE WHEN: PySide6 exposes a public window-geometry inset (a real QWindow
API) or ships the QtWaylandClient module. Then replace the body of
apply_wayland_content_margins with the public call and drop the ctypes code.

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
from typing import TYPE_CHECKING

import PySide6
import shiboken6

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtGui import QWindow

logger = logging.getLogger(__name__)

# QWindow::handle() const -> QPlatformWindow*
_HANDLE_SYMBOL = "_ZNK7QWindow6handleEv"
# QtWaylandClient::QWaylandWindow::setCustomMargins(QMargins const&)
_SET_CUSTOM_MARGINS_SYMBOL = "_ZN15QtWaylandClient14QWaylandWindow16setCustomMarginsERK8QMargins"
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


def _qt_lib(name: str) -> str:
    lib_dir = Path(PySide6.__file__).parent / "Qt" / "lib"
    matches = sorted(lib_dir.glob(f"lib{name}.so*"))
    if not matches:
        msg = f"could not find lib{name} under {lib_dir}"
        raise OSError(msg)
    return str(matches[0])


@lru_cache(maxsize=1)
def _resolve_symbols() -> tuple[Callable[..., int | None], Callable[..., None]] | None:
    # Cached so a missing symbol warns once, not on every margin or visibility change.
    try:
        gui = ctypes.CDLL(_qt_lib("Qt6Gui"))
        wayland = ctypes.CDLL(_qt_lib("Qt6WaylandClient"))
        handle = gui[_HANDLE_SYMBOL]
        set_custom_margins = wayland[_SET_CUSTOM_MARGINS_SYMBOL]
    except (OSError, AttributeError):
        logger.warning("Wayland window-geometry symbols unavailable; content margins not applied")
        return None

    handle.argtypes = [c_void_p]
    handle.restype = c_void_p
    set_custom_margins.argtypes = [c_void_p, c_void_p]
    set_custom_margins.restype = None
    return handle, set_custom_margins


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
    handle, set_custom_margins = symbols

    qwindow_ptr = shiboken6.Shiboken.getCppPointer(window)[0]
    platform_ptr = handle(c_void_p(qwindow_ptr))
    if not platform_ptr:
        # Platform window not created yet, nothing to inset.
        return

    wayland_window_ptr = platform_ptr - _QOBJECT_BASE_OFFSET
    native = native_margin(margin, high_dpi_factor(window))
    margins = _QMargins(native, native, native, native)
    set_custom_margins(c_void_p(wayland_window_ptr), byref(margins))
