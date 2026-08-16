// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls
import QtQuick.Templates as T

import io.github.mpvqc.mpvQC.Python

Loader {
    id: root

    required property MpvqcCommentTableViewModel viewModel

    readonly property url editCommentTypeMenu: Qt.resolvedUrl("MpvqcEditCommentTypeMenu.qml")
    readonly property url editCommentPopup: Qt.resolvedUrl("MpvqcEditCommentPopup.qml")
    readonly property url editTimePopup: Qt.resolvedUrl("MpvqcEditTimePopup.qml")

    readonly property bool isEditingCommentType: active && source === editCommentTypeMenu

    signal closed

    function startEditingTime(index: int, time: int, coordinates: point): void {
        asynchronous = true;
        setSource(editTimePopup, {
            viewModel: root.viewModel,
            currentTime: time,
            currentListIndex: index,
            openedAt: coordinates
        });
        active = true;
    }

    function startEditingCommentType(index: int, currentCommentType: string, coordinates: point): void {
        // Sync on purpose: async creation hits a Qt race that mis-stacks
        // Repeater-built menu items under popupType Window (QTBUG-84125).
        asynchronous = false;
        setSource(editCommentTypeMenu, {
            viewModel: root.viewModel,
            currentCommentType: currentCommentType,
            currentListIndex: index,
            position: coordinates
        });
        active = true;
    }

    function startEditingComment(index: int, currentComment: string, parentItem: Label): void {
        asynchronous = false;
        setSource(editCommentPopup, {
            parent: parentItem,
            viewModel: root.viewModel,
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
        if (!active) {
            return;
        }
        if (!item) {
            // Async load in flight: cancel before the editor materializes.
            active = false;
            return;
        }
        switch (source) {
        case editTimePopup:
            const popup = item as MpvqcEditTimePopup;
            popup.acceptValue = false;
            popup.close();
            break;
        case editCommentTypeMenu:
            const menu = item as MpvqcEditCommentTypeMenu;
            menu.close();
            break;
        }
    }

    active: false
    visible: active

    onLoaded: item.open() // qmllint disable

    Connections {
        // A style implements Popup and Menu as separate files over T.Popup and T.Menu, so
        // casting a Menu to the styled Popup yields null. T.Popup is the only shared base.
        target: root.item as T.Popup

        function onClosed(): void {
            // Focus loss fires onClosed() synchronously, before any click handler on the delegate runs.
            // Qt.callLater defers deactivation so click/double-click handlers execute first and can
            // start a new editor before we decide whether to deactivate.
            //
            // Guard: bail out if another editor is already open or still loading, to avoid
            // killing an in-flight async load triggered by a rapid editor transition.
            Qt.callLater(() => {
                const anotherEditorIsOpen = root.item && root.item.visible;
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
