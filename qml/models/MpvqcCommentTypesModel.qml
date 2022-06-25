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


ListModel {
    readonly property var forTranslationTool: [
        qsTranslate("CommentTypes", "Translation"),
        qsTranslate("CommentTypes", "Spelling"),
        qsTranslate("CommentTypes", "Punctuation"),
        qsTranslate("CommentTypes", "Phrasing"),
        qsTranslate("CommentTypes", "Timing"),
        qsTranslate("CommentTypes", "Typeset"),
        qsTranslate("CommentTypes", "Note"),
    ]

    ListElement {
        type: "Translation"
    }
    ListElement {
        type: "Spelling"
    }
    ListElement {
        type: "Punctuation"
    }
    ListElement {
        type: "Phrasing"
    }
    ListElement {
        type: "Timing"
    }
    ListElement {
        type: "Typeset"
    }
    ListElement {
        type: "Note"
    }

    function add(commentType) {
        this.append({ type: commentType })
    }

    function edit(index, commentType) {
        this.setProperty(index, 'type', commentType)
    }

    function asString() {
        return items().join(', ')
    }

    function items() {
        const marshalled = []
        for (let i = 0, count = this.count; i < count; i++) {
            marshalled.push(this.get(i).type)
        }
        return marshalled
    }

    function replaceWith(commaSeparatedStringList) {
        this.clear()
        commaSeparatedStringList
            .split(',')
            .map((value) => value.trim())
            .filter((value) => value)
            .forEach((value) => this.append({ type: value }))
    }

    function copy(qmlParent) {
        const copy = Qt.createQmlObject('import models; MpvqcCommentTypesModel {}', qmlParent)
        copy.clear()
        for (let i = 0, count = this.count; i < count; i++) {
            copy.append(this.get(i))
        }
        return copy
    }

    function reset(qmlParent) {
        const copy = Qt.createQmlObject('import models; MpvqcCommentTypesModel {}', qmlParent)
        this.clear()
        for (let i = 0, count = copy.count; i < count; i++) {
            this.append(copy.get(i))
        }
        copy.destroy()
    }

}
