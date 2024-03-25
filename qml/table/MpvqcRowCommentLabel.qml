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

import "MpvqcCommentHighlighter.js" as CommentHighlighter


Label {
    id: root

    required property var mpvqcApplication
    required property string comment
    required property string searchQuery
    required property bool rowSelected
    required property bool tableInEditMode
    required property var backgroundColor

    property alias loader: _loader

    readonly property var mpvqcDefaultTextValidatorPyObject: mpvqcApplication.mpvqcDefaultTextValidatorPyObject
    readonly property Timer delayEditingStoppedTimer: Timer { interval: 150; onTriggered: root.editingStopped() }

    signal clicked()
    signal edited(string newComment)
    signal editingStarted()
    signal editingStopped()
    signal upPressed()
    signal downPressed()

    textFormat: searchQuery ? Text.RichText : Text.PlainText
    text: searchQuery ? CommentHighlighter.highlightComment(comment, searchQuery) : comment
    wrapMode: Text.WordWrap
    height: _loader.item ? _loader.item.contentItem.height + topPadding : implicitHeight
    horizontalAlignment: Text.AlignLeft

    function _grabFocus(): void {
        focus = true
    }

    function startEditing(): void {
        editingStarted()
        openPopup()
    }

    function openPopup(): void {
        _loader.sourceComponent = _editComponent
    }

    function _stopEditing(): void {
        _closePopup()
        delayEditingStoppedTimer.restart()
    }

    function _closePopup(): void {
        _loader.sourceComponent = undefined
    }

    MouseArea {
        anchors.fill: parent

        onClicked: {
            if (root.rowSelected && root.tableInEditMode) {
                root._grabFocus()
            } else if (root.rowSelected) {
                root.startEditing()
            } else {
                root.clicked()
            }
        }
    }

    Loader { id: _loader; asynchronous: true }

    Component {
        id: _editComponent

        MpvqcRowCommentLabelEditPopup {
            implicitWidth: root.width
            currentComment: root.comment
            backgroundColor: root.backgroundColor
            mpvqcDefaultTextValidator: root.mpvqcDefaultTextValidatorPyObject
            leftPadding: root.leftPadding / 2
            rightPadding: root.rightPadding / 2
            topPadding: root.topPadding / 2
            bottomPadding: root.bottomPadding / 2

            onClosed: root._stopEditing()

            onEdited: (newComment) => root.edited(newComment)

            onUpPressed: root.upPressed()

            onDownPressed: root.downPressed()
        }
    }

}
