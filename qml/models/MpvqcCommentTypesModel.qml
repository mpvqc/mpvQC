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


ListModel {
    readonly property var forTranslationTool: [
        qsTranslate('CommentTypes', 'Translation'),
        qsTranslate('CommentTypes', 'Spelling'),
        qsTranslate('CommentTypes', 'Punctuation'),
        qsTranslate('CommentTypes', 'Phrasing'),
        qsTranslate('CommentTypes', 'Timing'),
        qsTranslate('CommentTypes', 'Typeset'),
        qsTranslate('CommentTypes', 'Note'),
    ]

    ListElement {
        type: 'Translation'
    }
    ListElement {
        type: 'Spelling'
    }
    ListElement {
        type: 'Punctuation'
    }
    ListElement {
        type: 'Phrasing'
    }
    ListElement {
        type: 'Timing'
    }
    ListElement {
        type: 'Typeset'
    }
    ListElement {
        type: 'Note'
    }

    function items(): Array<string> {
        const marshalled = []
        for (let i = 0; i < count; i++) {
            const item = obtain(i)
            marshalled.push(item)
        }
        return marshalled
    }

    function add(commentType: string): void {
        this.append({ type: commentType })
    }

    function replace(index: int, commentType: string): void {
        this.set(index, { type: commentType })
    }

    function obtain(index: int): string {
        return this.get(index)?.type
    }

    function copy(parent: any): MpvqcCommentTypesModel {
        const copy = Qt.createQmlObject('import models; MpvqcCommentTypesModel {}', parent)
        copy.clear()
        for (let i = 0; i < this.count; i++) {
            const item = obtain(i)
            copy.add(item)
        }
        return copy
    }

    function replaceWith(commentTypes: Array<string>): void {
        this.clear()
        for (const commentType of commentTypes) {
            this.add(commentType)
        }
    }

    function reset(parent: any): void {
        const cleanOne = Qt.createQmlObject('import models; MpvqcCommentTypesModel {}', parent)
        const items = cleanOne.items()
        this.clear()
        this.replaceWith(items)
    }

}
