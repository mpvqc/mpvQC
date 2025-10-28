// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import pyobjects

import "../../components"
import "../../utility"

Popup {
    id: root

    required property MpvqcSearchBoxViewModel viewModel

    readonly property bool isApplicationFullScreen: MpvqcWindowUtility.isFullscreen
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

    Material.background: MpvqcTheme.backgroundAlternate
    Material.foreground: MpvqcTheme.foregroundAlternate
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

        MpvqcIconLabel {
            Layout.leftMargin: 8
            Layout.rightMargin: 4

            icon {
                source: "qrc:/data/icons/search_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                height: 24
                width: 24
                color: Material.hintTextColor
            }
        }

        TextField {
            id: _textField

            Layout.fillWidth: true
            focus: false
            selectByMouse: true
            horizontalAlignment: Text.AlignLeft

            onTextChanged: {
                const sanitized = MpvqcTableUtility.sanitizeText(text);
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
                width: 18
                height: 18
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
            if (active) {
                dragStartY = root.y;
                _dragScaleAnimation.from = 1;
                _dragScaleAnimation.to = dragScaleFactor;
                _dragScaleAnimation.start();
            } else {
                dragStartY = -1;
                _dragScaleAnimation.from = dragScaleFactor;
                _dragScaleAnimation.to = 1;
                _dragScaleAnimation.start();
            }
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

    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.NoButton
        hoverEnabled: true
        cursorShape: _dragHandler.active ? Qt.ClosedHandCursor : Qt.OpenHandCursor
        z: _dragHandler.active ? 1 : -1
    }
}
