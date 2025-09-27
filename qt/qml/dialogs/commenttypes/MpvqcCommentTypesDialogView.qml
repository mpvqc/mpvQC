// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import pyobjects

import "../../shared"
import "../../themes"

MpvqcDialog {
    id: root

    readonly property MpvqcCommentTypesDialogControllerPyObject controller: MpvqcCommentTypesDialogControllerPyObject {}
    readonly property var mpvqcTheme: MpvqcTheme

    title: qsTranslate("CommentTypesDialog", "Comment Types")
    standardButtons: Dialog.Ok | Dialog.Cancel | Dialog.Reset

    onAccepted: {
        root.controller.accept();
    }

    onReset: {
        root.controller.reset();
    }

    contentItem: ColumnLayout {
        spacing: 10

        RowLayout {
            Layout.fillWidth: true
            Layout.topMargin: 20

            TextField {
                id: _textField

                Layout.fillWidth: true

                selectByMouse: true
                horizontalAlignment: Text.AlignLeft
                placeholderText: qsTranslate("CommentTypesDialog", "New comment type")

                onTextChanged: root.controller.onTextChanged(text)

                onActiveFocusChanged: root.controller.onTextFieldFocusChanged(activeFocus)

                onAccepted: root.controller.acceptInput()

                Keys.onEscapePressed: root.controller.rejectInput()
            }

            ToolButton {
                enabled: root.controller.isAcceptButtonEnabled

                icon {
                    width: 20
                    height: 20
                    source: "qrc:/data/icons/done_black_24dp.svg"
                }

                onPressed: {
                    root.controller.acceptInput();
                }
            }

            ToolButton {
                enabled: root.controller.isRejectButtonEnabled

                icon {
                    width: 20
                    height: 20
                    source: "qrc:/data/icons/close_black_24dp.svg"
                }

                onPressed: {
                    root.controller.rejectInput();
                }
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.preferredHeight: (fontMetrics.lineSpacing * _errorLabel.lineCount) + _errorLabel.topPadding + _errorLabel.bottomPadding

            Label {
                id: _errorLabel

                anchors.fill: parent

                topPadding: 4
                bottomPadding: 6

                text: root.controller.validationError
                maximumLineCount: 3
                color: root.mpvqcTheme.control
                wrapMode: Label.WordWrap
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignTop

                FontMetrics {
                    id: fontMetrics
                    font: _errorLabel.font
                }
            }
        }

        RowLayout {
            Layout.fillHeight: true
            Layout.fillWidth: true

            ListView {
                id: _listView

                property bool upMovement: true

                Layout.fillWidth: true
                Layout.fillHeight: true

                model: root.controller.temporaryCommentTypesModel
                currentIndex: root.controller.selectedIndex
                spacing: 0
                clip: true
                reuseItems: false // prevent artifacts from alternating row colors when deleting items
                boundsBehavior: Flickable.StopAtBounds

                highlightMoveDuration: 50
                highlightMoveVelocity: -1
                highlightResizeDuration: 0
                highlightResizeVelocity: -1

                highlight: Rectangle {
                    color: root.mpvqcTheme.rowHighlight
                    radius: Material.ExtraSmallScale
                }

                delegate: ItemDelegate {
                    id: _delegate

                    required property var modelData
                    required property int index

                    readonly property color foregroundColor: root.mpvqcTheme.getForeground(index % 2 === 1)
                    readonly property color backgroundColor: root.mpvqcTheme.getBackground(index % 2 === 1)

                    width: ListView.view.width - _scrollBar.visibleWidth
                    height: _upButton.height

                    Material.foreground: ListView.isCurrentItem ? root.mpvqcTheme.rowHighlightText : foregroundColor
                    Material.background: backgroundColor

                    onPressed: root.controller.selectItem(index)

                    background: Rectangle {
                        parent: _delegate.parent
                        y: _delegate.y
                        height: _delegate.height
                        color: _delegate.backgroundColor
                        radius: Material.ExtraSmallScale
                    }

                    contentItem: Label {
                        padding: 15
                        anchors.fill: parent

                        text: qsTranslate("CommentTypes", _delegate.modelData.display)
                        elide: LayoutMirroring.enabled ? Text.ElideLeft : Text.ElideRight
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                    }
                }

                ScrollBar.vertical: ScrollBar {
                    id: _scrollBar

                    readonly property bool isShown: _listView.contentHeight > _listView.height
                    readonly property real visibleWidth: isShown ? width : 0

                    policy: isShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
                }

                onCurrentIndexChanged: {
                    ensureVisible(currentIndex);
                }

                Behavior on contentY {
                    SmoothedAnimation {
                        duration: 75
                    }
                }

                move: Transition {
                    SmoothedAnimation {
                        properties: "y"
                        duration: 75
                    }
                }

                displaced: Transition {
                    SmoothedAnimation {
                        properties: "y"
                        duration: 75
                    }
                }

                function ensureVisible(index: int): void {
                    const targetIndex = upMovement ? index + 1 : index - 1;
                    const item = itemAtIndex(targetIndex);
                    if (!item) {
                        return;
                    }

                    const itemTop = item.y - contentY;
                    const itemBottom = itemTop + item.height;
                    const viewHeight = height;

                    const isFullyVisible = itemTop >= 0 && itemBottom <= viewHeight;
                    if (isFullyVisible) {
                        return;
                    }

                    const padding = 25;

                    if (itemTop < 0) {
                        contentY = Math.max(0, item.y - padding);
                    } else if (itemBottom > viewHeight) {
                        contentY = Math.min(contentHeight - height, item.y + item.height - height + padding);
                    }
                }
            }

            Column {
                Layout.alignment: Qt.AlignTop
                spacing: 4

                ToolButton {
                    id: _upButton

                    enabled: root.controller.isMoveUpButtonEnabled

                    icon {
                        width: 28
                        height: 28
                        source: "qrc:/data/icons/keyboard_arrow_up_black_24dp.svg"
                    }

                    onPressed: {
                        _listView.upMovement = true;
                        root.controller.moveUp();
                    }
                }

                ToolButton {
                    enabled: root.controller.isMoveDownButtonEnabled

                    icon {
                        width: 28
                        height: 28
                        source: "qrc:/data/icons/keyboard_arrow_down_black_24dp.svg"
                    }

                    onPressed: {
                        _listView.upMovement = false;
                        root.controller.moveDown();
                    }
                }

                ToolButton {
                    enabled: root.controller.isEditButtonEnabled

                    icon {
                        width: 18
                        height: 18
                        source: "qrc:/data/icons/edit_black_24dp.svg"
                    }

                    onPressed: {
                        root.controller.startEdit();
                    }
                }

                ToolButton {
                    enabled: root.controller.isDeleteButtonEnabled

                    icon {
                        width: 24
                        height: 24
                        source: "qrc:/data/icons/delete_black_24dp.svg"
                    }

                    onPressed: {
                        root.controller.deleteItem();
                    }
                }
            }
        }
    }

    Connections {
        target: root.controller

        function onClearTextFieldRequested(): void {
            _textField.placeholderText = qsTranslate("CommentTypesDialog", "New comment type");
            _textField.text = "";
        }

        function onSetTextFieldRequested(text: string): void {
            const commentType = qsTranslate("CommentTypes", text);
            //: %1 will be the comment type being edited
            _textField.placeholderText = qsTranslate("CommentTypesDialog", 'Edit "%1"').arg(commentType);
            _textField.text = commentType;
        }

        function onFocusTextFieldRequested(focus: bool): void {
            if (focus) {
                _textField.forceActiveFocus();
            } else {
                _textField.focus = false;
            }
        }
    }
}
