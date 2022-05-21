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


import { formatTimeToString } from "../helpers/MpvqcTimeFormatUtils.mjs";


export class DocumentBuilder {

    constructor() {
        this.lines = []
        this.comments = 0
    }

    withFileTag() {
        this.lines.push('[FILE]')
        return this
    }

    /**
     * @param date {string}
     */
    withDate(date) {
        this.lines.push(`date      : ${date}`)
        return this
    }

    /**
     * @param generator {string}
     */
    withGenerator(generator) {
        this.lines.push(`generator : ${generator}`)
        return this
    }

    /** @param nickname {string} */
    withNickname(nickname) {
        this.lines.push(`nick      : ${nickname}`)
        return this
    }

    /** @param filePath {string} */
    withFilePath(filePath) {
        this.lines.push(`path      : ${filePath}`)
        return this
    }

    withBlankLine() {
        this.lines.push('')
        return this
    }

    withDataTag() {
        this.lines.push('[DATA]')
        return this
    }

    /** @param comments {Array<MpvqcComment>} */
    withComments(comments) {
        this.comments += comments.length
        for (const comment of comments) {
            const time = formatTimeToString(comment.time)
            // noinspection JSUnresolvedFunction
            const commentType = qsTranslate("CommentTypes", comment.commentType)
            this.lines.push(`[${time}] [${commentType}] ${comment.comment}`)
        }
        return this
    }

    withCommentSummary() {
        this.lines.push(`# total lines: ${this.comments}`)
        return this
    }

    build() {
        return this.lines.join('\n')
    }

}


