/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick
import helpers
import "MpvqcDocumentImporter.js" as MpvqcDocumentImporter


Item {
    id: state

    property alias commentModel: exporter.commentModel
    property alias currentDocument: exporter.currentDocument
    property url currentVideo: ''

    function openDocuments(documents) {
        const report = MpvqcDocumentImporter.importFrom(documents)
        const commentsListOfComments = report.imports.map(value => value.comments)
        const commentsFlat = [].concat.apply([], commentsListOfComments)
        eventRegistry.produce(eventRegistry.EventImportComments, commentsFlat)
    }

    function openSubtitles(subtitles) {
        for (let file of subtitles) {
            console.log("Open sub: " + file)
        }
    }

    function openVideo(url) {
        eventRegistry.produce(eventRegistry.EventRequestOpenVideo, url)
        state.currentVideo = url // todo use mpv property to get current video
    }

    MpvqcExporter {
        id: exporter
        currentVideo: state.currentVideo
    }

    function requestSave() {
        exporter.requestSave()
    }

    function requestSaveAs() {
        exporter.requestSaveAs()
    }

}
