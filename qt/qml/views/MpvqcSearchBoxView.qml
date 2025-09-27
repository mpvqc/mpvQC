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
    property bool searchActive: false
    readonly property bool isApplicationFullScreen: MpvqcWindowProperties.isFullscreen
    readonly property string searchQuery: searchActive ? controller.searchQuery : ""

    function closeWithoutAnimation(): void {
        const exitAnimation = exit;
        exit = null;
        root.close();
        exit = exitAnimation;
    }

    x: mirrored ? 30 : parent.width - width - 30
    y: parent.height - height - 15
    z: 1

    width: 450
    height: _textField.height + topPadding + bottomPadding
    padding: 5

    closePolicy: Popup.NoAutoClose
    Material.roundedScale: Material.SmallScale

    onAboutToShow: {
        root.searchActive = true;
        _textField.selectAll();
        _textField.forceActiveFocus();
    }

    onAboutToHide: {
        root.searchActive = false;
    }

    onIsApplicationFullScreenChanged: {
        if (isApplicationFullScreen) {
            root.closeWithoutAnimation();
        }
    }

    QtObject {
        id: _searchInfo

        readonly property int currentResult: root.controller.currentResult
        readonly property int totalResults: root.controller.totalResults
        readonly property bool hasMultipleResults: totalResults >= 2
        readonly property string statusLabel: {
            if (currentResult >= 0 && totalResults >= 0) {
                return `${currentResult}/${totalResults}`;
            }
            return "";
        }
    }

    RowLayout {
        width: root.width - root.leftPadding - root.rightPadding
        spacing: 0

        TextField {
            id: _textField

            readonly property var forbiddenChars: /[\u00AD\r\n]/g

            function sanitizeInput(input: string): string {
                return input.replace(forbiddenChars, "");
            }

            Layout.fillWidth: true
            focus: false
            selectByMouse: true
            horizontalAlignment: Text.AlignLeft

            onTextChanged: {
                const sanitized = sanitizeInput(text);
                if (sanitized !== text) {
                    text = sanitized;
                } else {
                    root.controller.search(text);
                }
            }

            Component.onCompleted: {
                background.fillColor = "transparent";
                background.outlineColor = "transparent";
                background.focusedOutlineColor = "transparent";
            }
        }

        ToolButton {
            enabled: false
            text: _searchInfo.statusLabel
            focusPolicy: Qt.NoFocus
        }

        ToolSeparator {
            padding: 0
        }

        ToolButton {
            enabled: _searchInfo.hasMultipleResults
            focusPolicy: Qt.NoFocus

            icon {
                source: "qrc:/data/icons/keyboard_arrow_up_black_24dp.svg"
                width: 24
                height: 24
            }

            onPressed: root.controller.selectPrevious()
        }

        ToolButton {
            enabled: _searchInfo.hasMultipleResults
            focusPolicy: Qt.NoFocus

            icon {
                source: "qrc:/data/icons/keyboard_arrow_down_black_24dp.svg"
                width: 24
                height: 24
            }

            onPressed: root.controller.selectNext()
        }

        ToolButton {
            focusPolicy: Qt.NoFocus

            icon {
                source: "qrc:/data/icons/close_black_24dp.svg"
                width: 18
                height: 18
            }

            onPressed: root.close()
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
        onActivated: {
            root.searchActive = true;
            _textField.selectAll();
            _textField.forceActiveFocus();
        }
    }

    Shortcut {
        enabled: root.visible
        sequence: "esc"
        autoRepeat: false
        onActivated: root.close()
    }

    DragHandler {
        id: _dragHandler

        readonly property int marginVertical: 15
        readonly property real dragScaleFactor: 1.0375
        readonly property int snapThreshold: 15
        readonly property int minY: marginVertical
        readonly property int maxY: root.parent.height - root.height - marginVertical

        property int targetY: maxY
        property int dragStartY: -1
        property bool snapToBottom: true

        function updateTargetPosition(newY: int): void {
            targetY = Math.max(minY, Math.min(maxY, newY));
            snapToBottom = (targetY >= maxY - snapThreshold);

            if (!active && snapToBottom) {
                targetY = maxY;
            }
        }

        dragThreshold: 0
        target: null
        xAxis.enabled: false
        yAxis.enabled: true

        onActiveChanged: {
            dragStartY = active ? root.y : -1;
            if (active) {
                _dragScaleAnimation.from = 1;
                _dragScaleAnimation.to = dragScaleFactor;
            } else {
                _dragScaleAnimation.from = dragScaleFactor;
                _dragScaleAnimation.to = 1;
            }
            _dragScaleAnimation.start();
        }

        onMaxYChanged: {
            if (maxY <= 0)
                return;

            if (snapToBottom) {
                targetY = maxY;
            } else {
                updateTargetPosition(targetY);
            }
        }

        yAxis.onActiveValueChanged: {
            if (dragStartY === -1)
                return;
            updateTargetPosition(dragStartY + yAxis.activeValue);
        }
    }

    NumberAnimation {
        id: _dragScaleAnimation
        target: root
        property: "scale"
        duration: 75
    }

    Binding {
        when: root.visible
        target: root
        property: "y"
        value: _dragHandler.snapToBottom && !_dragHandler.active ? _dragHandler.maxY : _dragHandler.targetY
    }
}
