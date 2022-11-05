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
    id: control
    text: qsTranslate("CommentTypes", commentType)
    horizontalAlignment: Text.AlignLeft
    verticalAlignment: Text.AlignVCenter
    elide: LayoutMirroring.enabled ? Text.ElideLeft: Text.ElideRight

    property string commentType

    signal clicked()
    signal edited(string commentType)
    signal editingStarted()
    signal editingStopped()

    MouseArea {
        anchors.fill: parent

        onClicked: control.clicked()
    }

    function startEditing() {
        triggerEditingStarted()
        openCommentTypeEditMenu()
    }

    function openCommentTypeEditMenu() {
        const component = Qt.createComponent("MpvqcEditCommentTypeMenu.qml")
        const menu = component.createObject(control)
        menu.currentCommentType = control.commentType
        menu.closed.connect(control.triggerEditingStopped)
        menu.closed.connect(menu.destroy)
        menu.itemClicked.connect(control.triggerEdited)
        if (LayoutMirroring.enabled) {
            // fixme? workaround popup opening to the right
            menu.x = -(control.width / 2)
        }
        menu.open()
    }

    function grabFocus() {
        control.focus = true
    }

    function triggerClicked() {
        control.clicked()
    }

    function triggerEdited(commentType) {
        control.edited(commentType)
    }

    function triggerEditingStarted() {
        control.editingStarted()
    }

    function triggerEditingStopped() {
        control.editingStopped()
    }

}
