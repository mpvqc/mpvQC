// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.impl
import QtQuick.Controls.Material
import QtQuick.Layouts

import pyobjects

import "../../utility"

Popup {
    id: root

    required property MpvqcSearchBoxViewModel viewModel

    readonly property bool isApplicationFullScreen: MpvqcWindowProperties.isFullscreen
    readonly property string searchQuery: searchActive ? viewModel.searchQuery : ""

    property bool searchActive: false

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

    RowLayout {
        width: root.width - root.leftPadding - root.rightPadding
        spacing: 0

        IconLabel {
            Layout.leftMargin: 8
            Layout.rightMargin: 8

            icon {
                source: "qrc:/data/icons/search_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                color: Material.hintTextColor
            }
        }

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
                    root.viewModel.search(text);
                }
            }

            Component.onCompleted: {
                background.fillColor = "transparent";
                background.outlineColor = "transparent";
                background.focusedOutlineColor = "transparent";
            }
        }

        Label {
            text: root.viewModel.statusLabel
            color: Material.hintTextColor
            Layout.leftMargin: 4
            Layout.rightMargin: 4
        }

        ToolSeparator {
            padding: 0
        }

        ToolButton {
            enabled: root.viewModel.hasMultipleResults
            focusPolicy: Qt.NoFocus

            icon {
                source: "qrc:/data/icons/keyboard_arrow_up_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            }

            onPressed: root.viewModel.selectPrevious()
        }

        ToolButton {
            enabled: root.viewModel.hasMultipleResults
            focusPolicy: Qt.NoFocus

            icon {
                source: "qrc:/data/icons/keyboard_arrow_down_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            }

            onPressed: root.viewModel.selectNext()
        }

        ToolButton {
            focusPolicy: Qt.NoFocus

            icon {
                source: "qrc:/data/icons/close_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            }

            onPressed: root.close()
        }
    }

    Shortcut {
        enabled: root.visible && _textField.activeFocus
        sequences: ["up", "shift+return"]
        onActivated: root.viewModel.selectPrevious()
    }

    Shortcut {
        enabled: root.visible && _textField.activeFocus
        sequences: ["down", "return"]
        onActivated: root.viewModel.selectNext()
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
