/*
mpvQC

Copyright (C) 2024 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

pragma ComponentBehavior: Bound

import QtQuick

import pyobjects

import "../dialogs"

MpvqcManagerPyObject {
    id: root

    required property var mpvqcApplication
    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    readonly property var mpvqcCommentTable: mpvqcApplication.mpvqcCommentTable

    readonly property Timer backupTimer: Timer {
        repeat: true
        interval: Math.max(15, root.mpvqcSettings.backupInterval) * 1000
        running: root.mpvqcSettings.backupEnabled && mpvqcCommentTable.commentCount > 0

        onTriggered: {
            root.backup_impl();
        }
    }

    property var mpvqcDialogExportDocumentFactory: Component {
        MpvqcDialogExportDocument {}
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

    function reset(): void {
        root.reset_impl();
    }

    function openDocuments(documents: list<url>): void {
        root.open_documents_impl(documents);
    }

    function openVideo(video: url): void {
        root.open_video_impl(video);
    }

    function openSubtitles(subtitles: list<url>): void {
        root.open_subtitles_impl(subtitles);
    }

    function open(documents: list<url>, videos: list<url>, subtitles: list<url>): void {
        root.open_impl(documents, videos, subtitles);
    }

    function save(): void {
        root.save_impl();
    }

    function saveAs(): void {
        root.save_as_impl();
    }
}
