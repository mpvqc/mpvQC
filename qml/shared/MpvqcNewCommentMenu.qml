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
import QtQuick.Controls


MpvqcMenu {
    id: root

    required property var mpvqcApplication
    property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    property var mpv: mpvqcApplication.mpvqcMpvPlayerPyObject
    property var mpvqcCommentTable: mpvqcApplication.mpvqcCommentTable
    property alias repeater: _repeater

    modal: true
    dim: false

    function popupMenu(): void {
        mpv.pause()
        mpvqcApplication.disableFullScreen()
        popup()
    }

    Repeater {
        id: _repeater

        model: mpvqcSettings.commentTypes

        MenuItem {
            text: qsTranslate("CommentTypes", model.type)

            onTriggered: {
                root.mpvqcCommentTable.addNewComment(model.type)
            }
        }
    }

}
