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
import QtQuick.Layouts


Popup {
    id: root

    required property var searchFunc
    required property int tableHeight
    required property int tableWidth
    required property bool applicationIsFullscreen
    required property var mpvqcDefaultTextValidatorPyObject

    readonly property string searchQuery: searchQueryActive ? _textField.text : ''

    readonly property int customMarginVertical: 70
    readonly property int customMarginTop: 10

    readonly property var searchService: MpvqcSearchService {
        searchFunc: root.searchFunc

        onHighlightRequested: (index) => {
            root.highlightRequested(index)
        }
    }

    property bool searchQueryActive: false

    height: _textField.height + topPadding + bottomPadding
    width: 450

    x: mirrored ? customMarginVertical : root.tableWidth - width - customMarginVertical
    y: customMarginTop
    z: 1

    padding: 5
    closePolicy: Popup.NoAutoClose
    transformOrigin: mirrored ? Popup.TopLeft : Popup.TopRight

    Material.roundedScale: Material.SmallScale

    signal highlightRequested(int rowIndex)

    function showSearchBox() {
        root.visible = true
        root.searchQueryActive = true
        _textField.selectAll();
        _textField.forceActiveFocus()
    }

    function hideSearchBox() {
        root.visible = false
        root.searchQueryActive = false
    }

    function _hideSearchBoxWithoutAnimation() {
        const exitAnimation = root.exit
        root.exit = null
        hideSearchBox()
        root.exit = exitAnimation
    }

    onApplicationIsFullscreenChanged: {
        if (root.applicationIsFullscreen) {
            _hideSearchBoxWithoutAnimation()
        }
    }

    onClosed: {
        y = customMarginTop
    }

    RowLayout {
        width: root.width - root.leftPadding - root.rightPadding
        spacing: 0

        TextField {
            id: _textField

            focus: false
            selectByMouse: true
            horizontalAlignment: root.mirrored ? Text.AlignRight : Text.AlignLeft
            validator: root.mpvqcDefaultTextValidatorPyObject

            Layout.fillWidth: true

            onTextChanged: {
                root.searchService.search(text)
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
            id: _resultLabel

            readonly property int currentResult: root.searchService.currentResult
            readonly property int totalResults: root.searchService.totalResults
            readonly property bool haveResults: totalResults > 0
            readonly property bool displayText: currentResult >= 0 && totalResults >= 0

            text: displayText ? `${currentResult}/${totalResults}` : ''
            focusPolicy: Qt.NoFocus
            enabled: false
        }

        ToolSeparator {
            padding: 0
        }

        ToolButton {
            enabled: _resultLabel.haveResults
            icon.source: "qrc:/data/icons/keyboard_arrow_up_black_24dp.svg"
            icon.width: 24
            icon.height: 24

            onClicked: root.searchService.requestPrevious()
        }

        ToolButton {
            enabled: _resultLabel.haveResults
            icon.source: "qrc:/data/icons/keyboard_arrow_down_black_24dp.svg"
            icon.width: 24
            icon.height: 24

            onClicked: root.searchService.requestNext()
        }

        ToolButton {
            icon.source: "qrc:/data/icons/close_black_24dp.svg"
            icon.width: 18
            icon.height: 18

            onClicked: root.hideSearchBox()
        }

    }

    Shortcut {
        sequence: "return"
        enabled: root.visible && _textField.activeFocus

        onActivated: root.searchService.requestNext()
    }

    Shortcut {
        sequence: "shift+return"
        enabled: root.visible && _textField.activeFocus

        onActivated: root.searchService.requestPrevious()
    }

    Shortcut {
        sequence: "esc"
        enabled: _textField.activeFocus

        onActivated: root.hideSearchBox()
    }

    Shortcut {
        sequence: "up"
        enabled: _textField.activeFocus

        onActivated: root.searchService.requestPrevious()
    }

    Shortcut {
        sequence: "down"
        enabled: _textField.activeFocus

        onActivated: root.searchService.requestNext()
    }

}
