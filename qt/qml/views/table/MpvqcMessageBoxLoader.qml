// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import "../../components"
import "../../views/table"
import "../../utility"

Loader {
    id: root

    required property var viewModel

    property int commentIndex: -1
    property int commentTime: 0
    property string commentType: ""
    property string commentText: ""

    signal closed

    active: false
    visible: active

    sourceComponent: _messageBoxComponent

    onLoaded: item.open() // qmllint disable

    Component {
        id: _messageBoxComponent

        MpvqcMessageBox {
            title: qsTranslate("MessageBoxes", "Delete Comment")
            standardButtons: Dialog.Yes | Dialog.Cancel

            contentItem: ColumnLayout {
                spacing: 10

                Label {
                    text: qsTranslate("MessageBoxes", "Do you really want to delete this comment?")
                    horizontalAlignment: Text.AlignLeft
                    wrapMode: Label.WordWrap
                    Layout.fillWidth: true
                }

                Label {
                    Layout.fillWidth: true
                    Layout.topMargin: 20
                    textFormat: Text.StyledText
                    horizontalAlignment: Text.AlignLeft
                    wrapMode: Label.WordWrap

                    text: {
                        const hasComment = root.commentText.trim().length > 0;
                        const commentColor = hasComment ? MpvqcTheme.foreground : Material.hintTextColor;
                        const commentContent = hasComment ? root.commentText : qsTranslate("MessageBoxes", "No text available");
                        const noTextFallback = qsTranslate("MessageBoxes", "No text available");
                        const commentContent = hasComment ? root.commentText : noTextFallback;

                        const time = `<font color="${MpvqcTheme.control}">${MpvqcTableUtility.formatTime(root.commentTime)}</font>`;
                        const type = `<font color="${MpvqcTheme.control}">${qsTranslate("CommentTypes", root.commentType)}</font>`;
                        const comment = `<font color="${commentColor}">${commentContent}</font>`;
                        const separator = "&nbsp;&nbsp;•&nbsp;&nbsp;";

                        return `${time}${separator}${type}${separator}${comment}`;
                    }
                }
            }

            onAccepted: {
                root.viewModel.removeRow(root.commentIndex);
            }

            onClosed: {
                root.active = false;
                root.closed();
            }
        }
    }

    Connections {
        target: root.viewModel

        function onDeleteCommentRequested(index: int, time: int, commentType: string, commentText: string): void {
            root.commentIndex = index;
            root.commentTime = time;
            root.commentType = commentType;
            root.commentText = commentText;

            root.active = true;
        }
    }
}
