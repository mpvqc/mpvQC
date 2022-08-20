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


QtObject {
    property var timeFormatFunc: MpvqcTimeFormatUtils.extractSecondsFrom
    property var reverseLookupFunc: MpvqcCommentTypeReverseTranslator.lookup
    property var fileReaderFunc: FileReader.read
    property var pathToUrlFunc: FileIoPyObject.url_from_file
    property var importer: new FileImporter.Importer(timeFormatFunc, reverseLookupFunc, fileReaderFunc, pathToUrlFunc)

    signal commentsImported(var comments)
    signal videosImported(var videos)
    signal documentsRejected(var errors)

    function importIncludingVideoFrom(documents) {
        const report = importer.importFrom(documents)
        _handleComments(report.comments)
        _handleVideos(report.videos)
        _handleErrors(report.errors)
    }

    function _handleComments(comments) {
        if (comments.length > 0) {
            commentsImported(comments)
        }
    }

    function _handleVideos(videos) {
        if (videos.length > 0) {
            videosImported(videos)
        }
    }

    function _handleErrors(errors) {
        if (errors.length > 0) {
            documentsRejected(errors)
        }
    }

}
