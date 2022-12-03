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
import QtTest

Item {
    id: testHelper

    width: 400
    height: 400

    MpvqcReverseTranslator {
        id: objectUnderTest
    }

    TestCase {
        name: "MpvqcReverseTranslator"
        when: windowShown

        function init() {
            objectUnderTest.timer.interval = 0
            objectUnderTest.translations = undefined
        }

        function test_lookupTableCreated() {
            verify(!objectUnderTest.translations)
            Qt.uiLanguage = 'en'
            wait(10)
            verify(objectUnderTest.translations)
        }

        function test_lookup_data() {
            return [
                {
                    tag: 'translated-a', expected: 'english-a',
                    translations: { 'translated-a': 'english-a', 'translated-b': 'english-b' }
                },
                {
                    tag: 'translated-b', expected: 'english-b',
                    translations: { 'translated-a': 'english-a', 'translated-b': 'english-b' }
                },
                { tag: 'translated-c', expected: 'translated-c', translations: {} },
            ]
        }

        function test_lookup(data) {
            objectUnderTest.translations = data.translations
            compare(objectUnderTest.lookup(data.tag), data.expected)
        }

    }

 }
