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


// noinspection JSUnusedGlobalSymbols
class Importer {

    /**
     * @param secondsExtractorFunc {mpvqcSecondsExtractorFunc}
     * @param reverseTranslatorLookupFunc {mpvqcCommentTypeTranslatorReverseLookupFunc}
     * @param fileReaderFunc {mpvqcFileReaderFunc}
     * @param pathToUrlFunc {mpvqcPathToUrlFunc}
     */
    constructor(
        secondsExtractorFunc,
        reverseTranslatorLookupFunc,
        fileReaderFunc,
        pathToUrlFunc
    ) {
        this.fileImporter = new DocumentFileImporter(secondsExtractorFunc, reverseTranslatorLookupFunc, fileReaderFunc)
        this.pathToUrlFunc = pathToUrlFunc
    }

    /**
     * @param urls {Array<QUrl>}
     * @return {MpvqcImport}
     */
    importFrom(urls) {
        const report = this.fileImporter.importFrom(urls)
        const comments = this._combineComments(report)
        const videos = this._extractVideos(report)
        const errors = report.errors
        return { comments, videos, errors }
    }

    /**
     * @param report {MpvqcImportReport}
     * @return {Array<MpvqcComment>}
     */
    _combineComments(report) {
        const comments = []
        for (const document of report.imports) {
            comments.push(...document.comments)
        }
        return comments
    }

    /**
     * @param report {MpvqcImportReport}
     * @return {Array<string>}
     */
    _extractVideos(report) {
        const videos = []
        for (const document of report.imports) {
            const video = document.video
            if (video) {
                const url = this.pathToUrlFunc(video)
                videos.push(url)
            }
        }
        return videos
    }

}


class DocumentFileImporter {

    /**
     * @param secondsExtractorFunc {mpvqcSecondsExtractorFunc}
     * @param reverseTranslatorLookupFunc {mpvqcCommentTypeTranslatorReverseLookupFunc}
     * @param fileReaderFunc {mpvqcFileReaderFunc}
     */
    constructor(secondsExtractorFunc, reverseTranslatorLookupFunc, fileReaderFunc) {
        this.secondsExtractorFunc = secondsExtractorFunc
        this.reverseTranslatorLookupFunc = reverseTranslatorLookupFunc
        this.fileReaderFunc = fileReaderFunc
    }

    /**
     * @param urls {Array<QUrl>}
     * @return {MpvqcImportReport}
     */
    importFrom(urls) {
        const errors = [], imports = []
        for (const url of urls) {
            const readReport = this._read(url)
            if (readReport.error) {
                errors.push({ url, message: readReport.error })
            } else {
                const { comments, video } = this._extractFrom(readReport.textContent)
                imports.push({ url, video, comments })
            }
        }
        return { errors, imports }
    }

    /**
     * @param url {QUrl}
     * @return {MpvqcDocumentReaderResult}
     */
    _read(url) {
        const reader = new DocumentReader(this.fileReaderFunc)
        return reader.read(url)
    }

    /**
     *
     * @param textContent {string}
     * @return {{ comments: Array<MpvqcComment>, video: string }}
     */
    _extractFrom(textContent) {
        const extractor = new QcContentExtractor(this.secondsExtractorFunc, this.reverseTranslatorLookupFunc)
        extractor.extract(textContent)
        return { comments: extractor.comments, video: extractor.video }
    }

}


class DocumentReader {

    /** @param mpvqcFileReaderFunc {mpvqcFileReaderFunc} */
    constructor(mpvqcFileReaderFunc) {
        this.fileReaderFunc = mpvqcFileReaderFunc
    }

    /**
     * @param url {QUrl}
     * @return {MpvqcDocumentReaderResult}
     */
    read(url) {
        const textContent = this._read(url)
        if (this._startsNotWithFileTag(textContent)) {
            const error = qsTranslate('DocumentImport', "Document is not a valid quality check report")
            return { error }
        }
        return { textContent }
    }

    /**
     * @param url {QUrl}
     * @return {string} fileContent
     */
    _read(url) {
        return this.fileReaderFunc(url)
    }

    /**
     * @param textContent {string}
     * @return {boolean}
     */
    _startsNotWithFileTag(textContent) {
        return !this._startsWithFileTag(textContent)
    }

    /**
     * @param textContent {string}
     * @return {boolean}
     */
    _startsWithFileTag(textContent) {
        return textContent.trim().startsWith('[FILE]')
    }

}


const lineBreakRegex = /\r?\n/
const videoRegex = /^path\s*:\s*(.*?)\s*$/
const commentRegex = /^\[(\d{2}:\d{2}:\d{2})]\s*\[([^\[\]]+)]\s*(.*?)$/


class QcContentExtractor {

    /**
     * @param secondsExtractorFunc {mpvqcSecondsExtractorFunc}
     * @param reverseTranslatorLookupFunc {mpvqcCommentTypeTranslatorReverseLookupFunc}
     */
    constructor(secondsExtractorFunc, reverseTranslatorLookupFunc) {
        this.secondsExtractorFunc = secondsExtractorFunc
        this.reverseTranslatorLookupFunc = reverseTranslatorLookupFunc
        this.comments = []
        this.video = ''
    }

    extract(content) {
        const lines = content.trim().split(lineBreakRegex).filter(line => line)
        for (const line of lines) {
            if (!this.video) {
                this._extractVideo(line)
            }
            this._extractComment(line)
        }
    }

    /** @param line {string} */
    _extractVideo(line) {
        const match = videoRegex.exec(line)
        if (match) {
            this.video = match[1].trim()
        }
    }

    /** @param line {string} */
    _extractComment(line) {
        const match = commentRegex.exec(line)
        if (match) {
            const time = this.secondsExtractorFunc(match[1])
            const commentType = this.reverseTranslatorLookupFunc(match[2])
            const comment = match[3].trim()
            this.comments.push({ time, commentType, comment })
        }
    }

}
