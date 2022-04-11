// noinspection JSUnusedGlobalSymbols

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


class EventRegistry {

    constructor() {
        this.listeners = new Map()
    }

    register(eventKey, callableFunction) {
        const listeners = this.listeners.get(eventKey);
        if (listeners) {
            listeners.push(callableFunction)
        } else {
            this.listeners.set(eventKey, Array.of(callableFunction))
        }
    }

    call(eventKey, args) {
        const callableFunctions = this.listeners.get(eventKey)
        if (callableFunctions) {
            for (let callableFunction of callableFunctions) {
                callableFunction(args)
            }
        }
    }
}

const registry = new EventRegistry()

/**
 * Adds a callableFunction for the eventKey.
 * @param eventKey {string}
 * @param callableFunction {function}
 */
function register(eventKey, callableFunction) {
    registry.register(eventKey, callableFunction)
}

/**
 * Calls all functions that have been registered for the given eventKey.
 * @param eventKey {string}
 * @param args
 */
function produce(eventKey, args) {
    registry.call(eventKey, args)
}


/**
 * Called with no arguments
 */
const EventRequestNewComment = 'mpvqc-request-new-comment'

/**
 * Called with following args:
 * - commentType: string    untranslated new comment type to add
 */
const EventAddNewComment = 'mpvqc-add-new-comment'
