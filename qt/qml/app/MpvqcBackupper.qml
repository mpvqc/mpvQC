/*
 * Copyright (C) 2025 mpvQC developers
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

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
