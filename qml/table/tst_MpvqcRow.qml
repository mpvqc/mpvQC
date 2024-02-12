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
    name: 'MpvqcRow'

    Component { id: signalSpy; SignalSpy {} }

    Component {
        id: objectUnderTest

        MpvqcRow {
            id: objectUnderTest

            rowSelected: false
            tableInEditMode: false
            searchQuery: ''

            mpvqcApplication: QtObject {
                property var mpvqcLabelWidthCalculator: QtObject {
                    property int commentTypesWidth: 120
                }
                property var mpvqcTimeFormatUtils: QtObject {
                    function formatTimeToString(time) { return `${time}` }
                }
            }

            index: 0
            time: 42
            commentType: 'Phrasing'
            comment: 'Old Comment'
        }
    }

    function test_click() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        let spy = signalSpy.createObject(control, {target: control, signalName: 'clicked'})
        verify(spy)

        let playClickedSpy = signalSpy.createObject(control, {target: control, signalName: 'playClicked'})
        verify(playClickedSpy)

        control.playButton.clicked()
        compare(spy.count, 1)
        compare(playClickedSpy.count, 1)

        control.timeLabel.clicked()
        compare(spy.count, 2)

        control.commentTypeLabel.clicked()
        compare(spy.count, 3)

        control.commentLabel.clicked()
        compare(spy.count, 4)
    }

    function test_edit() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        control.time = 42
        control.commentType = 'Phrasing'
        control.comment = 'Old Comment'

        const timeSpy = signalSpy.createObject(control, {target: control, signalName: 'timeEdited'})
        const typeSpy = signalSpy.createObject(control, {target: control, signalName: 'commentTypeEdited'})
        const commSpy = signalSpy.createObject(control, {target: control, signalName: 'commentEdited'})

        verify(timeSpy)
        verify(typeSpy)
        verify(commSpy)

        control.timeLabel.edited(43)
        compare(timeSpy.count, 1)
        compare(typeSpy.count, 0)
        compare(commSpy.count, 0)
        compare(timeSpy.signalArguments[0][0], 43)

        control.commentTypeLabel.edited('Translation')
        compare(timeSpy.count, 1)
        compare(typeSpy.count, 1)
        compare(commSpy.count, 0)
        compare(typeSpy.signalArguments[0][0], 'Translation')

        control.commentLabel.edited('New Comment')
        compare(timeSpy.count, 1)
        compare(typeSpy.count, 1)
        compare(commSpy.count, 1)
        compare(commSpy.signalArguments[0][0], 'New Comment')
    }

    function test_editingStarted() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const spy = signalSpy.createObject(control, {target: control, signalName: 'editingStarted'})
        verify(spy)

        control.timeLabel.editingStarted()
        compare(spy.count, 1)

        control.commentTypeLabel.editingStarted()
        compare(spy.count, 2)

        control.commentLabel.editingStarted()
        compare(spy.count, 3)
    }

    function test_editingStopped() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const spy = signalSpy.createObject(control, {target: control, signalName: 'editingStopped'})
        verify(spy)

        control.timeLabel.editingStopped()
        compare(spy.count, 1)

        control.commentTypeLabel.editingStopped()
        compare(spy.count, 2)

        control.commentLabel.editingStopped()
        compare(spy.count, 3)
    }

    function test_upAndDownSignals() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        let spy = signalSpy.createObject(control, {target: control, signalName: 'upPressed'})
        verify(spy)
        control.commentLabel.upPressed()
        compare(spy.count, 1)

        spy = signalSpy.createObject(control, {target: control, signalName: 'downPressed'})
        verify(spy)
        control.commentLabel.downPressed()
        compare(spy.count, 1)
    }

    function test_menuSignals() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        let spy = signalSpy.createObject(control, {target: control, signalName: 'copyCommentClicked'})
        verify(spy)
        control.moreButton.copyCommentClicked()
        compare(spy.count, 1)

        spy = signalSpy.createObject(control, {target: control, signalName: 'deleteCommentClicked'})
        verify(spy)
        control.moreButton.deleteCommentClicked()
        compare(spy.count, 1)
    }

    function test_copyClipboardContent() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        control.time = 0
        control.commentType = 'Comment Type'
        control.comment = 'Comment'
        compare(control.toClipboardContent(), '[0] [Comment Type] Comment')

        control.time = 59
        control.commentType = 'Other Comment Type'
        control.comment = ''
        compare(control.toClipboardContent(), '[59] [Other Comment Type]')
    }

}
