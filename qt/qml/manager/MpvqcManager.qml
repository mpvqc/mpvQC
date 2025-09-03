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

import pyobjects

import "../shared"

import "MpvqcStateReducer.js" as MpvqcStateReducer

MpvqcObject {
    id: root

    readonly property bool saved: _stateManager.state.saved

    onSavedChanged: {
        console.warn("SAVED", saved);
    }

    function reset(): void {
        // todo check if unsaved changes -> ask or reset immediately
        _backend.performReset();
    }

    function openDocuments(documents: list<url>): void {
        open(documents, [], []);
    }

    function openVideo(video: url): void {
        open([], [video], []);
    }

    function openSubtitles(subtitles: list<url>): void {
        open([], [], subtitles);
    }

    function open(documents: list<url>, videos: list<url>, subtitles: list<url>): void {
        _backend.performImport(documents, videos, subtitles);
    }

    function save(): void {
    // todo
    }

    function saveAs(): void {
    // todo
    }

    MpvqcManagerBackendPyObject { //qmllint disable
        id: _backend

        onImported: delta => {
            console.log("onImported", JSON.stringify(delta));
            // todo video selector
            // notify invalid documents
        }

        onChanged: _stateManager.processChange()

        onReset: _stateManager.processReset()
    }

    QtObject {
        id: _stateManager

        property var state: MpvqcStateReducer.initialState(null)

        function processImport(documents: list<url>, video: url): void {
            console.log("processImport");
            _dispatch({
                type: "IMPORT",
                change: {
                    documents: documents,
                    video: video
                }
            });
        }

        function processChange(): void {
            console.log("processChange");
            _dispatch({
                type: "CHANGE"
            });
        }

        function processSave(document: url): void {
            console.log("processSave");
            _dispatch({
                type: "SAVE",
                document: document
            });
        }

        function processReset(): void {
            console.log("processReset");
            _dispatch({
                type: "RESET"
            });
        }

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
}
