// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

Timer {

    required property var backend
    required property bool isHaveComments
    required property bool isBackupEnabled
    required property int backupInterval

    repeat: true
    interval: Math.max(15, backupInterval) * 1000
    running: isBackupEnabled && isHaveComments

    onTriggered: {
        backend.backup();
    }
}
