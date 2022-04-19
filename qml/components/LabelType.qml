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

    id: label

    property string type
    property bool rowSelected

    signal clicked()
    signal edited(string type)

    text: qsTranslate("CommentTypes", type)
    horizontalAlignment: Text.AlignLeft
    verticalAlignment: Text.AlignVCenter
    elide: TranslationPyObject.rtl_enabled ? Text.ElideLeft: Text.ElideRight

    MouseArea {
        anchors.fill: parent

        onClicked: {
            if (rowSelected) {
                openCommentTypeEditMenu()
            } else {
                triggerClicked()
            }
        }
    }

    function openCommentTypeEditMenu() {
        const component = Qt.createComponent("MenuEditCommentType.qml")
        const menu = component.createObject(appWindow)
        menu.currentCommentType = label.type
        menu.closed.connect(() => menu.destroy())
        menu.itemClicked.connect((commentType) => {
            triggerEdited(commentType)
        })
        menu.popup()
    }

    function triggerClicked() {
        label.clicked()
    }

    function triggerEdited(commentType) {
        label.edited(commentType)
    }

}
