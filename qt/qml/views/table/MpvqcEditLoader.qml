// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

Loader {
    id: root

    required property var viewModel

    readonly property url editCommentTypeMenu: Qt.resolvedUrl("MpvqcEditCommentTypeMenu.qml")
    readonly property url editCommentPopup: Qt.resolvedUrl("MpvqcEditCommentPopup.qml")
    readonly property url editTimePopup: Qt.resolvedUrl("MpvqcEditTimePopup.qml")

    readonly property bool isEditingComment: source === editCommentPopup

    signal commentEditPopupHeightChanged(heightDelta: int, totalHeight: int)

    function _startEditingTime(index: int, time: int, coordinates: point): void {
        asynchronous = true;
        setSource(editTimePopup, {
            currentTime: time,
            currentListIndex: index,
            videoDuration: root.viewModel.videoDuration,
            openedAt: coordinates
        });
        active = true;
    }

    function _startEditingCommentType(index: int, currentCommentType: string, coordinates: point): void {
        asynchronous = true;
        setSource(editCommentTypeMenu, {
            currentCommentType: currentCommentType,
            currentListIndex: index,
            commentTypes: root.viewModel.commentTypes,
            position: coordinates
        });
        active = true;
    }

    function startEditingComment(index: int, currentComment: string, parentItem: Label): void {
        asynchronous = false;
        setSource(editCommentPopup, {
            parent: parentItem,
            currentComment: currentComment,
            currentListIndex: index,
            leftPadding: parentItem.leftPadding / 2,
            rightPadding: parentItem.rightPadding / 2,
            topPadding: parentItem.topPadding / 2,
            bottomPadding: parentItem.bottomPadding / 2
        });
        active = true;
    }

    active: false
    visible: active

    onLoaded: item.open() // qmllint disable

    Connections {
        target: root.viewModel

        function onTimeEditRequested(index: int, time: int, coordinates: point): void {
            root._startEditingTime(index, time, coordinates);
        }

        function onCommentTypeEditRequested(index: int, commentType: string, coordinates: point): void {
            root._startEditingCommentType(index, commentType, coordinates);
        }
    }

    Connections {
        target: root.item
        ignoreUnknownSignals: true

        function onTimeTemporaryChanged(time: int): void {
            root.viewModel.jumpToTime(time);
        }

        function onTimeEdited(index: int, newTime: int): void {
            root.viewModel.updateTime(index, newTime);
        }

        function onTimeKept(oldTime: int): void {
            root.viewModel.jumpToTime(oldTime);
        }

        function onCommentTypeEdited(index: int, newCommentType: string): void {
            root.viewModel.updateCommentType(index, newCommentType);
        }

        function onCommentEdited(index: int, newComment: string): void {
            root.viewModel.updateComment(index, newComment);
        }

        function onCommentEditPopupHeightChanged(editorHeight: int, heightDelta: int): void {
            root.commentEditPopupHeightChanged(editorHeight, heightDelta);
        }

        function onClosed(): void {
            // When closing without animation, focus loss triggers onClosed() before click handlers on delegates
            // execute. Defer deactivation to allow click handlers to detect the editing state as a human would perceive
            // it. In typical usage, this enables the sequence: editing → click other component → editor closes → new
            // editor opens smoothly. The deferred check prevents deactivation during rapid editor transitions.
            Qt.callLater(() => {
                if (root.item && root.item.opened) {
                    return;
                }
                root.active = false;
            });
        }
    }
}
