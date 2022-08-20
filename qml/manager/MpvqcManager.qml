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
    property alias currentDocument: exporter.currentDocument
    property alias currentVideo:  exporter.currentVideo
    property alias saved: state.saved

    signal commentsImported(var comments)
    signal videoImported(url video)
    signal subtitlesImported(var subtitles)

    MpvqcState {
        id: state
    }

    MpvqcImporter {
        id: documentImporter

        onCommentsImported: (comments) => {
            manager.commentsImported(comments)
        }

        onVideosImported: (videos) => {
            _openFirstExistingVideoOf(videos)
        }

        onDocumentsRejected: (errors) => {
            console.log('Import errors:', JSON.stringify(errors))
        }
    }

    MpvqcExporter {
        id: exporter

        onSaved: {
            state.transitionToSaved()
        }
    }

    function openDocuments(documents) {
        documentImporter.importIncludingVideoFrom(documents)
    }

    function openSubtitles(subtitles) {
        subtitlesImported(subtitles)
    }

    function openVideo(url) {
        manager.videoImported(url)
    }

    function requestSave() {
        exporter.requestSave()
    }

    function requestSaveAs() {
        exporter.requestSaveAs()
    }

    function _openFirstExistingVideoOf(videoUrls) {
        for (const video of videoUrls) {
            if (FileIoPyObject.is_existing_file(video)) {
                manager.openVideo(video)
                break
            }
        }
    }

    Connections {
        target: playerProperties

        function onPathChanged(path) {
            currentVideo = FileIoPyObject.url_from_file(path)
            state.transitionToUnsaved()
        }
    }

}
