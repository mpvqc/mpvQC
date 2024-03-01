/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

import QtQuick


Timer {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    readonly property var mpvqcCommentTable: mpvqcApplication.mpvqcCommentTable
    readonly property var mpvqcDocumentExporterPyObject: mpvqcApplication.mpvqcDocumentExporterPyObject
    readonly property var mpvqcMpvPlayerPropertiesPyObject: mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject

    repeat: true
    interval: Math.max(15, root.mpvqcSettings.backupInterval) * 1000
    running: root.mpvqcSettings.backupEnabled && mpvqcCommentTable.count > 0

    onTriggered: {
        mpvqcDocumentExporterPyObject.backup()
    }

}
