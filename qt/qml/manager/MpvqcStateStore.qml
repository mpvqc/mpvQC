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

pragma Singleton

import QtQuick

import "MpvqcStateReducer.js" as MpvqcStateReducer

QtObject {
    property var state: MpvqcStateReducer.initialState(null)

    function processImport(documents: list<url>, video: url): void {
        _dispatch({
            type: "IMPORT",
            change: {
                documents: documents,
                video: video
            }
        });
    }

    function processChange(): void {
        _dispatch({
            type: "CHANGE"
        });
    }

    function processSave(document: url): void {
        _dispatch({
            type: "SAVE",
            document: document
        });
    }

    function processReset(): void {
        _dispatch({
            type: "RESET"
        });
    }

    // todo use a private QtObject to encapsulate "private" methods

    function _dispatch(event): void {
        const next = MpvqcStateReducer.reducer(state, event, {
            videoEquals: _videoEquals
        });
        if (next.kind !== state.kind || next.document !== state.document || next.video !== state.video || next.saved !== state.saved) {
            state = next;
        }
    }

    // todo remove? if not required
    function _videoEquals(a: url, b: url): bool {
        console.log("url a", typeof (a), a, "url b", typeof (b), b);
        return a === b;
    }
}
