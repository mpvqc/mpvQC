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
import QtQuick.Controls.Material

Item {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcTheme: mpvqcApplication.mpvqcTheme

    readonly property bool isWindows: Qt.platform.os === "windows"
    readonly property url iconMaximize: "qrc:/data/icons/open_in_full_black_24dp.svg"
    readonly property url iconNormalize: "qrc:/data/icons/close_fullscreen_black_24dp.svg"

    readonly property alias minimizeButton: _minimizeButton
    readonly property alias maximizeButton: _maximizeButton
    readonly property alias closeButton: _closeButton

    ToolButton {
        id: _minimizeButton

        height: root.height
        focusPolicy: Qt.NoFocus
        anchors.right: _maximizeButton.left
        icon.width: 18
        icon.height: 18
        icon.source: "qrc:/data/icons/minimize_black_24dp.svg"

        onClicked: {
            root.mpvqcApplication.showMinimized();
        }
    }

    ToolButton {
        id: _maximizeButton

        height: root.height
        focusPolicy: Qt.NoFocus
        anchors.right: _closeButton.left
        icon.width: 18
        icon.height: 18
        icon.source: root.mpvqcApplication.maximized ? root.iconNormalize : root.iconMaximize

        onClicked: {
            root.mpvqcApplication.toggleMaximized();
        }
    }

    ToolButton {
        id: _closeButton

        height: root.height
        focusPolicy: Qt.NoFocus
        anchors.right: root.right

        icon {
            width: 18
            height: 18
            source: "qrc:/data/icons/close_black_24dp.svg"
            color: root.isWindows && _closeButton.hovered ? "#FFFFFD" : _closeButton.hovered ? root.mpvqcTheme.background : root.mpvqcTheme.foreground
        }

        onClicked: {
            root.mpvqcApplication.close();
        }

        Binding {
            when: true
            target: _closeButton.background
            property: "color"
            value: root.isWindows ? "#C42C1E" : root.mpvqcTheme.control
            restoreMode: Binding.RestoreNone
        }
    }
}
