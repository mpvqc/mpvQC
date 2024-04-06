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

    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    readonly property var mpvqcCommentTable: mpvqcApplication.mpvqcCommentTable
    readonly property var mpvqcMpvPlayerPyObject: mpvqcApplication.mpvqcMpvPlayerPyObject
    readonly property var mpvqcUtilityPyObject: mpvqcApplication.mpvqcUtilityPyObject
    property string selectedCommentType: ''

    property alias repeater: _repeater

    modal: true
    dim: false
    parent: Overlay.overlay
    z: 2
    exit: null

	onAboutToShow: _positionMenu()
    onClosed: _addComment()

    function _positionMenu(): void {
        const pos = parent.mapFromGlobal(mpvqcUtilityPyObject.cursorPosition)
		x = root.mMirrored ? pos.x - root.width : pos.x
		y = pos.y
    }

    function popupMenu(): void {
        mpvqcMpvPlayerPyObject.pause()
        popup()
    }

    function _addComment(): void {
        // Instead of directly adding a comment in the MenuItem triggered signal handler,
        // we defer adding it until the popup closes. If we would directly add it,
        // the menu's closing signals would interfere with the focus of the newly added comment.
        if (selectedCommentType !== '') {
            mpvqcCommentTable.addNewComment(selectedCommentType)
            selectedCommentType = ''
        }
    }

    Repeater {
        id: _repeater

        model: root.mpvqcSettings.commentTypes

        MenuItem {
            required property string modelData

            text: qsTranslate("CommentTypes", modelData)

            onTriggered: {
                mpvqcApplication.disableFullScreen()
                root.selectedCommentType = modelData
            }
        }
    }

}
