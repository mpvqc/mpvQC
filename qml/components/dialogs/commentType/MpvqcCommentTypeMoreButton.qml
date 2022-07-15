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


import QtQuick.Controls
import components.shared


ToolButton {
    id: otherButton

    signal deletePressed()
    signal editPressed()

    icon {
        width: 20
        height: 20
        source: "qrc:/data/icons/more_vert_black_24dp.svg"
    }

    onClicked: {
        menu.open()
    }

    MpvqcAutoWidthMenu {
        id: menu

        Action {
            text: qsTranslate("CommentTypeSettings", "Edit")
            icon.source: "qrc:/data/icons/edit_black_24dp.svg"

            onTriggered: {
                editPressed()
            }
        }

        Action {
            text: qsTranslate("CommentTypeSettings", "Delete")
            icon.source: "qrc:/data/icons/delete_black_24dp.svg"

            onTriggered: {
                deletePressed()
            }
        }
    }

}
