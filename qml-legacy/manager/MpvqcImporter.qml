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
import "MpvqcDocumentFileImporter.js" as FileImporter
import "MpvqcFileReader.js" as FileReader
import "MpvqcStateChanges.js" as MpvqcStateChanges


Item {

    signal commentsImported(var comments)
    signal videoImported(url video)
    signal subtitlesImported(var subtitles)
    signal stateChange(var change)
    signal erroneousDocumentsImported(var documents)

    QtObject {
        id: fileImporter
        property var timeFormatFunc: MpvqcTimeFormatUtils.extractSecondsFrom
        property var reverseLookupFunc: MpvqcCommentTypeReverseTranslator.lookup
        property var fileReaderFunc: FileReader.read
        property var importer: new FileImporter.Importer(timeFormatFunc, reverseLookupFunc, fileReaderFunc)

        function importFrom(documents) {
            return importer.importFrom(documents)
        }
    }

    function importFrom(documents, standaloneVideo, subtitles) {
        const importReport = fileImporter.importFrom(documents)
        const linkedVideo = _findFirstExistingVideoFrom(importReport.successful)
        const validDocuments = _extractUrlsFrom(importReport.successful)
        const erroneousDocuments = _extractUrlsFrom(importReport.errors)
        const newVideo = standaloneVideo || linkedVideo
        const change = new MpvqcStateChanges.ImportChanges(validDocuments, newVideo)
        _fireCommentsImported(importReport.comments)
        _fireVideoImported(newVideo)
        _fireSubtitlesImported(subtitles)
        _fireStateChange(change)
        _fireErroneousDocumentsImported(erroneousDocuments)
    }

    function _findFirstExistingVideoFrom(documents) {
        for (const document of documents) {
            const video = document.video
            const url = FileIoPyObject.url_from_file(video)
            if (FileIoPyObject.is_existing_file(url)) {
                return url
            }
        }
        return ''
    }

    function _extractUrlsFrom(documents) {
        const urls = []
        for (const document of documents) {
            urls.push(document.url)
        }
        return urls
    }

    function _fireCommentsImported(comments) {
        if (comments.length > 0) {
            commentsImported(comments)
        }
    }

    function _fireVideoImported(video) {
        if (video) {
            videoImported(video)
        }
    }

    function _fireSubtitlesImported(subtitles) {
        if (subtitles.length > 0) {
            subtitlesImported(subtitles)
        }
    }

    function _fireErroneousDocumentsImported(documents) {
        if (documents.length > 0) {
            erroneousDocumentsImported(documents)
        }
    }

    function _fireStateChange(change) {
        if (change.documents.length > 0 || change.video) {
            stateChange(change)
        }
    }

}
