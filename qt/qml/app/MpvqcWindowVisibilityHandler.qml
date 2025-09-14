// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

QtObject {
    id: root

    required property var mpvqcApplication

    readonly property bool maximized: mpvqcApplication.visibility === Window.Maximized
    readonly property bool fullscreen: mpvqcApplication.visibility === Window.FullScreen

    property bool wasMaximizedBefore: false

    function toggleMaximized(): void {
        if (maximized) {
            mpvqcApplication.showNormal();
        } else {
            mpvqcApplication.showMaximized();
        }
    }

    function toggleFullScreen(): void {
        if (fullscreen) {
            disableFullScreen();
        } else {
            enableFullScreen();
        }
    }

    function enableFullScreen(): void {
        if (!fullscreen) {
            wasMaximizedBefore = maximized;
            mpvqcApplication.showFullScreen();
        }
    }

    function disableFullScreen(): void {
        if (fullscreen && wasMaximizedBefore) {
            mpvqcApplication.showMaximized();
        } else if (fullscreen) {
            mpvqcApplication.showNormal();
        }
    }
}
