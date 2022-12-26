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

import models


TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: 'MpvqcTableEventHandler'

    Component { id: signalSpy; SignalSpy {} }

    Component {
        id: objectUnderTest

        MpvqcTableEventHandler {

            mpvqcApplication: QtObject {
                property bool fullscreen: false
                property var mpvqcSettings: QtObject {
                    property MpvqcCommentTypesModel commentTypes: MpvqcCommentTypesModel {}
                }
                property bool toggleFullScreenCalled: false
                function toggleFullScreen() { toggleFullScreenCalled = true }

                property bool disableFullScreenCalled: false
                function disableFullScreen() { disableFullScreenCalled = true  }
            }

            mpvqcCommentTable: QtObject {
                property int count: 0
                property bool editMode: false

                property bool startEditingCalled: false
                function startEditing() { startEditingCalled = true }
            }

            newCommentMenu: QtObject {
                property bool popupMenuCalled: false
                function popupMenu() { popupMenuCalled = true }
            }

            function helpEnableFullscreen(): void { mpvqcApplication.fullscreen = true }
            function helpHaveComments(): void { mpvqcCommentTable.count = 1 }
            function helpEditMode(enabled: bool): void { mpvqcCommentTable.editMode = enabled }
        }
    }

    function test_pressKeys_data() {
        return [
            {
                tag: 'e',
                prepare: (control) => {},
                runTest: (control) => keyPress(Qt.Key_E),
                verify: (control) => verify(control.newCommentMenu.popupMenuCalled),
            },
            {
                tag: 'f',
                prepare: (control) => {},
                runTest: (control) => keyPress(Qt.Key_F),
                verify: (control) => verify(control.mpvqcApplication.toggleFullScreenCalled),
            },
            {
                tag: 'return',
                prepare: (control) => {},
                runTest: (control) => keyPress(Qt.Key_Return),
                verify: (control) => verify(!control.mpvqcCommentTable.startEditingCalled),
            },
            {
                tag: 'return/fullscreen',
                prepare: (control) => control.helpEnableFullscreen(),
                runTest: (control) => keyPress(Qt.Key_Return),
                verify: (control) => verify(!control.mpvqcCommentTable.startEditingCalled),
            },
            {
                tag: 'return/comments',
                prepare: (control) => control.helpHaveComments(),
                runTest: (control) => keyPress(Qt.Key_Return),
                verify: (control) => verify(control.mpvqcCommentTable.startEditingCalled),
            },
            {
                tag: 'return/comments-fullscreen',
                prepare: (control) => {
                    control.helpEnableFullscreen()
                    control.helpHaveComments()
                },
                runTest: (control) => keyPress(Qt.Key_Return),
                verify: (control) => verify(!control.mpvqcCommentTable.startEditingCalled),
            },
            {
                tag: 'return/comments-already-editing',
                prepare: (control) => {
                    control.helpHaveComments()
                    control.helpEditMode(true)
                },
                runTest: (control) => keyPress(Qt.Key_Return),
                verify: (control) => verify(!control.mpvqcCommentTable.startEditingCalled),
            },
            {
                tag: 'escape',
                prepare: (control) => {},
                runTest: (control) => keyPress(Qt.Key_Escape),
                verify: (control) => verify(!control.mpvqcApplication.disableFullScreenCalled),
            },
            {
                tag: 'escape/fullscreen',
                prepare: (control) => control.helpEnableFullscreen(),
                runTest: (control) => keyPress(Qt.Key_Escape),
                verify: (control) => verify(control.mpvqcApplication.disableFullScreenCalled),
            },
            {
                tag: 'delete',
                prepare: function(control) {
                    this.spy = signalSpy.createObject(control, {target: control, signalName: 'deleteCommentPressed'})
                },
                runTest: (control) => keyPress(Qt.Key_Delete),
                verify: function(control) {
                    compare(this.spy.count, 0)
                },
            },
            {
                tag: 'delete/comments',
                prepare: function(control) {
                    control.helpHaveComments()
                    this.spy = signalSpy.createObject(control, {target: control, signalName: 'deleteCommentPressed'})
                },
                runTest: (control) => keyPress(Qt.Key_Delete),
                verify: function(control) {
                    compare(this.spy.count, 1)
                },
            },
            {
                tag: 'delete/comments-fullscreen',
                prepare: function(control) {
                    control.helpHaveComments()
                    control.helpEnableFullscreen()
                    this.spy = signalSpy.createObject(control, {target: control, signalName: 'deleteCommentPressed'})
                },
                runTest: (control) => keyPress(Qt.Key_Delete),
                verify: function(control) {
                    compare(this.spy.count, 0)
                },
            },
            {
                tag: 'backspace',
                prepare: function(control) {
                    this.spy = signalSpy.createObject(control, {target: control, signalName: 'deleteCommentPressed'})
                },
                runTest: (control) => keyPress(Qt.Key_Backspace),
                verify: function(control) {
                    compare(this.spy.count, 0)
                },
            },
            {
                tag: 'backspace/comments',
                prepare: function(control) {
                    control.helpHaveComments()
                    this.spy = signalSpy.createObject(control, {target: control, signalName: 'deleteCommentPressed'})
                },
                runTest: (control) => keyPress(Qt.Key_Backspace),
                verify: function(control) {
                    compare(this.spy.count, 1)
                },
            },
            {
                tag: 'backspace/comments-fullscreen',
                prepare: function(control) {
                    control.helpHaveComments()
                    control.helpEnableFullscreen()
                    this.spy = signalSpy.createObject(control, {target: control, signalName: 'deleteCommentPressed'})
                },
                runTest: (control) => keyPress(Qt.Key_Backspace),
                verify: function(control) {
                    compare(this.spy.count, 0)
                },
            },
            {
                tag: 'ctrl+c',
                prepare: function(control) {
                    this.spy = signalSpy.createObject(control, {target: control, signalName: 'copyToClipboardPressed'})
                },
                runTest: (control) => keyPress(Qt.Key_C, Qt.ControlModifier),
                verify: function(control) {
                    compare(this.spy.count, 0)
                },
            },
            {
                tag: 'ctrl+c/fullscreen',
                prepare: function(control) {
                    control.helpEnableFullscreen()
                    this.spy = signalSpy.createObject(control, {target: control, signalName: 'copyToClipboardPressed'})
                },
                runTest: (control) => keyPress(Qt.Key_C, Qt.ControlModifier),
                verify: function(control) {
                    compare(this.spy.count, 0)
                },
            },
            {
                tag: 'ctrl+c/comments',
                prepare: function(control) {
                    control.helpHaveComments()
                    this.spy = signalSpy.createObject(control, {target: control, signalName: 'copyToClipboardPressed'})
                },
                runTest: (control) => keyPress(Qt.Key_C, Qt.ControlModifier),
                verify: function(control) {
                    compare(this.spy.count, 1)
                },
            },
            {
                tag: 'ctrl+c/comments-fullscreen',
                prepare: function(control) {
                    control.helpHaveComments()
                    control.helpEnableFullscreen()
                    this.spy = signalSpy.createObject(control, {target: control, signalName: 'copyToClipboardPressed'})
                },
                runTest: (control) => keyPress(Qt.Key_C, Qt.ControlModifier),
                verify: function(control) {
                    compare(this.spy.count, 0)
                },
            },
            {
                tag: 'ctrl+c/comments-already-editing',
                prepare: function(control) {
                    control.helpHaveComments()
                    control.helpEditMode(true)
                    this.spy = signalSpy.createObject(control, {target: control, signalName: 'copyToClipboardPressed'})
                },
                runTest: (control) => keyPress(Qt.Key_C, Qt.ControlModifier),
                verify: function(control) {
                    compare(this.spy.count, 0)
                },
            },
        ]
    }

    function test_pressKeys(data) {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        data.prepare(control)
        data.runTest(control)
        data.verify(control)
    }

    function test_ignore() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const ignoredEvents = [
            { key: Qt.Key_Up },
            { key: Qt.Key_Down },
            { key: Qt.Key_Return, modifiers: Qt.NoModifier },
            { key: Qt.Key_Escape, modifiers: Qt.NoModifier },
            { key: Qt.Key_Delete, modifiers: Qt.NoModifier },
            { key: Qt.Key_Backspace, modifiers: Qt.NoModifier },
            { key: Qt.Key_F, modifiers: Qt.ControlModifier },
            { key: Qt.Key_C, modifiers: Qt.ControlModifier },
        ]

        for (const event of ignoredEvents) {
            verify(control.ignore(event))
        }

        verify(!control.ignore({ key: Qt.Key_T }))
    }

}
