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


.import helpers as Helpers


const lineBreakRegex = /\r?\n/
const videoRegex = /^path\s*:\s*(.*?)\s*$/
const commentRegex = /^\[(\d{2}:\d{2}:\d{2})]\s*\[([^\[\]]+)]\s*(.*?)$/


/** @param content {string} */
function Extractor(content) {
    return {
        comments: [],
        video: '',

        extract() {
            const lines = content.trim().split(lineBreakRegex).filter(line => line)
            for (const line of lines) {
                if (!this.video) {
                    this._extractVideo(line)
                }
                this._extractComment(line)
            }
        },

        /** @param line {string} */
        _extractVideo(line) {
            const match = videoRegex.exec(line)
            if (match) {
                this.video = match[1].trim()
            }
        },

        /** @param line {string} */
        _extractComment(line) {
            const match = commentRegex.exec(line)
            if (match) {
                const time = Helpers.MpvqcTimeFormatUtils.extractSecondsFrom(match[1])
                const commentType = Helpers.MpvqcCommentTypeReverseTranslator.lookup(match[2])
                const comment = match[3].trim()
                this.comments.push({ time, commentType, comment })
            }
        }
    }
}


/**
 * @param url {string}
 * @param textContent {string|undefined}
 */
function Document(url, textContent) {
    return {
        textContent,

        isNotTextFile() {
            return !this.isTextFile()
        },

        isTextFile() {
            return url.toString().endsWith('.txt')
        },

        read() {
            if (!this.textContent) {
                this.textContent = Helpers.MpvqcFileReader.read(url)
            }
        },

        startsNotWithFileTag() {
            return !this.startsWithFileTag()
        },

        startsWithFileTag() {
            return this.textContent.trim().startsWith('[FILE]')
        }
    }
}


/**
 * @param urls {Array<string>} actually Qml urls
 * @return {{
 *      imports: Array<{url: string, video: string, comments: Array<{time: number, commentType: string, comment: string}>}>,
 *      errors: Array<{message: string, url: string}>
 * }}
 */
function importFrom(urls) {
    const report = new ImportReport()
    for (const url of urls) {
        const { error, successful } = _importSingle(url)
        if (error)
            report.errors.push({ url, message: error })
        if (successful)
            report.imports.push({ url, video: successful.video, comments: successful.comments })
    }
    return report
}


/**
 * @return {{
 *  imports: Array<{url: string, video: string, comments: Array<{time: number, commentType: string, comment: string}>}>,
 *  errors: Array<{message: string, url: string}>
 * }}
 */
function ImportReport() {
    return { errors: [], imports: [] }
}


/**
 *
 * @param url {string}
 * @return {{
 *      error: string | undefined,
 *      successful: {
 *          url: string,
 *          video: string,
 *          comments: Array<{time: number, commentType: string, comment: string}>
 *          } | undefined
 * }}
 * @private
 */
function _importSingle(url) {
    const document = new Document(url)
    if (document.isNotTextFile()) {
        return { error: qsTranslate('DocumentImport', 'Document is not a txt file') }
    }
    document.read()
    if (document.startsNotWithFileTag()) {
        return { error: qsTranslate('DocumentImport', "Document is not a valid quality check report") }
    }
    const extractor = new Extractor(document.textContent)
    extractor.extract()
    return { successful: { url, video: extractor.video, comments: extractor.comments } }
}
