// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

Loader {
    id: root

    required property MpvqcCommentTableViewModel viewModel

    property int commentIndex: -1
    property int commentTime: 0
    property string commentType: ""
    property string commentText: ""

    signal closed

    function requestDeletion(index: int, time: int, commentType: string, commentText: string): void {
        root.commentIndex = index;
        root.commentTime = time;
        root.commentType = commentType;
        root.commentText = commentText;
        root.active = true;
    }

    function dismiss(): void {
        (root.item as MpvqcMessageBox)?.close();
    }

    active: false
    visible: active

    sourceComponent: _messageBoxComponent

    onLoaded: (item as MpvqcMessageBox).open()

    Component {
        id: _messageBoxComponent

        MpvqcMessageBox {
            id: _messageBox
            objectName: "deleteConfirmationMessageBox"

            // Mirrors the terms the Material style adds to the content in a Dialog's implicit height
            readonly property real _chromeHeight: topPadding + bottomPadding + (implicitHeaderHeight > 0 ? implicitHeaderHeight + spacing : 0) + (implicitFooterHeight > 0 ? implicitFooterHeight + spacing : 0)
            readonly property real _maxContentHeight: (MpvqcWindowUtility.contentFrame ?? root.Window.window.contentItem).height - 2 * MpvqcConstants.dialogEdgeMargin - _chromeHeight

            title: qsTranslate("MessageBoxes", "Delete Comment")
            contentWidth: MpvqcConstants.smallDialogContentWidth
            standardButtons: Dialog.Yes | Dialog.Cancel

            contentItem: ScrollView {
                id: _scroll

                readonly property bool _needsScrollBar: contentHeight > availableHeight

                // Cap the implicit height, never the dialog's height: under Popup.Window Qt resizes the popup
                // to its implicit height on every change and ignores an explicit one
                implicitHeight: Math.min(contentHeight, _messageBox._maxContentHeight)
                contentWidth: availableWidth
                contentHeight: _sections.implicitHeight

                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
                ScrollBar.vertical: MpvqcScrollBar {
                    parent: _scroll
                    // The scroll bar sits in the dialog's padding so it never takes width from the comment.
                    // A narrower comment wraps taller, which changes whether the bar is needed: at a length
                    // that fits only without the bar, the two flip forever and the application hangs
                    x: _scroll.mirrored ? -(_messageBox.leftPadding + width) / 2 : _scroll.width + (_messageBox.rightPadding - width) / 2
                    y: _scroll.topPadding
                    height: _scroll.availableHeight
                    policy: _scroll._needsScrollBar ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
                }

                ColumnLayout {
                    id: _sections

                    width: _scroll.availableWidth

                    MpvqcSectionCard {
                        Layout.fillWidth: true
                        Layout.topMargin: MpvqcConstants.dialogContentTopMargin

                        Label {
                            objectName: "deleteQuestion"

                            text: qsTranslate("MessageBoxes", "Do you really want to delete this comment?")
                            horizontalAlignment: Text.AlignLeft
                            wrapMode: Text.Wrap

                            Layout.fillWidth: true
                            Layout.bottomMargin: 12
                        }

                        Label {
                            objectName: "deleteMetadata"

                            text: `${MpvqcTableUtility.formatTime(root.commentTime)}  •  ${qsTranslate("CommentTypes", root.commentType)}`
                            textFormat: Text.PlainText
                            color: MpvqcAppearance.palette.hint
                            horizontalAlignment: Text.AlignLeft
                            wrapMode: Text.Wrap

                            Layout.fillWidth: true
                        }

                        Label {
                            objectName: "deletePreview"

                            readonly property bool hasComment: root.commentText.trim().length > 0

                            //: This is displayed as a fallback in the delete confirmation box when the actual comment is empty.
                            text: hasComment ? root.commentText : qsTranslate("MessageBoxes", "No text available")
                            textFormat: Text.PlainText
                            color: hasComment ? MpvqcAppearance.palette.foreground : MpvqcAppearance.palette.hint
                            horizontalAlignment: Text.AlignLeft
                            wrapMode: Text.Wrap

                            Layout.fillWidth: true
                        }
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
}
