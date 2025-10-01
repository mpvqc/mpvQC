// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import pyobjects

import "../filedialogs"
import "../messageboxes"
import "../shared"

MpvqcObject {
    id: root

    required property var mpvqcApplication

    readonly property bool saved: _backend.saved

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
            MpvqcExportDocumentFileDialog {
                isExtendedExport: false
            }
        }

        property var mpvqcMessageBoxVideoFoundFactory: Component {
            MpvqcVideoFoundMessageBox {
                parent: root.mpvqcApplication.contentItem
            }
        }

        property var mpvqcMessageBoxNewDocumentFactory: Component {
            MpvqcNewDocumentMessageBox {
                parent: root.mpvqcApplication.contentItem
            }
        }

        property var mpvqcMessageBoxDocumentNotCompatibleFactory: Component {
            MpvqcDocumentNotCompatibleMessageBox {
                parent: root.mpvqcApplication.contentItem
            }
        }
    }
}
