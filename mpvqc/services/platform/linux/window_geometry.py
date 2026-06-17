# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Wayland-only hack: tell the compositor the window's real rectangle.

A frameless window with a transparent shadow margin hands the compositor the
whole padded surface, so the content cannot sit flush at screen edges and
drag-snap/maximize fire off the padded rectangle. QWaylandWindow::setCustomMargins
declares the real geometry inset. It is private Qt API reached through ctypes.

DELETE WHEN: PySide6 exposes a public window-geometry inset (a real QWindow API)
or ships the QtWaylandClient module. Then replace the body of
apply_wayland_content_margins with the public call and drop the ctypes plumbing.

The mangled symbol names below are regenerated from the bundled Qt by our dependency
updater script run by `just update-python-dependencies`) do not hand-edit them.
The QObject base offset is sizeof(QObject) on 64-bit.
"""

from __future__ import annotations

import ctypes
import logging
from ctypes import Structure, byref, c_int, c_void_p
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

# QWaylandWindow inherits QObject then QPlatformWindow. handle() returns the
# QPlatformWindow subobject, which sits one QObject (16 bytes on 64-bit) past the
# QWaylandWindow* the method needs. A C++ static_cast does this; we subtract it.
_QOBJECT_BASE_OFFSET = 16


class _QMargins(Structure):
    _fields_ = (("left", c_int), ("top", c_int), ("right", c_int), ("bottom", c_int))


def _qt_lib(name: str) -> str:
    lib_dir = Path(PySide6.__file__).parent / "Qt" / "lib"
    matches = sorted(lib_dir.glob(f"lib{name}.so*"))
    if not matches:
        msg = f"could not find lib{name} under {lib_dir}"
        raise OSError(msg)
    return str(matches[0])


@lru_cache(maxsize=1)
def _resolve_symbols() -> tuple[Callable[..., int | None], Callable[..., None]] | None:
    # Cached so resolution (and a missing-symbol failure) happens once: the
    # warning logs a single time, not on every margin or visibility change.
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


def apply_wayland_content_margins(window: QWindow, margin: int) -> None:
    symbols = _resolve_symbols()
    if symbols is None:
        return
    handle, set_custom_margins = symbols

    qwindow_ptr = shiboken6.Shiboken.getCppPointer(window)[0]
    platform_ptr = handle(c_void_p(qwindow_ptr))
    if not platform_ptr:
        # Platform window not created yet; nothing to inset.
        return

    wayland_window_ptr = platform_ptr - _QOBJECT_BASE_OFFSET
    margins = _QMargins(margin, margin, margin, margin)
    set_custom_margins(c_void_p(wayland_window_ptr), byref(margins))
