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
import "../settings"

import "MpvqcStateReducer.js" as MpvqcStateReducer

MpvqcObject {
    id: root

    required property int importWhenVideoLinkedInDocument

    readonly property bool saved: _stateManager.state.saved
    readonly property bool isHaveDocument: _stateManager.state.document !== null

    signal linkedVideoFound(delta: var, video: string)
    signal invalidDocumentsImported(documents: list<string>)

    onSavedChanged: {
        console.warn("SAVED", saved);
        console.warn("SAVED _stateManager.state.document", _stateManager.state.document);
    }

    function reset(): void {
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

    function continueAfterVideoSelected(delta: var, video: string): void {
        const videoUrl = video && video.toString() !== "" ? video.toString() : null;
        console.log("Continue after Video Selected", typeof (videoUrl));
        if (videoUrl) {
            console.log("Video !== null -> openVideo", videoUrl);
            _backend.openVideo(videoUrl);
        }
        if (delta.subtitles.length > 0) {
            console.log("Subtitles about to open");
            _backend.openSubtitles(delta.subtitles);
        }
        if (delta.documentsInvalid.length > 0) {
            console.log("invalidDocumentsImported");
            root.invalidDocumentsImported(delta.documentsInvalid);
        }

        const documents = delta.documentsValid.map(document => document.url);
        _stateManager.processImport(documents, videoUrl);
        console.log("Import done!", documents, videoUrl);
    }

    function saveCurrent(): void {
        _backend.performSave(_stateManager.state.document);
    }

    function save(document: string): void {
        _backend.performSave(document);
    }

    MpvqcManagerBackendPyObject { //qmllint disable
        id: _backend

        onImported: delta => _videoSelector.chooseVideoThenContinueWith(delta)

        onSaved: url => _stateManager.processSave(url)

        onChanged: _stateManager.processChange()

        onReset: _stateManager.processReset()
    }

    QtObject {
        id: _stateManager

        property var state: MpvqcStateReducer.initialState(null)

        onStateChanged: {
            console.log("State changed", JSON.stringify(state));
        }

        function processImport(documents: list<string>, video: string): void {
            console.log("processImport", documents, video, video ?? null);
            _dispatch({
                type: "IMPORT",
                change: {
                    documents: documents,
                    video: video ?? null
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
            console.log("processSave", document);
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
            const next = MpvqcStateReducer.reducer(state, event);
            if (next.kind !== state.kind || next.document !== state.document || next.video !== state.video || next.saved !== state.saved) {
                state = next;
            }
        }
    }

    QtObject {
        id: _videoSelector

        /** @param {Delta} delta */
        function chooseVideoThenContinueWith(delta): void {
            console.log("chooseVideoThenContinueWith", JSON.stringify(delta), JSON.stringify(delta.videos));
            if (delta.videos.length > 0) {
                console.log("delta.videos.length > 0");
                root.continueAfterVideoSelected(delta, delta.videos[0]);
                return;
            }
            if (isNeverImportLinkedVideo()) {
                console.log("isNeverImportLinkedVideo");
                root.continueAfterVideoSelected(delta);
                return;
            }
            const firstLinkedVideo = findFirstLinkedVideoIn(delta) ?? null;
            if (firstLinkedVideo == null) {
                console.log("firstLinkedVideo === null");
                root.continueAfterVideoSelected(delta);
                return;
            }
            if (isAlwaysImportLinkedVideo()) {
                console.log("isAlwaysImportLinkedVideo");
                root.continueAfterVideoSelected(delta, firstLinkedVideo);
                return;
            }
            console.log("signal to user to decide");
            root.linkedVideoFound(delta, firstLinkedVideo);
        }

        function isNeverImportLinkedVideo(): bool {
            return root.importWhenVideoLinkedInDocument === MpvqcSettings.ImportWhenVideoLinkedInDocument.NEVER;
        }

        function isAlwaysImportLinkedVideo(): bool {
            return root.importWhenVideoLinkedInDocument === MpvqcSettings.ImportWhenVideoLinkedInDocument.ALWAYS;
        }

        function findFirstLinkedVideoIn(delta: var): string {
            if (delta.documentsValid.length > 0) {
                for (const document of delta.documentsValid) {
                    console.log("Check doc", document, JSON.stringify(document));
                    if (document.videoExists) {
                        console.log("document.videoExists");
                        return document.videoUrl;
                    }
                }
            }
            return null;
        }
    }
}
