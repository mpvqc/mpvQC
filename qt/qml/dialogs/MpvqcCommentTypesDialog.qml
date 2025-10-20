// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import pyobjects

import "../components"
import "../utility"

MpvqcDialog {
    id: root

    readonly property MpvqcCommentTypesDialogViewModel viewModel: MpvqcCommentTypesDialogViewModel {}
    readonly property var mpvqcTheme: MpvqcTheme

    title: qsTranslate("CommentTypesDialog", "Comment Types")
    standardButtons: Dialog.Ok | Dialog.Cancel | Dialog.Reset

    onAccepted: {
        root.viewModel.accept();
    }

    onReset: {
        root.viewModel.reset();
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

                onTextChanged: root.viewModel.onTextChanged(text)

                onActiveFocusChanged: root.viewModel.onTextFieldFocusChanged(activeFocus)

                onAccepted: root.viewModel.acceptInput()

                Keys.onEscapePressed: root.viewModel.rejectInput()
            }

            ToolButton {
                enabled: root.viewModel.isAcceptButtonEnabled

                icon {
                    width: 20
                    height: 20
                    source: "qrc:/data/icons/check_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                }

                onPressed: {
                    root.viewModel.acceptInput();
                }
            }

            ToolButton {
                enabled: root.viewModel.isRejectButtonEnabled

                icon {
                    width: 20
                    height: 20
                    source: "qrc:/data/icons/close_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                }

                onPressed: {
                    root.viewModel.rejectInput();
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

                text: root.viewModel.validationError
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

                model: root.viewModel.temporaryCommentTypesModel
                currentIndex: root.viewModel.selectedIndex
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

                    onPressed: root.viewModel.selectItem(index)

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

                    enabled: root.viewModel.isMoveUpButtonEnabled

                    icon {
                        width: 28
                        height: 28
                        source: "qrc:/data/icons/keyboard_arrow_up_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                    }

                    onPressed: {
                        _listView.upMovement = true;
                        root.viewModel.moveUp();
                    }
                }

                ToolButton {
                    enabled: root.viewModel.isMoveDownButtonEnabled

                    icon {
                        width: 28
                        height: 28
                        source: "qrc:/data/icons/keyboard_arrow_down_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                    }

                    onPressed: {
                        _listView.upMovement = false;
                        root.viewModel.moveDown();
                    }
                }

                ToolButton {
                    enabled: root.viewModel.isEditButtonEnabled

                    icon {
                        source: "qrc:/data/icons/edit_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                    }

                    onPressed: {
                        root.viewModel.startEdit();
                    }
                }

                ToolButton {
                    enabled: root.viewModel.isDeleteButtonEnabled

                    icon {
                        source: "qrc:/data/icons/delete_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                    }

                    onPressed: {
                        root.viewModel.deleteItem();
                    }
                }
            }
        }
    }

    Connections {
        target: root.viewModel

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
