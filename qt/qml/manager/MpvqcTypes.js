/*
 * Copyright (C) 2025 mpvQC developers
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

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
