// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

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
