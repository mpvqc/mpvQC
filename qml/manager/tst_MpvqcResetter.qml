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
import QtQuick.Controls
import QtTest


Item {

    MpvqcResetter {
        id: objectUnderTest

        saved: true
        mpvqcApplication: ApplicationWindow {
            property real windowRadius: 12
        }

        property var test: TestCase {
            name: "MpvqcResetter"
            when: windowShown

            SignalSpy { id: resettedSpy; target: objectUnderTest; signalName: 'reset' }

            function init() {
                objectUnderTest.saved = true
                objectUnderTest.dialog = null
                resettedSpy.clear()
            }

            function test_reset_data() {
                return [
                    {
                        tag: 'saved',
                        saved: true,
                        expectedResetCalled: true,
                        exec: () => {
                            objectUnderTest.requestReset()
                        },
                    },
                    {
                        tag: 'unsaved/no',
                        saved: false,
                        expectedResetCalled: false,
                        exec: () => {
                            objectUnderTest.requestReset()
                        },
                    },
                    {
                        tag: 'unsaved/yes',
                        saved: false,
                        expectedResetCalled: true,
                        exec: () => {
                            objectUnderTest.requestReset()
                            objectUnderTest.dialog.accept()
                        },
                    }
                ]
            }

            function test_reset(data) {
                objectUnderTest.saved = data.saved
                data.exec()
                compare(resettedSpy.count, data.expectedResetCalled ? 1 : 0)
            }
        }
    }

}
