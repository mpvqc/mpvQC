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
    name: 'MpvqcDialogEditMpv'

    Component { id: signalSpy; SignalSpy {} }

    Component {
        id: objectUnderTest

        MpvqcDialogEditMpv {

            mpvqcApplication: QtObject {
                property var mpvqcMpvFiles: QtObject {
                    property var editMpvInterface: QtObject {
                        property string fileContent: 'initial'
                    }
                }
                property var mpvqcResourcePyObject: QtObject {
                    function get_mpv_conf_content() { return 'default' }
                }
            }
        }
    }

    function test_initial() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        compare(control.editView.textArea.text, 'initial')
    }

    function test_edit_accept() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        control.editView.textArea.text = 'changed by user'
        control.accepted()
        compare(control.mpvqcApplication.mpvqcMpvFiles.editMpvInterface.fileContent, 'changed by user')
    }

    function test_edit_cancel() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        control.editView.textArea.text = 'changed by user'
        compare(control.mpvqcApplication.mpvqcMpvFiles.editMpvInterface.fileContent, 'initial')

        control.rejected()
        compare(control.mpvqcApplication.mpvqcMpvFiles.editMpvInterface.fileContent, 'initial')
    }

    function test_edit_reset() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        control.editView.textArea.text = 'changed by user'
        compare(control.editView.textArea.text, 'changed by user')
        compare(control.mpvqcApplication.mpvqcMpvFiles.editMpvInterface.fileContent, 'initial')
        control.reset()
        compare(control.editView.textArea.text, 'default')
        compare(control.mpvqcApplication.mpvqcMpvFiles.editMpvInterface.fileContent, 'initial')

        control.editView.textArea.text = 'changed by user again'
        compare(control.editView.textArea.text, 'changed by user again')
        compare(control.mpvqcApplication.mpvqcMpvFiles.editMpvInterface.fileContent, 'initial')
        control.reset()
        compare(control.editView.textArea.text, 'default')
        compare(control.mpvqcApplication.mpvqcMpvFiles.editMpvInterface.fileContent, 'initial')
    }

}
