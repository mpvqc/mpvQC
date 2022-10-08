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
import helpers
import pyobjects


Item {
    id: manager
    property alias commentGetterFunc: exporter.commentGetterFunc
    property alias saved: state.saved

    signal commentsImported(var comments)
    signal videoImported(url video)
    signal subtitlesImported(var subtitles)

    MpvqcState {
        id: state
    }

    Connections {
        target: globalEvents

        function onCommentsChanged() {
            state.handleChange()
        }
    }

    MpvqcImporter {
        id: importer

        onCommentsImported: (comments) => {
            manager.commentsImported(comments)
        }

        onVideoImported: (video) => {
            manager.videoImported(video)
        }

        onSubtitlesImported: (subtitles) => {
            console.log(subtitles)
        }

        onStateChange: (change) => {
            state.handleImport(change)
        }
    }

    function openDocuments(documents) {
        const video = ''
        const subtitles = []
        _open(documents, video, subtitles)
    }

    function openVideo(video) {
        const documents = []
        const subtitles = []
        _open(documents, video, subtitles)
    }

    function openSubtitles(subtitles) {
        const documents = []
        const video = ''
        _open(documents, video, subtitles)
    }

    function open(documents, video, subtitles) {
        const docs = documents && documents.length > 0 ? documents : []
        const vid = video && video != '' ? video : ''
        const subs = subtitles && subtitles.length > 0 ? subtitles : []
        _open(docs, vid, subs)
    }

    function _open(documents, video, subtitles) {
        importer.importFrom(documents, video, subtitles)
    }

    MpvqcExporter {
        id: exporter
        video: state.video
        document: state.document

        onSaved: (document) => {
            state.handleSave(document)
        }
    }

    function requestSave() {
        exporter.requestSave()
    }

    function requestSaveAs() {
        exporter.requestSaveAs()
    }

    MpvqcReseter {
        id: reseter
        saved: state.saved

        onReset: {
            globalEvents.requestCommentsReset()
            state.handleReset()
        }
    }

    function requestReset() {
        reseter.requestReset()
    }

}
