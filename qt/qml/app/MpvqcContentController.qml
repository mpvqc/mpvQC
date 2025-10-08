// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

QtObject {

    required property var mpvqcMpvPlayerPyObject
    required property var mpvqcManager
    required property var mpvqcSettings

    // --- Controller configuration / tiny UI-agnostic state ---
    readonly property int minContainerHeight: 200
    readonly property int minContainerWidth: 500
    readonly property real defaultSplitRatio: 0.4
    readonly property int layoutOrientation: mpvqcSettings.layoutOrientation
    readonly property list<string> commentTypes: mpvqcSettings.commentTypes

    // --- Intents: the View reacts to these ---
    signal appWindowSizeRequested(width: int, height: int)
    signal disableFullScreenRequested
    signal toggleFullScreenRequested
    signal splitViewTableSizeRequested(width: int, height: int)
    signal openNewCommentMenuRequested
    signal addNewCommentRequested(commentType: string)

    // --- Public API  ---

    function onKeyPressed(key, modifiers, isAutoRepeat: bool): void {
        const plainPress = !isAutoRepeat && modifiers === Qt.NoModifier;

        if (plainPress && key === Qt.Key_E) {
            openNewCommentMenuRequested();
            return;
        }
        if (plainPress && key === Qt.Key_F) {
            toggleFullScreenRequested();
            return;
        }
        if (_isPreventReachingMpvCustomCommand(key, modifiers)) {
            return;
        }
        _handleMpvCustomCommand(key, modifiers);
    }

    function requestDisableFullScreen(): void {
        disableFullScreenRequested();
    }

    function requestToggleFullScreen(): void {
        toggleFullScreenRequested();
    }

    function requestResizeAppWindow(width, height): void {
        appWindowSizeRequested(width, height);
    }

    function pausePlayer(): void {
        mpvqcMpvPlayerPyObject.pause();
    }

    function addNewEmptyComment(commentType): void {
        addNewCommentRequested(commentType);
    }

    function preferredSplitSizes(splitViewWidth, splitViewHeight) {
        return {
            width: Math.round(splitViewWidth * defaultSplitRatio),
            height: Math.round(splitViewHeight * defaultSplitRatio)
        };
    }

    // --- Private helpers ---

    function _isPreventReachingMpvCustomCommand(key, modifiers): bool {
        const noModifier = modifiers === Qt.NoModifier;
        const ctrlModifier = (modifiers & Qt.ControlModifier) !== 0;

        return key === Qt.Key_Up  //
        || key === Qt.Key_Down //
        || (key === Qt.Key_Return && noModifier) //
        || (key === Qt.Key_Escape && noModifier) //
        || (key === Qt.Key_Delete && noModifier) //
        || (key === Qt.Key_Backspace && noModifier) //
        || (key === Qt.Key_F && ctrlModifier) //
        || (key === Qt.Key_C && ctrlModifier) //
        || (key === Qt.Key_Z && ctrlModifier);
    }

    function _handleMpvCustomCommand(key, modifiers): void {
        mpvqcMpvPlayerPyObject.handle_key_event(key, modifiers);
    }
}
