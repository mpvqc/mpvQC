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


/**
 @typedef MpvqcExportData
 @type {Object}
 @property {string} date
 @property {string} generator
 @property {string} nickname
 @property {string} videoPath
 @property {Array<MpvqcComment>} comments
 */

/**
 @typedef MpvqcExportSettings
 @type {Object}
 @property {boolean} writeHeaderDate
 @property {boolean} writeHeaderGenerator
 @property {boolean} writeHeaderNickname
 @property {boolean} writeHeaderVideoPath
 */

/**
 @typedef MpvqcComment
 @type {Object}
 @property {number} time
 @property {string} commentType
 @property {string} comment
 */

/**
 @typedef MpvqcImport
 @type {Object}
 @property {Array<MpvqcComment>} comments
 @property {Array<string>?} videos
 @property {Array<MpvqcImportError>} errors
 */

/**
 @typedef MpvqcImportReport
 @type {Object}
 @property {Array<MpvqcImportError>} errors
 @property {Array<MpvqcImportSuccess>} imports
 */

/**
 @typedef MpvqcImportSuccess
 @type {Object}
 @property {QUrl} url
 @property {string} video
 @property {MpvqcComment} comments
 */

/**
 @typedef MpvqcImportError
 @type {Object}
 @property {QUrl} url
 */

/**
 @typedef MpvqcDocumentReaderResult
 @type {Object}
 @property {string?} error
 @property {string?} textContent
 */

/**
 @typedef QUrl
 @type {Class}
 */

/**
 * @name mpvqcTimeFormatFunc
 * @type function
 * @param {number} seconds
 * @return {string}
 */

/**
 * @name mpvqcNicknameGetterFunc
 * @type function
 * @return {string}
 */

/**
 * @name mpvqcAbsPathGetterFunc
 * @type function
 * @param {QUrl} url
 * @return {string}
 */

/**
 * @name mpvqcCommentGetterFunc
 * @type function
 * @return {Array<MpvqcComment>}
 */

/**
 * @name mpvqcPathToUrlFunc
 * @type function
 * @param {string} file path (absolute)
 * @return {url} url
 */

/**
 * @name mpvqcFileReaderFunc
 * @type function
 * @param {url} fileUrl Qt url
 * @return {string} fileContent
 */

/**
 * @name mpvqcSecondsExtractorFunc
 * @type function
 * @param {string} timeString e.g. 00:00:01
 * @return {number} seconds
 */

/**
 * @name mpvqcCommentTypeTranslatorReverseLookupFunc
 * @type function
 * @param {string} commentType
 * @return {string} commentTypeTranslated | commentType
 */

/**
 * @name mpvqcSettingsGetterFunc
 * @type Function
 * @return {Object} settings
 */

/**
 * @name qsTranslate
 * @type function
 * @param {string} context
 * @param {string} translation
 * @return {string} translated | untranslated
 */
