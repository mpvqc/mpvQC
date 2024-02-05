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
import QtQuick.Controls.Material.impl
import QtQuick.Layouts


Popup {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcCommentTable: root.mpvqcApplication.mpvqcCommentTable
    readonly property var mpvqcSpecialCharacterValidatorPyObject: root.mpvqcApplication.mpvqcSpecialCharacterValidatorPyObject

    readonly property int heightIncludingMargins: height + 2 * marginVertical

    readonly property int marginVertical: 10
    readonly property int xInRightToLeftLayout: mpvqcCommentTable.width - root.width - marginVertical
    readonly property int xInLeftToRightLayout: marginVertical

    height: _textField.height + topPadding + bottomPadding
    width: 450

    x: mirrored ? xInLeftToRightLayout : xInRightToLeftLayout
    y: marginVertical
    z: 1

    padding: 6
    closePolicy: Popup.CloseOnEscape
    transformOrigin: mirrored ? Popup.TopLeft : Popup.TopRight

    Material.roundedScale: Material.SmallScale

    signal nextOccurrenceRequested()
    signal previousOccurrenceRequested()

    function showSearchBox() {
        root.visible = true
        _textField.selectAll();
        _textField.forceActiveFocus()
    }

    function hideSearchBox() {
        root.visible = false
    }

    RowLayout {
        width: root.width - root.leftPadding - root.rightPadding
        spacing: 0

        TextField {
            id: _textField

            objectName: 'searchField'
            height: implicitHeight - 5
            focus: false
            selectByMouse: true
            horizontalAlignment: Text.AlignLeft
            validator: root.mpvqcSpecialCharacterValidatorPyObject

            Layout.fillWidth: true

            onTextChanged: {
                console.log("Query", text)
            }

            Component.onCompleted: {
                background.fillColor = 'transparent'
                background.outlineColor = 'transparent'
                background.focusedOutlineColor = 'transparent'
            }

            Keys.onPressed: (event) => {
                if (event.key === Qt.Key_F && event.modifiers === Qt.ControlModifier) {
                    if (event.isAutoRepeat) {
                        return
                    }
                    return root.showSearchBox()
                }
                event.accepted = false
            }
        }

        ToolButton {
            enabled: false
            focusPolicy: Qt.NoFocus
            text: "10/10"
        }

        ToolSeparator {
            padding: 0
        }

        ToolButton {
            focusPolicy: Qt.NoFocus
            icon.source: "qrc:/data/icons/keyboard_arrow_up_black_24dp.svg"
            icon.width: 24
            icon.height: 24

            onClicked: root.previousOccurrenceRequested()
        }

        ToolButton {
            focusPolicy: Qt.NoFocus
            icon.source: "qrc:/data/icons/keyboard_arrow_down_black_24dp.svg"
            icon.width: 24
            icon.height: 24

            onClicked: root.nextOccurrenceRequested()
        }

        ToolButton {
            focusPolicy: Qt.NoFocus
            icon.source: "qrc:/data/icons/close_black_24dp.svg"
            icon.width: 18
            icon.height: 18

            onClicked: root.hideSearchBox()
        }

    }

    Shortcut {
        sequence: "return"
        enabled: root.visible && _textField.activeFocus

        onActivated: root.nextOccurrenceRequested()
    }

    Shortcut {
        sequence: "shift+return"
        enabled: root.visible && _textField.activeFocus

        onActivated: root.previousOccurrenceRequested()
    }

    Connections {
        target: root.mpvqcApplication

        function onFullscreenChanged() {
            if (mpvqcApplication.fullscreen) {
                hideSearchBox()
            }
        }
    }

    Connections {
        target: root.mpvqcCommentTable

        function onHeightChanged() {
            const searchBoxHeight = root.height
            const tableHeight = root.parent.height
            const spaceToTop = root.y
            if (tableHeight < searchBoxHeight + spaceToTop * 2) {
                root.hideSearchBox()
            }
        }
    }


}
