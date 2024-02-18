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
            property var writenFilePath: ''
            property var writenContent: ''

            video: ''
            document: ''

            mpvqcApplication: QtObject {
                property var mpvqcSettings: QtObject
                {
                    property string nickname: 'nickname'
                }

                property var mpvqcCommentTable: QtObject
                {
                    function getAllComments() {
                        return []
                    }
                }

                property var mpvqcFileSystemHelperPyObject: QtObject
                {
                    function write(filePath, content) {
                        writenFilePath = filePath
                        writenContent = content
                    }
                }

                property var mpvqcDocumentExporterPyObject: QtObject
                {
                    function generate_file_path_proposal() {
                        return '/some/path'
                    }
                }

                property var mpvqcTimeFormatUtils: QtObject
                {
                    function formatTimeToStringLong(seconds) {
                        return 'formatted'
                    }
                }
            }

            generator: QtObject {
                function createExportContent(video) {
                    return 'content'
                }
            }

        }
    }

    function test_save() {
        let control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        control.requestSave()

        compare(control.exportDialog.selectedFile.toString(), '/some/path.txt')
        compare(control.writenFilePath, '')
        compare(control.writenContent, '')


        control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        control.document = '/some/path'
        control.requestSave()

        compare(control.writenFilePath, '/some/path')
        compare(control.writenContent, 'content')
    }

    function test_saveAs() {
        let control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        let savedSpy = signalSpy.createObject(control, {target: control, signalName: 'saved'})
        verify(savedSpy)

        control.requestSaveAs()
        control.exportDialog.accepted()

        compare(savedSpy.count, 1)


        control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        savedSpy = signalSpy.createObject(control, {target: control, signalName: 'saved'})
        verify(savedSpy)

        control.requestSaveAs()
        control.exportDialog.rejected()

        compare(savedSpy.count, 0)
    }

}
