// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import pyobjects

import "../shared"

Popup {
    id: root

    required property MpvqcSearchBoxController controller

    readonly property bool isApplicationFullScreen: MpvqcWindowProperties.isFullscreen
    readonly property string searchQuery: _impl.searchActive ? controller.searchQuery : ""

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

        property bool searchActive: false

        readonly property int currentResult: root.controller.currentResult
        readonly property int totalResults: root.controller.totalResults

        readonly property string labelText: currentResult >= 0 && totalResults >= 0 ? `${currentResult}/${totalResults}` : ""

        function reactivateSearch(): void {
            root.visible = true;
            searchActive = true;
            _textField.selectAll();
            _textField.forceActiveFocus();
        }

        function hideSearchBox(): void {
            root.visible = false;
            searchActive = false;
        }

        function hideSearchBoxQuickly(): void {
            const exitAnimation = root.exit;
            root.exit = null;
            hideSearchBox();
            root.exit = exitAnimation;
        }
    }

    RowLayout {
        width: root.width - root.leftPadding - root.rightPadding
        spacing: 0

        TextField {
            id: _textField

            readonly property var reForbidden: new RegExp('[\u00AD\r\n]', 'gi')

            focus: false
            selectByMouse: true
            horizontalAlignment: Text.AlignLeft

            Layout.fillWidth: true

            onTextChanged: {
                const sanitized = sanitizeText(text);
                if (sanitized !== text) {
                    text = sanitized;
                    return;
                } else {
                    root.controller.search(text);
                }
            }

            function sanitizeText(text: string): string {
                if (text.search(reForbidden) === -1) {
                    return text;
                }
                return text.replace(reForbidden, "");
            }

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
            enabled: _impl.totalResults >= 2
            focusPolicy: Qt.NoFocus

            icon {
                source: "qrc:/data/icons/keyboard_arrow_up_black_24dp.svg"
                width: 24
                height: 24
            }

            onPressed: root.controller.selectPrevious()
        }

        ToolButton {
            enabled: _impl.totalResults >= 2

            icon {
                source: "qrc:/data/icons/keyboard_arrow_down_black_24dp.svg"
                width: 24
                height: 24
            }

            onPressed: root.controller.selectNext()
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

        onActivated: root.controller.selectPrevious()
    }

    Shortcut {
        enabled: root.visible && _textField.activeFocus
        sequences: ["down", "return"]

        onActivated: root.controller.selectNext()
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

        function recalculateCurrentY(newPosition: int): void {
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

            currentY = root.topBottomMargin;
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
