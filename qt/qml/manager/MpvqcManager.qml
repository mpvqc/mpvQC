// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import pyobjects

import "../dialogs"
import "../shared"

import "MpvqcStateReducer.js" as MpvqcStateReducer

MpvqcObject {
    id: root

    required property var mpvqcApplication

    readonly property bool saved: _stateManager.state.saved

    function reset(): void {
        _backend.reset_impl();
    }

    function openDocuments(documents: list<url>): void {
        _backend.open_documents_impl(documents);
    }

    function openVideo(video: url): void {
        _backend.open_video_impl(video);
    }

    function openSubtitles(subtitles: list<url>): void {
        _backend.open_subtitles_impl(subtitles);
    }

    function open(documents: list<url>, videos: list<url>, subtitles: list<url>): void {
        _backend.open_impl(documents, videos, subtitles);
    }

    function save(): void {
        _backend.save_impl();
    }

    function saveAs(): void {
        _backend.save_as_impl();
    }

    MpvqcManagerBackendPyObject {
        id: _backend

        property var mpvqcDialogExportDocumentFactory: Component {
            MpvqcDialogExportDocument {
                isExtendedExport: false
            }
        }

        property var mpvqcMessageBoxVideoFoundFactory: Component {
            MpvqcMessageBoxVideoFound {
                mpvqcApplication: root.mpvqcApplication
            }
        }

        property var mpvqcMessageBoxNewDocumentFactory: Component {
            MpvqcMessageBoxNewDocument {
                mpvqcApplication: root.mpvqcApplication
            }
        }

        property var mpvqcMessageBoxDocumentNotCompatibleFactory: Component {
            MpvqcMessageBoxDocumentNotCompatible {
                mpvqcApplication: root.mpvqcApplication
            }
        }

        readonly property bool saved: _stateManager.state.saved
        readonly property string _document: _stateManager.state.document

        onImported: change => {
            const delta = JSON.parse(change);
            _stateManager.processImport(delta.documents, delta.video);
        }

        onChanged: {
            _stateManager.processChange();
        }

        onReset: {
            _stateManager.processReset();
        }

        onSaved: document => {
            _stateManager.processSave(document);
        }
    }

    QtObject {
        id: _stateManager

        property var state: MpvqcStateReducer.initialState(null)

        function processImport(documents: list<string>, video: string): void {
            // Python -> QML conversation is really mean :|
            const isVideoFalsy = `${video}` === 'null' || `${video}` === 'undefined';
            _dispatch({
                type: "IMPORT",
                change: {
                    documents,
                    video: isVideoFalsy ? null : video
                }
            });
        }

        function processChange(): void {
            _dispatch({
                type: "CHANGE"
            });
        }

        function processReset(): void {
            _dispatch({
                type: "RESET"
            });
        }

        function processSave(document: string): void {
            _dispatch({
                type: "SAVE",
                document
            });
        }

        function _dispatch(event): void {
            const next = MpvqcStateReducer.reducer(state, event);
            if (next.kind !== state.kind || next.document !== state.document || next.video !== state.video || next.saved !== state.saved) {
                state = next;
            }
        }
    }
}
