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

import "MpvqcDocumentFileExporter.js" as MpvqcDocumentFileExporter


QtObject {
    id: root

    required property url video
    required property var mpvqcApplication

    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    readonly property var mpvqcFileSystemHelperPyObject: mpvqcApplication.mpvqcFileSystemHelperPyObject
    readonly property var mpvqcTimeFormatUtils: mpvqcApplication.mpvqcTimeFormatUtils
    readonly property var mpvqcCommentTable: mpvqcApplication.mpvqcCommentTable
    property var mpvqcBackupPyObject: mpvqcApplication.mpvqcBackupPyObject

    readonly property var absPathGetterFunc:mpvqcFileSystemHelperPyObject.url_to_absolute_path
    readonly property var nicknameGetterFunc: function() { return root.mpvqcSettings.nickname }
    readonly property var commentGetterFunc: mpvqcCommentTable.getAllComments
    readonly property var settingsGetterFunc: function() { return root.mpvqcSettings }
    readonly property var timeFormatFunc: mpvqcTimeFormatUtils.formatTimeToStringLong

    property var generator: new MpvqcDocumentFileExporter.ExportContentGenerator(
        absPathGetterFunc, nicknameGetterFunc, commentGetterFunc, settingsGetterFunc, timeFormatFunc
    )

    property var timer: Timer {
        interval: Math.max(15, root.mpvqcSettings.backupInterval) * 1000
        running: root.mpvqcSettings.backupEnabled
        repeat: true

        onTriggered: {
            backup()
        }
    }

    function backup(): void {
        const videoName = getVideoName()
        const content = generator.createBackupContent(root.video)
        mpvqcBackupPyObject.write_backup(videoName, content)
    }

    function getVideoName(): string {
        if (video && video != '') {
            return mpvqcFileSystemHelperPyObject.url_to_filename_without_suffix(video)
        } else {
            return qsTranslate("FileInteractionDialogs", "untitled")
        }
    }

}
