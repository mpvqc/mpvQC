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


class MpvqcEventRegistry {

    constructor() {
        this.listeners = new Map()
    }

    subscribe(eventKey, callableFunction) {
        const listeners = this.listeners.get(eventKey)
        if (listeners) {
            listeners.push(callableFunction)
        } else {
            this.listeners.set(eventKey, Array.of(callableFunction))
        }
    }

    produce(eventKey, args) {
        const callableFunctions = this.listeners.get(eventKey)
        if (callableFunctions) {
            for (let callableFunction of callableFunctions) {
                callableFunction(args)
            }
        }
    }
}


const registry = new MpvqcEventRegistry()


/**
 * Adds a callableFunction for the eventKey
 * @param eventKey {string}
 * @param callableFunction {function}
 */
function subscribe(eventKey, callableFunction) {
    registry.subscribe(eventKey, callableFunction)
}


/**
 * Calls all functions that have been registered for the given eventKey
 * @param eventKey {string}
 * @param args
 */
function produce(eventKey, args) {
    registry.produce(eventKey, args)
}


/**
 * Called with no arguments
 */
const EventRequestVideoPause = 'mpvqc-request-video-pause'


/**
 * Called with no arguments
 */
const EventRequestNewRow = 'mpvqc-request-new-row'


/**
 * Called with following args:
 * - commentType: string    untranslated new comment type to add
 */
const EventAddNewRow = 'mpvqc-add-new-row'


/**
 * Called with following args:
 * - time: int      the seconds since the beginning to jump to
 */
const EventJumpToVideoPosition = 'mpvqc-jump-to-video-position'


/**
 * Called with no arguments
 */
const EventFocusTable = 'mpvqc-focus-table'


/**
 * Called with following args:
 * - time: string      the custom command
 */
const EventCustomPlayerCommand = 'mpvqc-custom-player-command'


/**
 * Called with no arguments
 */
const EventEditCurrentlySelectedComment = 'mpvqc-edit-currently-selected-comment'


/**
 * Called with following args:
 * - url: QUrl      the url of the video
 */
const EventRequestOpenVideo = 'mpvqc-request-open-video'


/**
 * Called with following args:
 * - comments: Array<{time: number, commentType: string, comment: string}>
 */
const EventImportComments = 'mpvqc-import-comments'


/**
 * Called with following args:
 * - selected index (0 based)
 */
const EventCommentsSelectedIndexChanged = 'mpvqc-comments-selected-index-changed'


/**
 * Called with following args:
 * - count: total number of comments
 */
const EventCommentsCountChanged = 'mpvqc-comments-count-changed'