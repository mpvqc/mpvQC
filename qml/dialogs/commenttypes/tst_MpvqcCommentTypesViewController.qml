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

import QtTest
import QtQuick


TestCase {
    id: testCase

    property list < string > testModel: ['Type 0', 'Type 1', 'Type 2']

    name: "MpvqcCommentTypesViewController"

    Component {
        id: signalSpy

        SignalSpy {
            function invocation(invocation: int) {
                const inv = signalArguments[invocation]
                return {arg: index => inv[index]}
            }
        }
    }

    Component {
        id: objectUnderTest

        MpvqcCommentTypesViewController {
            selectedIndex: 0
            model: [...testModel]
        }
    }

    function test_add() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const spy = signalSpy.createObject(control, {target: control, signalName: 'highlightIndexRequested'})
        verify(spy)

        compare(control.modelCopy.length, 3)
        compare(spy.count, 0)

        control.add('New Type')

        compare(control.modelCopy.length, 4)
        compare(spy.count, 1)

        compare(spy.invocation(0).arg(0), control.modelCopy.length - 1)
    }

    function test_replaceWith() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        control.selectedIndex = 1
        compare(control.modelCopy[control.selectedIndex], 'Type 1')

        control.replaceWith('New Type')
        compare(control.modelCopy[control.selectedIndex], 'New Type')
    }

    function test_moveUp() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const spy = signalSpy.createObject(control, {target: control, signalName: 'highlightIndexRequested'})
        verify(spy)

        control.selectedIndex = 2

        compare(control.modelCopy[control.selectedIndex - 1], 'Type 1')
        compare(control.modelCopy[control.selectedIndex], 'Type 2')

        control.moveUp()

        compare(control.modelCopy[control.selectedIndex - 1], 'Type 2')
        compare(control.modelCopy[control.selectedIndex], 'Type 1')
        compare(spy.count, 1)
        compare(spy.invocation(0).arg(0), 1)
    }

    function test_moveDown() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const spy = signalSpy.createObject(control, {target: control, signalName: 'highlightIndexRequested'})
        verify(spy)

        control.selectedIndex = 1
        compare(control.modelCopy[control.selectedIndex], 'Type 1')
        compare(control.modelCopy[control.selectedIndex + 1], 'Type 2')

        control.moveDown()

        compare(control.modelCopy[control.selectedIndex], 'Type 2')
        compare(control.modelCopy[control.selectedIndex + 1], 'Type 1')
        compare(spy.count, 1)
        compare(spy.invocation(0).arg(0), 2)
    }

    function test_startEditing() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const spy = signalSpy.createObject(control, {target: control, signalName: 'editClicked'})
        verify(spy)

        control.selectedIndex = 1
        control.startEditing()

        compare(spy.count, 1)
        compare(spy.invocation(0).arg(0), 'Type 1')

        control.selectedIndex = 2
        control.startEditing()

        compare(spy.count, 2)
        compare(spy.invocation(1).arg(0), 'Type 2')
    }

    function test_deleteItem() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const spy = signalSpy.createObject(control, {target: control, signalName: 'highlightIndexRequested'})
        verify(spy)

        control.selectedIndex = 1
        control.deleteItem()

        compare(control.modelCopy.length, 2)
        compare(spy.count, 1)
        compare(spy.invocation(0).arg(0), 1)

        control.selectedIndex = 1
        control.deleteItem()

        compare(control.modelCopy.length, 1)
        compare(spy.count, 2)
        compare(spy.invocation(1).arg(0), 0)
    }

    function test_acceptModelCopy() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const spy = signalSpy.createObject(control, {target: control, signalName: 'acceptCopyRequested'})
        verify(spy)

        control.acceptModelCopy()
        compare(spy.count, 1)
    }

    function test_reset() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const spy = signalSpy.createObject(control, {target: control, signalName: 'resetRequested'})
        verify(spy)

        control.reset()
        compare(spy.count, 1)
    }

}
