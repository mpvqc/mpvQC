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


TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: 'MpvqcRowCommentTypeLabelEditMenu'

    Component { id: signalSpy; SignalSpy {} }

    Component {
        id: objectUnderTest

        MpvqcRowCommentTypeLabelEditMenu {
            mpvqcApplication: QtObject {
                property var mpvqcSettings: QtObject {
                    property var commentTypes: ListModel {
                        ListElement {type: '1'}
                        ListElement {type: '2'}
                        ListElement {type: '3'}
                        ListElement {type: '4'}
                        ListElement {type: '5'}
                        ListElement {type: '6'}
                        ListElement {type: '7'}

                        function items(): list<string> {
                            const marshalled = []
                            for (let i = 0; i < count; i++) {
                                marshalled.push(this.get(i)?.type)
                            }
                            return marshalled
                        }
                    }
                }
            }
        }
    }

    function test_comment_type_known() {
        const control = createTemporaryObject(objectUnderTest, testCase, { currentCommentType: '1' })
        verify(control)

        verify(!control.unknownCommentType.visible)
    }

    function test_comment_type_unknown() {
        const control = createTemporaryObject(objectUnderTest, testCase, { currentCommentType: '-1' })
        verify(control)

        verify(control.unknownCommentType.visible)
    }

    function test_clicked() {
        const control = createTemporaryObject(objectUnderTest, testCase, { currentCommentType: '1' })
        verify(control)

        const itemClickedSpy = signalSpy.createObject(null, {target: control, signalName: 'itemClicked'})
        mouseClick(control.itemAt(0))
        compare(itemClickedSpy.count, 1)
    }

}
