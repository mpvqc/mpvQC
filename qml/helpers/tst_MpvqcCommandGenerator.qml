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


import QtQuick 2.0
import QtTest
import "MpvqcCommandGenerator.js" as TestObject

TestCase {
    name: "MpvqcCommandGenerator"

    function exec(expected, key_, modifiers_) {
        const tag = expected === null ? ` null ` : ` > ${expected} < `
        const key = key_ === null ? 'null' : key_
        const modifiers = modifiers_ === null ? 'null' : modifiers_
        const event = { key, modifiers, text: key_ === null ? '' : key.text }
        const actual = TestObject.generateFrom(event)
        return { expected, actual, tag }
    }

    function test_generate_command_data() {
        return [
            // Special keys
            exec('PGUP', Qt.Key_PageUp),
            exec('HOME', Qt.Key_Home),
            exec('LEFT', Qt.Key_Left),

            // Special keys with modifiers
            exec('shift+SPACE', Qt.Key_Space, Qt.ShiftModifier),
            exec('ctrl+SPACE', Qt.Key_Space, Qt.ControlModifier),
            exec('alt+SPACE', Qt.Key_Space, Qt.AltModifier),
            exec('shift+alt+SPACE', Qt.Key_Space, Qt.AltModifier | Qt.ShiftModifier),
            exec('shift+ctrl+alt+SPACE', Qt.Key_Space, Qt.AltModifier | Qt.ControlModifier | Qt.ShiftModifier),

            // Invalid keys
            exec(null, Qt.NoModifier),
            exec(null, null, Qt.ShiftModifier),
            exec(null, null, Qt.AltModifier),
            exec(null, null, Qt.ControlModifier),
            exec(null, null, Qt.AltModifier | Qt.ControlModifier | Qt.ShiftModifier),

            // Normal key sequences
            exec('u', Qt.Key_U),
            exec('U', Qt.Key_U, Qt.ShiftModifier),
            exec('alt+u', Qt.Key_U, Qt.AltModifier),
            exec('alt+U', Qt.Key_U, Qt.AltModifier | Qt.ShiftModifier),
            exec('ctrl+u', Qt.Key_U, Qt.ControlModifier),
            exec('ctrl+U', Qt.Key_U, Qt.ControlModifier | Qt.ShiftModifier),
            exec('ctrl+alt+u', Qt.Key_U, Qt.ControlModifier | Qt.AltModifier),
            exec('ctrl+alt+U', Qt.Key_U, Qt.AltModifier | Qt.ControlModifier | Qt.ShiftModifier),
            exec('?', Qt.Key_Question),
            exec('?', Qt.Key_Question, Qt.AltModifier | Qt.ControlModifier | Qt.ShiftModifier),
            exec('0', Qt.Key_0),
            exec('ctrl+alt+0', Qt.Key_0, Qt.AltModifier | Qt.ControlModifier | Qt.ShiftModifier),
        ]
    }

    function test_generate_command(data) {
        // data comes from test_generate_command_data
        compare(data.actual, data.expected)
    }

    function benchmark_generate_commandSpecialCommand() {
        const event = { key: 'PGUP', modifiers: null, text: 'PGUP' }
        const actual = TestObject.generateFrom(event)
    }

    function benchmark_generate_commandSpecialCommandWithModifier() {
        const event = { key: 'PGUP', modifiers: Qt.AltModifier | Qt.ControlModifier , text: 'PGUP' }
        const actual = TestObject.generateFrom(event)
    }

    function benchmark_generate_commandInvalidKeys() {
        const event = { key: null, modifiers: Qt.AltModifier | Qt.ControlModifier , text: null }
        const actual = TestObject.generateFrom(event)
    }

    function benchmark_generate_commandNormalSequences() {
        const event = { key: Qt.Key_U, modifiers: Qt.AltModifier | Qt.ControlModifier , text: 'u' }
        const actual = TestObject.generateFrom(event)
    }

}
