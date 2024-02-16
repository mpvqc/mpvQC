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

import "MpvqcDocumentFileImporter.js" as MpvqcDocumentFileImporter
import "MpvqcFileReader.js" as MpvqcFileReader
import "MpvqcStateChanges.js" as MpvqcStateChanges


QtObject {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcTimeFormatUtils: mpvqcApplication.mpvqcTimeFormatUtils
    readonly property var mpvqcReverseTranslatorPyObject: mpvqcApplication.mpvqcReverseTranslatorPyObject

    property var fileImporter: QtObject {
        property var timeFormatFunc: root.mpvqcTimeFormatUtils.extractSecondsFrom
        property var reverseLookupFunc: root.mpvqcReverseTranslatorPyObject.lookup
        property var fileReaderFunc: MpvqcFileReader.read
        property var importer: new MpvqcDocumentFileImporter.Importer(timeFormatFunc, reverseLookupFunc, fileReaderFunc)

        /**
         * @param documents
         * @returns {MpvqcImport}
         */
        function importFrom(documents: list<url>): int {
            return importer.importFrom(documents)
        }
    }

    property var videoSelector: MpvqcVideoSelector {
        property var report
        property var subtitles

        mpvqcApplication: root.mpvqcApplication

        onVideoSelected: (video) => {
            root.continueImportProcessingWith(report, video, subtitles)
        }
    }

    signal commentsImported(var comments)
    signal videoImported(url video)
    signal subtitlesImported(var subtitles)
    signal stateChanged(var change)
    signal erroneousDocumentsImported(var documents)

    function importFrom(documents: list<url>, standaloneVideo: url, subtitles: list<url>): void {
        const report = fileImporter.importFrom(documents)
        handleImport(report, standaloneVideo, subtitles)
    }

    /**
     * @param report {MpvqcImport}
     * @param standaloneVideo
     * @param subtitles
     */
    function handleImport(report, standaloneVideo: url, subtitles: list<url>): void {
        const possiblyLinkedVideosInDocument = report.successful
        videoSelector.report = report
        videoSelector.subtitles = subtitles
        videoSelector.chooseBetween(standaloneVideo, possiblyLinkedVideosInDocument)
    }

    /**
     *
     * @param report {MpvqcImport}
     * @param video
     * @param subtitles
     */
    function continueImportProcessingWith(report, video: url, subtitles: list<url>): void {
        const validDocuments = report.successful.map(document => document.url)
        const erroneousDocuments = report.errors.map(document => document.url)
        const change = new MpvqcStateChanges.ImportChanges(validDocuments, video)
        _fireCommentsImported(report.comments)
        _fireVideoImported(video)
        _fireSubtitlesImported(subtitles)
        _fireStateChange(change)
        _fireErroneousDocumentsImported(erroneousDocuments)
    }

    /**
     * @param comments {Array<MpvqcComment>}
     * @private
     */
    function _fireCommentsImported(comments): void {
        if (comments.length > 0) {
            commentsImported(comments)
        }
    }

    function _fireVideoImported(video: url): void {
        if (video && video != '') {
            videoImported(video)
        }
    }

    function _fireSubtitlesImported(subtitles: list<url>): void {
        if (subtitles.length > 0) {
            subtitlesImported(subtitles)
        }
    }

    function _fireErroneousDocumentsImported(documents: list<url>): void {
        if (documents.length > 0) {
            erroneousDocumentsImported(documents)
        }
    }

    /**
     * @param change {MpvqcStateChanges.ImportChanges}
     * @private
     */
    function _fireStateChange(change): void {
        if (change.documents.length > 0 || (change.video && change.video != '')) {
            stateChanged(change)
        }
    }

}
