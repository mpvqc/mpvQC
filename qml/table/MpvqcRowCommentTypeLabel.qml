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

    property alias loader: _loader

    signal clicked()
    signal edited(string newCommentType)
    signal editingStarted()
    signal editingStopped()

    text: qsTranslate("CommentTypes", commentType)
    horizontalAlignment: Text.AlignLeft
    verticalAlignment: Text.AlignVCenter

    function _grabFocus(): void {
        focus = true
    }

    function _startEditing(): void {
        editingStarted()
        openMenu()
    }

    function openMenu(): void {
        _loader.sourceComponent = _editComponent
    }

    function _stopEditing(): void {
        _closeMenu()
        editingStopped()
    }

    function _closeMenu(): void {
        _loader.sourceComponent = undefined
    }

    MouseArea {
        anchors.fill: parent

        onClicked: {
            if (root.rowSelected && root.tableInEditMode) {
                root._grabFocus()
            } else if (root.rowSelected) {
                root._startEditing()
            } else {
                root.clicked()
            }
        }
    }

    Loader { id: _loader; asynchronous: true }

    Component {
        id: _editComponent

        MpvqcRowCommentTypeLabelEditMenu {
            y: (-1/2) * (height - root.height)
            x: mirrored ? - (width - root.width) : 0
            currentCommentType: root.commentType
            mpvqcApplication: root.mpvqcApplication

            onClosed: root._stopEditing()

            onItemClicked: (newCommentType) => root.edited(newCommentType)

        }
    }

}
