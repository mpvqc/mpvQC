// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import pyobjects // qmllint disable unused-imports

WindowContainer {
    id: root

    window: MpvWindowPyObject {} // qmllint disable import

    // Workaround: on Windows, when the top-level transitions through
    // minimize → maximize, the embedded child HWND ends up offset by a few
    // pixels up-and-left from its correct position. Nudging the native
    // QWindow.width forces a SetWindowPos on the child and corrects it.
    Connections {
        target: root.Window.window

        function onVisibilityChanged(visibility: int): void {
            if (visibility !== Window.Minimized) {
                Qt.callLater(root._resyncChildGeometry);
            }
        }
    }

    function _resyncChildGeometry(): void {
        const w = root.width;
        if (w > 1) {
            root.window.width = w - 1;
            root.window.width = w;
        }
    }
}
