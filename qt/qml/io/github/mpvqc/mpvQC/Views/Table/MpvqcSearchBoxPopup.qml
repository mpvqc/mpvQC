// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material as M
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

Popup {
    id: root
    objectName: "searchBoxPopup"

    required property MpvqcSearchBoxViewModel viewModel

    readonly property bool isApplicationFullScreen: MpvqcWindowUtility.isFullscreen
    readonly property string searchQuery: searchActive ? viewModel.searchQuery : ""

    readonly property int edgeMarginHorizontal: 30
    readonly property int edgeMarginVertical: 15

    property bool searchActive: false

    // While one is open it owns the input, so cursor claims, the drag grab, and
    // hover feedback all stand down.
    readonly property bool _modalOverlayOpen: MpvqcModalState.anyModalOverlayOpen

    readonly property real _dragScaleFactor: 1.0375

    readonly property bool _anyChildHovered: _textField.hovered || (_previousButton.enabled && _previousButton.hovered) || (_nextButton.enabled && _nextButton.hovered) || _closeButton.hovered

    // The drag handler grabs any press inside these bounds, including one that landed on
    // a popup drawn above. Hovering does respect what is on top, so it says whether the
    // press was really meant for us. Once a drag is under way the pointer may leave.
    readonly property bool _shouldScaleUp: _dragHandler.active || (_dragHandler.isPressed && _backgroundHover.hovered && !_anyChildHovered)

    readonly property int _grabCursor: _dragHandler.isPressed || _dragHandler.active ? Qt.ClosedHandCursor : Qt.OpenHandCursor

    // A modal overlay owns the input, so a plain arrow is the only honest cursor anywhere
    // in the box; during a drag the whole box is in hand. Undefined stands down and lets
    // the cursors below through, the text field's built-in I-beam included.
    readonly property var _overrideCursor: _modalOverlayOpen ? Qt.ArrowCursor : (_dragHandler.active ? Qt.ClosedHandCursor : undefined)

    function closeWithoutAnimation(): void {
        const exitAnimation = exit;
        exit = null;
        root.close();
        exit = exitAnimation;
    }

    x: mirrored ? edgeMarginHorizontal : parent.width - width - edgeMarginHorizontal
    y: parent.height - height - edgeMarginVertical
    z: MpvqcConstants.zSearchBox

    width: 450
    height: _textField.height + topPadding + bottomPadding
    padding: 5

    scale: _shouldScaleUp ? _dragScaleFactor : 1

    closePolicy: Popup.NoAutoClose

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

    M.Material.background: MpvqcAppearance.palette.popupBackground
    M.Material.foreground: MpvqcAppearance.palette.popupText
    M.Material.roundedScale: M.Material.SmallScale

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
        id: _backgroundHover
        objectName: "popupBackgroundCursorHandler"
        cursorShape: root._grabCursor
    }

    RowLayout {
        anchors.verticalCenter: parent.verticalCenter

        width: root.width - root.leftPadding - root.rightPadding
        spacing: 0

        MpvqcIconLabel {
            objectName: "searchIconLabel"

            icon {
                source: MpvqcIcons.search
                height: 24
                width: 24
                color: MpvqcAppearance.palette.hint
            }

            Layout.leftMargin: 8
            Layout.rightMargin: 4
        }

        TextField {
            id: _textField
            objectName: "searchTextField"

            focus: false
            selectByMouse: true
            hoverEnabled: !root._modalOverlayOpen
            horizontalAlignment: Text.AlignLeft

            Layout.fillWidth: true

            ContextMenu.menu: null

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
            objectName: "statusLabel"
            text: root.viewModel.statusLabel
            color: MpvqcAppearance.palette.hint
            Layout.leftMargin: 4
            Layout.rightMargin: 4
        }

        ToolSeparator {
            padding: 0
        }

        Item {
            implicitWidth: _previousButton.implicitWidth
            implicitHeight: _previousButton.implicitHeight

            Layout.preferredWidth: 36
            Layout.preferredHeight: 36

            ToolButton {
                id: _previousButton
                objectName: "previousButton"
                anchors.fill: parent

                enabled: root.viewModel.hasMultipleResults
                focusPolicy: Qt.NoFocus
                hoverEnabled: !root._modalOverlayOpen

                icon {
                    source: MpvqcIcons.keyboardArrowUp
                }

                onClicked: root.viewModel.selectPrevious()
            }

            HoverHandler {
                objectName: "previousButtonCursorHandler"
                cursorShape: _previousButton.enabled ? Qt.ArrowCursor : root._grabCursor
            }
        }

        Item {
            implicitWidth: _nextButton.implicitWidth
            implicitHeight: _nextButton.implicitHeight

            Layout.preferredWidth: 36
            Layout.preferredHeight: 36
            Layout.leftMargin: 3

            ToolButton {
                id: _nextButton
                objectName: "nextButton"
                anchors.fill: parent

                enabled: root.viewModel.hasMultipleResults
                focusPolicy: Qt.NoFocus
                hoverEnabled: !root._modalOverlayOpen

                icon {
                    source: MpvqcIcons.keyboardArrowDown
                }

                onClicked: root.viewModel.selectNext()
            }

            HoverHandler {
                objectName: "nextButtonCursorHandler"
                cursorShape: _nextButton.enabled ? Qt.ArrowCursor : root._grabCursor
            }
        }

        ToolButton {
            id: _closeButton
            objectName: "closeButton"

            focusPolicy: Qt.NoFocus
            hoverEnabled: !root._modalOverlayOpen

            icon {
                width: 18
                height: 18
                source: MpvqcIcons.close
            }

            Layout.preferredWidth: 36
            Layout.preferredHeight: 36
            Layout.leftMargin: 3
            Layout.rightMargin: 3

            onClicked: root.close()

            HoverHandler {
                objectName: "closeButtonCursorHandler"
                cursorShape: Qt.ArrowCursor
            }
        }
    }

    // Topmost while it claims a cursor, so the claim beats every cursor below, including
    // the text field's built-in I-beam. Hidden otherwise: an always-on cover would steal
    // the hover highlights from the controls beneath.
    Item {
        anchors.fill: parent
        visible: root._overrideCursor !== undefined

        HoverHandler {
            objectName: "cursorOverrideHandler"
            cursorShape: root._overrideCursor
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
        enabled: root.visible && MpvqcWindowUtility.isMainWindowFocused
        sequence: "ctrl+f"
        autoRepeat: false
        onActivated: {
            root.searchActive = true;
            _textField.selectAll();
            _textField.forceActiveFocus();
        }
    }

    Shortcut {
        enabled: root.visible && MpvqcWindowUtility.isMainWindowFocused
        sequence: "esc"
        autoRepeat: false
        onActivated: root.close()
    }

    MpvqcSearchBoxDragHandler {
        id: _dragHandler

        parent: root.contentItem
        enabled: !root._modalOverlayOpen

        edgeMarginVertical: root.edgeMarginVertical
        parentHeight: root.parent.height
        popupHeight: root.height
        popupY: root.y
    }

    Binding {
        when: root.visible
        target: root
        property: "y"
        value: _dragHandler.snapToBottom && !_dragHandler.active ? _dragHandler.maxY : _dragHandler.targetY
    }

    Behavior on scale {
        enabled: root.opened
        NumberAnimation {
            duration: 75
        }
    }
}
