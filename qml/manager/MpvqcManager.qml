/*
mpvQC

Copyright (C) 2022 mpvQC developers

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

import QtQuick

import dialogs


Item {
    id: root

    required property var mpvqcApplication

    property var mpv: mpvqcApplication.mpvqcMpvPlayerPyObject
    property var mpvqcCommentTable: mpvqcApplication.mpvqcCommentTable

    property alias saved: state.saved

    function reset(): void {
        resetter.requestReset()
    }

    function openDocuments(documents: list<url>): void {
        const video = ''
        const subtitles = []
        _open(documents, video, subtitles)
    }

    function openVideo(video: url): void {
        const documents = []
        const subtitles = []
        _open(documents, video, subtitles)
    }

    function openSubtitles(subtitles: list<url>): void {
        const documents = []
        const video = ''
        _open(documents, video, subtitles)
    }

    function open(documents: list<url>, video: url, subtitles: list<url>): void {
        const docs = documents && documents.length > 0 ? documents : []
        const vid = video && video != '' ? video : ''
        const subs = subtitles && subtitles.length > 0 ? subtitles : []
        _open(docs, vid, subs)
    }

    function _open(documents: list<url>, video: url, subtitles: list<url>): void {
        importer.importFrom(documents, video, subtitles)
    }

    function save(): void {
        exporter.requestSave()
    }

    function saveAs(): void {
        exporter.requestSaveAs()
    }

    MpvqcBackupper {
        id: backupper

        video: state.video
        mpvqcApplication: root.mpvqcApplication
    }

    MpvqcExporter {
        id: exporter

        video: state.video
        document: state.document
        mpvqcApplication: root.mpvqcApplication

        onSaved: (newDocumentUrl) => {
            state.handleSave(newDocumentUrl)
        }
    }

    MpvqcImporter {
        id: importer

        property var factory: Component {
            MpvqcMessageBoxDocumentNotCompatible {
                mpvqcApplication: root.mpvqcApplication
            }
        }

        mpvqcApplication: root.mpvqcApplication

        onCommentsImported: (comments) => {
            root.mpvqcCommentTable.importComments(comments)
        }

        onVideoImported: (video) => {
            root.mpv.open_video(video)
        }

        onSubtitlesImported: (subtitles) => {
            root.mpv.open_subtitles(subtitles)
        }

        onStateChanged: (change) => {
            state.handleImport(change)
        }

        onErroneousDocumentsImported: (documents) => {
            const dialog = factory.createObject(root)
            dialog.closed.connect(dialog.destroy)
            dialog.renderErroneous(documents)
            dialog.open()
        }

    }

    MpvqcResetter {
        id: resetter

        mpvqcApplication: root.mpvqcApplication
        saved: state.saved

        onReset: {
            root.mpvqcCommentTable.clearComments()
            state.handleReset()
        }
    }

    MpvqcState {
        id: state
    }

    Connections {
        target: root.mpvqcCommentTable

        function onCommentsChanged() {
            state.handleChange()
        }
    }

}
