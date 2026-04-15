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
    objectName: "searchBoxPopup"

    required property MpvqcSearchBoxViewModel viewModel

    readonly property bool isApplicationFullScreen: MpvqcWindowUtility.isFullscreen
    readonly property string searchQuery: searchActive ? viewModel.searchQuery : ""
    readonly property int edgeMarginHorizontal: 30
    readonly property int edgeMarginVertical: 15

    property bool searchActive: false

    function closeWithoutAnimation(): void {
        const exitAnimation = exit;
        exit = null;
        root.close();
        exit = exitAnimation;
    }

    function _scaleUp(): void {
        _dragScaleAnimation.from = root.scale;
        _dragScaleAnimation.to = _dragScaleAnimation.dragScaleFactor;
        _dragScaleAnimation.start();
    }

    function _scaleDown(): void {
        _dragScaleAnimation.from = root.scale;
        _dragScaleAnimation.to = 1;
        _dragScaleAnimation.start();
    }

    function _shouldSuppressScaleOnPress(): bool {
        return _textFieldHover.hovered || (_previousButton.enabled && _previousButton.hovered) || (_nextButton.enabled && _nextButton.hovered) || _closeButton.hovered;
    }

    x: mirrored ? edgeMarginHorizontal : parent.width - width - edgeMarginHorizontal
    y: parent.height - height - edgeMarginVertical
    z: 1

    width: 450
    height: _textField.height + topPadding + bottomPadding
    padding: 5

    closePolicy: Popup.NoAutoClose

    Material.background: MpvqcTheme.backgroundAlternate
    Material.foreground: MpvqcTheme.foregroundAlternate
    Material.roundedScale: Material.SmallScale

    enter: Transition {
        NumberAnimation {
            property: "opacity"
            from: 0.0
            to: 1.0
            duration: 150
            easing.type: Easing.OutCubic
        }
        NumberAnimation {
            property: "scale"
            from: 0.95
            to: 1.0
            duration: 150
            easing.type: Easing.OutCubic
        }
    }

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

    HoverHandler {
        objectName: "popupBackgroundCursorHandler"
        cursorShape: _dragHandler.isPressed || _dragHandler.active ? Qt.ClosedHandCursor : Qt.OpenHandCursor
    }

    RowLayout {
        width: root.width - root.leftPadding - root.rightPadding
        spacing: 0

        MpvqcIconLabel {
            objectName: "searchIconLabel"
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
            objectName: "searchTextField"

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

            HoverHandler {
                id: _textFieldHover
                objectName: "searchTextFieldCursorHandler"
                cursorShape: _dragHandler.active ? Qt.ClosedHandCursor : Qt.IBeamCursor
            }

            Component.onCompleted: {
                background.fillColor = "transparent";
                background.outlineColor = "transparent";
                background.focusedOutlineColor = "transparent";
            }
        }

        Label {
            objectName: "statusLabel"
            text: root.viewModel.statusLabel
            color: Material.hintTextColor
            Layout.leftMargin: 4
            Layout.rightMargin: 4
        }

        ToolSeparator {
            padding: 0
        }

        Item {
            implicitWidth: _previousButton.implicitWidth
            implicitHeight: _previousButton.implicitHeight

            ToolButton {
                id: _previousButton
                objectName: "previousButton"
                anchors.fill: parent

                enabled: root.viewModel.hasMultipleResults
                focusPolicy: Qt.NoFocus

                icon {
                    source: "qrc:/data/icons/keyboard_arrow_up_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                }

                onClicked: root.viewModel.selectPrevious()

                HoverHandler {
                    objectName: "previousButtonEnabledCursorHandler"
                    cursorShape: _dragHandler.active ? Qt.ClosedHandCursor : Qt.ArrowCursor
                }
            }

            HoverHandler {
                objectName: "previousButtonDisabledCursorHandler"
                enabled: !_previousButton.enabled
                cursorShape: _dragHandler.isPressed || _dragHandler.active ? Qt.ClosedHandCursor : Qt.OpenHandCursor
            }
        }

        Item {
            implicitWidth: _nextButton.implicitWidth
            implicitHeight: _nextButton.implicitHeight

            ToolButton {
                id: _nextButton
                objectName: "nextButton"
                anchors.fill: parent

                enabled: root.viewModel.hasMultipleResults
                focusPolicy: Qt.NoFocus

                icon {
                    source: "qrc:/data/icons/keyboard_arrow_down_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                }

                onClicked: root.viewModel.selectNext()

                HoverHandler {
                    objectName: "nextButtonEnabledCursorHandler"
                    cursorShape: _dragHandler.active ? Qt.ClosedHandCursor : Qt.ArrowCursor
                }
            }

            HoverHandler {
                objectName: "nextButtonDisabledCursorHandler"
                enabled: !_nextButton.enabled
                cursorShape: _dragHandler.isPressed || _dragHandler.active ? Qt.ClosedHandCursor : Qt.OpenHandCursor
            }
        }

        ToolButton {
            id: _closeButton
            objectName: "closeButton"

            focusPolicy: Qt.NoFocus

            icon {
                width: 18
                height: 18
                source: "qrc:/data/icons/close_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            }

            onClicked: root.close()

            HoverHandler {
                objectName: "closeButtonCursorHandler"
                cursorShape: _dragHandler.active ? Qt.ClosedHandCursor : Qt.ArrowCursor
            }
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

    MpvqcSearchBoxDragHandler {
        id: _dragHandler

        parent: root.contentItem

        edgeMarginVertical: root.edgeMarginVertical
        parentHeight: root.parent.height
        popupHeight: root.height
        popupY: root.y

        onPointerPressed: {
            if (!root._shouldSuppressScaleOnPress()) {
                root._scaleUp();
            }
        }

        onPointerReleased: root._scaleDown()

        onDragStarted: {
            if (root.scale < _dragScaleAnimation.dragScaleFactor) {
                root._scaleUp();
            }
        }
    }

    NumberAnimation {
        id: _dragScaleAnimation

        readonly property real dragScaleFactor: 1.0375

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
