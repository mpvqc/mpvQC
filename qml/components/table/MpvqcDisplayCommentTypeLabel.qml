/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick
import QtQuick.Controls
import pyobjects


Label {
    id: control
    text: qsTranslate("CommentTypes", commentType)
    horizontalAlignment: Text.AlignLeft
    verticalAlignment: Text.AlignVCenter
    elide: LayoutMirroring.enabled ? Text.ElideLeft: Text.ElideRight

    property string commentType
    property bool itemSelected

    signal clicked()
    signal edited(string commentType)

    MouseArea {
        anchors.fill: parent

        onClicked: {
            if (itemSelected) {
                openCommentTypeEditMenu()
            } else {
                triggerClicked()
            }
        }
    }

    function openCommentTypeEditMenu() {
        const component = Qt.createComponent("MpvqcEditCommentTypeMenu.qml")
        const menu = component.createObject(control)
        menu.currentCommentType = control.commentType
        menu.closed.connect(menu.destroy)
        menu.itemClicked.connect((commentType) => triggerEdited(commentType))
        if (LayoutMirroring.enabled) {
            // fixme? workaround popup opening to the right
            menu.x = -(control.width / 2)
        }
        menu.open()
    }

    function triggerClicked() {
        control.clicked()
    }

    function triggerEdited(commentType) {
        control.edited(commentType)
    }

}
