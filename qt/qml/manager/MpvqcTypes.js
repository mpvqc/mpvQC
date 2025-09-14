// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

/**
 * @typedef {Object} Delta
 * @property {Array<{
 *   url: url,
 *   videoUrl: url|null,
 *   videoExists: boolean
 * }>} documentsValid - List of valid documents with optional video reference
 * @property {string[]} documentsInvalid - List of invalid absolute document paths
 * @property {url[]} videos - Encoded video URLs
 * @property {url[]} subtitles - Encoded subtitle URLs
 */

/**
 * @typedef {Object} ImportChange
 * @property {string[] | undefined} documents
 * @property {string | null | undefined} video
 */

/**
 * @typedef {"initial" | "other"} StateKind
 */

/**
 * @typedef {Object} ApplicationState
 * @property {StateKind} kind
 * @property {string | null} document
 * @property {string | null} video
 * @property {boolean} saved
 */

/**
 * @callback VideoEquals
 * @param {string | null} a
 * @param {string | null} b
 * @returns {boolean}
 */

/**
 * @typedef {Object} ReducerOptions
 * @property {VideoEquals=} videoEquals
 */

/**
 * @typedef {Object} ImportEvent
 * @property {"IMPORT"} type
 * @property {ImportChange} change
 */

/**
 * @typedef {Object} SaveEvent
 * @property {"SAVE"} type
 * @property {string} document
 */

/**
 * @typedef {{ type: "CHANGE" } | { type: "RESET" } | ImportEvent | SaveEvent} Event
 */
