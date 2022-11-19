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


.import helpers as Helpers


class CommentTypeExistsChecker {

    /**
     * @param commentType {string}
     * @param commentTypes {Array<string>}
     */
    constructor(commentType, commentTypes) {
        this.commentType = commentType
        this.commentTypes = commentTypes
    }

    /** @return {boolean} */
    isIncluded() {
        return this.commentTypes.some(commentType => commentType === this.commentType)
    }

    /** @return {boolean} */
    translationExists() {
        const translation = qsTranslate("CommentTypes", this.commentType)
        if (translation === this.commentType) return false
        return this.commentTypes.some(commentType => commentType === translation)
    }

    /** @return {boolean} */
    reverseTranslationExists() {
        const lookup = Helpers.MpvqcCommentTypeReverseTranslator.lookup(this.commentType)
        return (lookup !== this.commentType) && this.commentTypes.some(commentType => commentType === lookup)
    }
}


/**
 * @param commentType {string}
 * @param commentTypes {Array<string>}
 */
function commentTypeIncludedOrExists(commentType, commentTypes) {
    const checker = new CommentTypeExistsChecker(commentType, commentTypes)
    return checker.isIncluded() || checker.translationExists() || checker.reverseTranslationExists()
}


/**
 * @param container {Array<any>}
 * @param items
 */
function remove(container, ...items) {
    return container.filter((value) => !items.includes(value))
}


/**
 * @param input {string}
 */
function includesForbiddenCharacters(input) {
    return /[[\]]/.test(input)
}
