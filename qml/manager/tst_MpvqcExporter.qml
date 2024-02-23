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
    name: 'MpvqcExporter'

    Component {
        id: signalSpy; SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcExporter {
            property bool saveCalled: false

            video: ''
            document: ''

            mpvqcApplication: QtObject {
                property var mpvqcDocumentExporterPyObject: QtObject
                {
                    function generate_file_path_proposal() {
                        return '/some/path'
                    }

                    function save(document: url) {
                        saveCalled = true
                    }
                }
            }
        }
    }

    function test_saveNoDocument() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const savedSpy = signalSpy.createObject(control, {target: control, signalName: 'saved'})
        verify(savedSpy)

        verify(!control.exportDialog.visible)
        verify(!control.saveCalled)
        compare(savedSpy.count, 0)

        control.document = ''
        control.requestSave()

        compare(control.exportDialog.selectedFile.toString(), '/some/path.txt')
        verify(control.exportDialog.visible)
        verify(!control.saveCalled)
        compare(savedSpy.count, 0)
    }

    function test_saveDocument() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const savedSpy = signalSpy.createObject(control, {target: control, signalName: 'saved'})
        verify(savedSpy)

        verify(!control.exportDialog.visible)
        verify(!control.saveCalled)
        compare(savedSpy.count, 0)

        control.document = '/some/path'
        control.requestSave()

        verify(!control.exportDialog.visible)
        verify(control.saveCalled)
        compare(savedSpy.count, 1)
    }

    function test_saveAsAccepted() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const savedSpy = signalSpy.createObject(control, {target: control, signalName: 'saved'})
        verify(savedSpy)

        verify(!control.exportDialog.visible)
        verify(!control.saveCalled)
        compare(savedSpy.count, 0)

        control.requestSaveAs()

        verify(control.exportDialog.visible)
        verify(!control.saveCalled)
        compare(savedSpy.count, 0)

        control.exportDialog.accepted()

        verify(control.saveCalled)
        compare(savedSpy.count, 1)
    }

    function test_saveAsRejected() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const savedSpy = signalSpy.createObject(control, {target: control, signalName: 'saved'})
        verify(savedSpy)

        verify(!control.exportDialog.visible)
        verify(!control.saveCalled)
        compare(savedSpy.count, 0)

        control.requestSaveAs()

        verify(control.exportDialog.visible)
        verify(!control.saveCalled)
        compare(savedSpy.count, 0)

        control.exportDialog.rejected()

        verify(!control.saveCalled)
        compare(savedSpy.count, 0)
    }

}
