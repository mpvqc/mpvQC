// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma Singleton

import QtQuick

QtObject {

    readonly property bool anyModalOverlayOpen: _openCount > 0

    // A count, not a flag: overlays overlap, e.g. a message box opens while a
    // file dialog tears down.
    property int _openCount: 0

    function retain(): void {
        _openCount += 1;
    }

    function release(): void {
        _openCount -= 1;
    }
}
