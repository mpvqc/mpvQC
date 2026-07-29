// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import io.github.mpvqc.mpvQC.Utility

QtObject {
    id: root

    required property bool open

    property bool _counted: false

    function _sync(): void {
        if (root.open === root._counted) {
            return;
        }
        root._counted = root.open;
        if (root.open) {
            MpvqcModalState.retain();
        } else {
            MpvqcModalState.release();
        }
    }

    onOpenChanged: root._sync()

    Component.onCompleted: root._sync()

    Component.onDestruction: {
        if (root._counted) {
            root._counted = false;
            MpvqcModalState.release();
        }
    }
}
