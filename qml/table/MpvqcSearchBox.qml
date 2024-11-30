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
import QtQuick.Layouts

Popup {
    id: root

    required property bool isApplicationFullScreen

    required property var searchQueryValidator
    required property var performModelSearchFunc

    readonly property string searchQuery: _impl.searchQueryActive ? _impl.currentSearchQuery : ""

    readonly property int topBottomMargin: 15
    readonly property int leftRightMargin: 30

    signal highlightRequested(rowIndex: int)

    x: mirrored ? root.leftRightMargin : parent.width - width - root.leftRightMargin
    y: parent.height - root.height - root.topBottomMargin
    z: 1

    height: _textField.height + topPadding + bottomPadding
    width: 450

    padding: 5
    closePolicy: Popup.NoAutoClose

    Material.roundedScale: Material.SmallScale

    onAboutToShow: {
        _impl.reactivateSearch();
    }

    onIsApplicationFullScreenChanged: {
        if (root.isApplicationFullScreen) {
            _impl.hideSearchBoxQuickly();
        }
    }

    QtObject {
        id: _impl

        property string currentSearchQuery: ""
        property bool searchQueryActive: false

        property int currentResult: -1
        property int totalResults: -1

        readonly property bool isDisplayText: currentResult >= 0 && totalResults >= 0
        readonly property bool isHaveResults: totalResults > 1
        readonly property string labelText: isDisplayText ? `${currentResult}/${totalResults}` : ""

        function reactivateSearch(): void {
            root.visible = true;
            searchQueryActive = true;
            _textField.selectAll();
            _textField.forceActiveFocus();
        }

        function hideSearchBox(): void {
            root.visible = false;
            searchQueryActive = false;
        }

        function hideSearchBoxQuickly(): void {
            const exitAnimation = root.exit;
            root.exit = null;
            hideSearchBox();
            root.exit = exitAnimation;
        }

        function search(query: string): void {
            currentSearchQuery = query;
            const includeCurrentRow = true;
            const topDown = true;
            _search(includeCurrentRow, topDown);
        }

        function _search(includeCurrentRow: bool, topDown: bool): void {
            const result = root.performModelSearchFunc(currentSearchQuery, includeCurrentRow, topDown); // qmllint disable
            const nextIndex = result.nextIndex;
            if (nextIndex >= 0) {
                root.highlightRequested(nextIndex);
            }
            currentResult = result.currentResult;
            totalResults = result.totalResults;
        }

        function requestNextSearchResult(): void {
            const includeCurrentRow = false;
            const topDown = true;
            _search(includeCurrentRow, topDown);
        }

        function requestPreviousSearchResult(): void {
            const includeCurrentRow = false;
            const topDown = false;
            _search(includeCurrentRow, topDown);
        }
    }

    RowLayout {
        width: root.width - root.leftPadding - root.rightPadding
        spacing: 0

        TextField {
            id: _textField

            validator: root.searchQueryValidator

            focus: false
            selectByMouse: true
            horizontalAlignment: Text.AlignLeft

            Layout.fillWidth: true

            onTextChanged: _impl.search(text)

            Component.onCompleted: {
                background.fillColor = "transparent";
                background.outlineColor = "transparent";
                background.focusedOutlineColor = "transparent";
            }
        }

        ToolButton {
            enabled: false
            text: _impl.labelText
            focusPolicy: Qt.NoFocus
        }

        ToolSeparator {
            padding: 0
        }

        ToolButton {
            enabled: _impl.isHaveResults
            focusPolicy: Qt.NoFocus

            icon {
                source: "qrc:/data/icons/keyboard_arrow_up_black_24dp.svg"
                width: 24
                height: 24
            }

            onPressed: _impl.requestPreviousSearchResult()
        }

        ToolButton {
            enabled: _impl.isHaveResults

            icon {
                source: "qrc:/data/icons/keyboard_arrow_down_black_24dp.svg"
                width: 24
                height: 24
            }

            onPressed: _impl.requestNextSearchResult()
        }

        ToolButton {
            icon {
                source: "qrc:/data/icons/close_black_24dp.svg"
                width: 18
                height: 18
            }

            onPressed: _impl.hideSearchBox()
        }
    }

    Shortcut {
        enabled: root.visible && _textField.activeFocus
        sequences: ["up", "shift+return"]

        onActivated: _impl.requestPreviousSearchResult()
    }

    Shortcut {
        enabled: root.visible && _textField.activeFocus
        sequences: ["down", "return"]

        onActivated: _impl.requestNextSearchResult()
    }

    Shortcut {
        enabled: root.visible
        sequence: "ctrl+f"
        autoRepeat: false

        onActivated: _impl.reactivateSearch()
    }

    Shortcut {
        enabled: root.visible
        sequence: "esc"
        autoRepeat: false

        onActivated: _impl.hideSearchBox()
    }

    DragHandler {
        id: _dragHandler

        readonly property NumberAnimation dragStartAnimation: NumberAnimation {
            target: root
            property: "scale"
            from: 1
            to: 1.0375
            duration: 75
        }

        readonly property NumberAnimation dragEndAnimation: NumberAnimation {
            target: root
            property: "scale"
            from: 1.0375
            to: 1
            duration: 75
        }

        readonly property int minimalY: root.topBottomMargin
        readonly property int maximalY: root.parent.height - root.height - root.topBottomMargin
        property int currentY: maximalY

        property int transistionStartedY: -1
        property bool stickToBottom: true

        function recalculateCurrentY(newPosition: int) {
            if (!_dragHandler.active && stickToBottom) {
                currentY = maximalY;
                return;
            }

            if (newPosition >= maximalY) {
                currentY = maximalY;
                stickToBottom = true;
                return;
            }

            if (newPosition >= minimalY) {
                currentY = newPosition;
                stickToBottom = newPosition >= maximalY - 15;
                return;
            }

            currentY = topBottomMargin;
            stickToBottom = false;
        }

        dragThreshold: 0
        target: null

        xAxis.enabled: false
        yAxis.enabled: true

        onActiveChanged: {
            transistionStartedY = _dragHandler.active ? root.y : -1;
        }

        onMaximalYChanged: {
            if (maximalY <= 0)
                return;
            _dragHandler.recalculateCurrentY(currentY);
        }

        yAxis.onActiveValueChanged: {
            const possiblePosition = transistionStartedY + yAxis.activeValue;
            _dragHandler.recalculateCurrentY(possiblePosition);
        }

        onGrabChanged: transition => {
            switch (transition) {
            case PointerDevice.GrabExclusive:
                dragStartAnimation.start();
                break;
            case PointerDevice.UngrabExclusive:
                dragEndAnimation.start();
                break;
            }
        }
    }

    Binding {
        when: root.visible
        target: root
        property: "y"
        value: _dragHandler.currentY
    }
}
