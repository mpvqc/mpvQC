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


Label {
    id: root

    required property var mpvqcApplication
    required property string commentType
    required property bool rowSelected
    required property bool tableInEditMode

    property var menu: undefined
    property var menuFactory: Component
    {
        MpvqcRowCommentTypeLabelEditMenu {
            readonly property int additionalSpace: 7

            y: additionalSpace
            x: mirrored ? - (width - root.width + additionalSpace) : additionalSpace

            currentCommentType: root.commentType
            mpvqcApplication: root.mpvqcApplication

            onClosed: root.editingStopped()

            onItemClicked: (newCommentType) => root.edited(newCommentType)
        }
    }

    signal edited(string newCommentType)
    signal editingStarted()
    signal editingStopped()

    text: qsTranslate("CommentTypes", commentType)
    horizontalAlignment: Text.AlignLeft

    function _grabFocus(): void {
        focus = true
    }

    function _startEditing(): void {
        editingStarted()
        openMenu()
    }

    function openMenu(): void {
        menu = menuFactory.createObject(root)
        menu.closed.connect(menu.destroy)
        menu.open()
    }

    MouseArea {
        anchors.fill: parent
        enabled: root.rowSelected

        onClicked: {
            if (root.tableInEditMode) {
                root._grabFocus()
            } else {
                root._startEditing()
            }
        }
    }

}
