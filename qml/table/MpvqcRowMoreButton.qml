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


ToolButton {
    id: root

    required property bool tableInEditMode

    property var menu: null
    property var menuFactory: Component
    {

        MpvqcMenuMore {
            property int spaceToBorder: 10

            x: mirrored ? spaceToBorder : -(width - spaceToBorder * 3)
            y: spaceToBorder
            transformOrigin: mirrored ? Popup.TopLeft : Popup.TopRight

            onCopyCommentClicked: root.copyCommentClicked()

            onDeleteCommentClicked: root.deleteCommentClicked()

            onEditCommentClicked: {
                exit = null
                root.editCommentClicked()
            }
        }

    }

    signal copyCommentClicked()
    signal deleteCommentClicked()
    signal editCommentClicked()

    focusPolicy: Qt.NoFocus
    icon.source: "qrc:/data/icons/more_vert_black_24dp.svg"
    icon.width: 18
    icon.height: 18

    function _grabFocus(): void {
        focus = true
    }

    function openMenu(): void {
        menu = menuFactory.createObject(root)
        menu.closed.connect(menu.destroy)
        menu.open()
    }

    onClicked: {
        if (root.tableInEditMode) {
            root._grabFocus()
        } else {
            root.openMenu()
        }
    }

}
