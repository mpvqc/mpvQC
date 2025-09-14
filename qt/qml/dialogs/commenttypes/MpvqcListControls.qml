// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick.Controls.Material
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

    signal upClicked
    signal downClicked
    signal editClicked
    signal deleteClicked

    Layout.alignment: Qt.AlignTop

    ToolButton {
        id: _upButton

        icon.width: 28
        icon.height: 28
        icon.source: "qrc:/data/icons/keyboard_arrow_up_black_24dp.svg"

        onPressed: {
            root.upClicked();
        }
    }

    ToolButton {
        id: _downButton

        icon.width: 28
        icon.height: 28
        icon.source: "qrc:/data/icons/keyboard_arrow_down_black_24dp.svg"

        onPressed: {
            root.downClicked();
        }
    }

    ToolButton {
        id: _editButton

        icon.width: 18
        icon.height: 18
        icon.source: "qrc:/data/icons/edit_black_24dp.svg"

        onPressed: {
            root.editClicked();
        }
    }

    ToolButton {
        id: _deleteButton

        icon.width: 24
        icon.height: 24
        icon.source: "qrc:/data/icons/delete_black_24dp.svg"

        onPressed: {
            root.deleteClicked();
        }
    }
}
