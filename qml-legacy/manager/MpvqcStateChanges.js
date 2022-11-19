// noinspection JSUnusedGlobalSymbols

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


const NO_VIDEO = ''
const NO_DOCUMENT = ''
const SAVED = true
const UNSAVED = false


class ImportChanges {

    /**
     * @param documents {Array<QUrl>}
     * @param video {QUrl}
     */
    constructor(documents, video) {
        this.documents = documents
        this.video = video || ''
    }

    get isOnlyVideoImported() {
        return this.video && this.documents.length === 0
    }

    get isExactlyOneDocumentImported() {
        return this.documents.length === 1
    }

    get thatImportedDocument() {
        return this.documents[0]
    }
}


class ApplicationState {

    /**
     * @param video {QUrl}
     * @param document {QUrl}
     * @param saved {boolean}
     */
    constructor(video, document, saved) {
        this.video = video
        this.document = document
        this.saved = saved
    }

    /** @param change {ImportChanges} */
    findVideo(change) {
        return change.video ? change.video : this.video
    }

    /**
     * @param document {QUrl}
     * @returns ApplicationState
     */
    handleSave(document) {
        return new OtherState(this.video, document, SAVED)
    }

    /**
     * @param change {ImportChanges}
     * @returns ApplicationState
     */
    handleImport(change) {
        throw new Error('not implemented')
    }

    /** @returns ApplicationState */
    handleChange() {
        return new OtherState(this.video, this.document, UNSAVED)
    }

    /** @returns ApplicationState */
    handleReset() {
        return new InitialState(this.video)
    }

}


class InitialState extends ApplicationState {

    constructor(video) {
        super(video || NO_VIDEO, NO_DOCUMENT, SAVED)
    }

    handleImport(change) {
        if (change.isOnlyVideoImported)
            return new InitialState(change.video, NO_DOCUMENT, SAVED)
        const video = this.findVideo(change)
        if (change.isExactlyOneDocumentImported)
            return new OtherState(video, change.thatImportedDocument, SAVED)
        return new OtherState(video, NO_DOCUMENT, UNSAVED)
    }

}


class OtherState extends ApplicationState {

    handleImport(change) {
        if (change.isOnlyVideoImported && this._urlsEqual(this.video, change.video))
            return new OtherState(this.video, this.document, SAVED)
        const video = this.findVideo(change)
        return new OtherState(video, NO_DOCUMENT, UNSAVED)
    }

    /**
     * @param url1 {QUrl}
     * @param url2 {QUrl}
     * @returns boolean
     */
    _urlsEqual(url1, url2) {
        return url1.toString() === url2.toString()
    }

}
