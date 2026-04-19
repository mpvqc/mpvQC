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
            function invocation(invocation: int): var {
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
            id: menu

            property int pausePlayerCount: 0

            viewModel: QtObject {
                readonly property var commentTypes: ["1", "ABC", "3", "4"]
                function cursorPosition(): point {
                    return Qt.point(0, 0);
                }
                function pausePlayer(): void {
                    menu.pausePlayerCount += 1;
                }
            }
        }
    }

    function makeControl(): var {
        const control = createTemporaryObject(objectUnderTest, testCase, {});
        verify(control);
        return control;
    }

    function makeSpy(control, signalName): var {
        const spy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: signalName
        });
        verify(spy);
        return spy;
    }

    function test_select() {
        const control = makeControl();
        const spy = makeSpy(control, "commentTypeChosen");
        control.popup();

        keyClick(Qt.Key_Down);
        keyClick(Qt.Key_Down);
        keyClick(Qt.Key_Return);

        compare(spy.count, 1);
        compare(spy.invocation(0).arg(0), "ABC");
        compare(control.pausePlayerCount, 1);
    }

    function test_cancel() {
        const control = makeControl();
        const spy = makeSpy(control, "commentTypeChosen");

        control.popup();

        keyClick(Qt.Key_Escape);
        compare(spy.count, 0);
        compare(control.pausePlayerCount, 1);
    }

    function test_hidden_after_close() {
        const control = makeControl();

        control.popup();
        tryCompare(control, "visible", true);

        control.close();
        tryCompare(control, "visible", false);
    }
}
