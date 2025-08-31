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

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcNewCommentMenu"

    Component {
        id: signalSpy

        SignalSpy {
            function invocation(invocation: int): variant {
                const inv = signalArguments[invocation];
                return {
                    arg: index => inv[index]
                };
            }
        }
    }

    Component {
        id: objectUnderTest

        MpvqcNewCommentMenu {
            commentTypes: ["1", "ABC", "3", "4"]
        }
    }

    function test_select() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        const spy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: "commentTypeChosen"
        });
        verify(spy);

        control.popup();

        keyClick(Qt.Key_Down);
        keyClick(Qt.Key_Down);
        keyClick(Qt.Key_Return);

        compare(spy.count, 1);
        compare(spy.invocation(0).arg(0), "ABC");
    }

    function test_cancel() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        const spy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: "commentTypeChosen"
        });
        verify(spy);

        compare(spy.count, 0);

        control.popup();

        keyClick(Qt.Key_Escape);

        compare(spy.count, 0);
    }
}
