// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

Loader {
    id: root

    readonly property url editCommentTypeMenu: Qt.resolvedUrl("MpvqcEditCommentTypeMenu.qml")
    readonly property url editCommentPopup: Qt.resolvedUrl("MpvqcEditCommentPopup.qml")
    readonly property url editTimePopup: Qt.resolvedUrl("MpvqcEditTimePopup.qml")

    readonly property bool isEditingCommentType: active && source === editCommentTypeMenu

    signal timeTemporaryChanged(time: int)
    signal timeKept(oldTime: int)
    signal commentEditPopupHeightChanged(editorHeight: int, heightDelta: int)

    signal timeEdited(index: int, newTime: int)
    signal commentTypeEdited(index: int, newCommentType: string)
    signal commentEdited(index: int, newComment: string)
    signal closed

    function startEditingTime(index: int, time: int, coordinates: point, videoDuration: real): void {
        asynchronous = true;
        setSource(editTimePopup, {
            currentTime: time,
            currentListIndex: index,
            videoDuration: videoDuration,
            openedAt: coordinates
        });
        active = true;
    }

    function startEditingCommentType(index: int, currentCommentType: string, coordinates: point, commentTypes: var): void {
        asynchronous = true;
        setSource(editCommentTypeMenu, {
            currentCommentType: currentCommentType,
            currentListIndex: index,
            commentTypes: commentTypes,
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

    function abortEdit(): void {
        if (active && item) {
            if (item.acceptValue !== undefined) {
                item.acceptValue = false;
            }
            item.close();
        }
    }

    active: false
    visible: active

    onLoaded: item.open() // qmllint disable

    Connections {
        target: root.item
        ignoreUnknownSignals: true

        function onTimeTemporaryChanged(time: int): void {
            root.timeTemporaryChanged(time);
        }

        function onTimeEdited(index: int, newTime: int): void {
            root.timeEdited(index, newTime);
        }

        function onTimeKept(oldTime: int): void {
            root.timeKept(oldTime);
        }

        function onCommentTypeEdited(index: int, newCommentType: string): void {
            root.commentTypeEdited(index, newCommentType);
        }

        function onCommentEdited(index: int, newComment: string): void {
            root.commentEdited(index, newComment);
        }

        function onCommentEditPopupHeightChanged(editorHeight: int, heightDelta: int): void {
            root.commentEditPopupHeightChanged(editorHeight, heightDelta);
        }

        function onClosed(): void {
            // Focus loss fires onClosed() synchronously, before any click handler on the delegate runs.
            // Qt.callLater defers deactivation so click/double-click handlers execute first and can
            // start a new editor before we decide whether to deactivate.
            //
            // Guard: bail out if another editor is already open or still loading, to avoid
            // killing an in-flight async load triggered by a rapid editor transition.
            Qt.callLater(() => {
                const anotherEditorIsOpen = root.item && root.item.opened;
                const anotherEditorIsLoading = !root.item && root.active;
                if (anotherEditorIsOpen || anotherEditorIsLoading) {
                    return;
                }
                root.active = false;
                root.closed();
            });
        }
    }
}
