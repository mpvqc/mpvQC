/*
 * Copyright (C) 2025 mpvQC developers
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

import QtQuick

QtObject {

    required property var mpvqcMpvPlayerPyObject
    required property var mpvqcManager
    required property var mpvqcExtendedDocumentExporterPyObject
    required property var mpvqcSettings

    // --- Controller configuration / tiny UI-agnostic state ---
    readonly property int minContainerHeight: 200
    readonly property int minContainerWidth: 500
    readonly property real defaultSplitRatio: 0.4

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

    function saveExtendedDocument(documentUrl, templateUrl): void {
        mpvqcExtendedDocumentExporterPyObject.performExport(documentUrl, templateUrl);
    }

    function openDroppedFiles(documents, videos, subtitles): void {
        mpvqcManager.open(documents, videos, subtitles);
    }

    function preferredSplitSizes(splitViewWidth, splitViewHeight) {
        return {
            width: Math.round(splitViewWidth * defaultSplitRatio),
            height: Math.round(splitViewHeight * defaultSplitRatio)
        };
    }

    function resetAppState(): void {
        mpvqcManager.reset();
    }

    function save(): void {
        mpvqcManager.save();
    }

    function saveAs(): void {
        mpvqcManager.saveAs();
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
