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

import "../../app"

TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcDialogEditInput"

    Component {
        id: signalSpy

        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcDialogEditInput {

            mpvqcApplication: QtObject {
                property var mpvqcPlayerFilesPyObject: QtObject {
                    property string default_input_conf_content: "default"
                    property url input_conf_url: Qt.resolvedUrl("")
                }
                property var mpvqcTheme: MpvqcTheme {
                    themeColorOption: 4
                    themeIdentifier: "Material You"
                }
            }
        }
    }

    function test_edit_accept() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        const acceptedSpy = createTemporaryObject(signalSpy, testCase, {
            target: control.editView,
            signalName: "accepted"
        });
        verify(acceptedSpy);

        const resetSpy = createTemporaryObject(signalSpy, testCase, {
            target: control.editView,
            signalName: "reset"
        });
        verify(resetSpy);

        control.editView.textArea.text = "changed by user";
        control.accepted();

        compare(acceptedSpy.count, 1);
        compare(resetSpy.count, 0);
    }

    function test_edit_reset() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        const acceptedSpy = createTemporaryObject(signalSpy, testCase, {
            target: control.content,
            signalName: "accepted"
        });
        verify(acceptedSpy);

        const resetSpy = createTemporaryObject(signalSpy, testCase, {
            target: control.editView,
            signalName: "reset"
        });
        verify(resetSpy);

        control.editView.textArea.text = "changed by user";
        control.reset();

        compare(acceptedSpy.count, 0);
        compare(resetSpy.count, 1);
    }
}
