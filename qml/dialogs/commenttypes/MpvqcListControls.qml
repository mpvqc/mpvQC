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
import QtQuick.Layouts


ColumnLayout {
    id: root

    readonly property alias upButton: _upButton
    readonly property alias downButton: _downButton
    readonly property alias editButton: _editButton
    readonly property alias deleteButton: _deleteButton
    readonly property alias buttonHeight: _deleteButton.height

    property alias upEnabled: _upButton.enabled
    property alias downEnabled: _downButton.enabled
    property alias editEnabled: _editButton.enabled
    property alias deleteEnabled: _deleteButton.enabled

    signal upClicked()
    signal downClicked()
    signal editClicked()
    signal deleteClicked()

    Layout.alignment: Qt.AlignTop

    ToolButton {
        id: _upButton

        icon.width: 28
        icon.height: 28
        icon.source: "qrc:/data/icons/keyboard_arrow_up_black_24dp.svg"

        onClicked: {
            root.upClicked()
        }
    }

    ToolButton {
        id: _downButton

        icon.width: 28
        icon.height: 28
        icon.source: "qrc:/data/icons/keyboard_arrow_down_black_24dp.svg"

        onClicked: {
            root.downClicked()
        }
    }

    ToolButton {
        id: _editButton

        icon.width: 18
        icon.height: 18
        icon.source: "qrc:/data/icons/edit_black_24dp.svg"

        onClicked: {
            root.editClicked()
        }

    }

    ToolButton {
        id: _deleteButton

        icon.width: 24
        icon.height: 24
        icon.source: "qrc:/data/icons/delete_black_24dp.svg"

        onClicked: {
            root.deleteClicked()
        }
    }

}
