// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtTest

TestCase {
    id: testCase

    width: 400
    height: 200
    visible: true
    when: windowShown
    name: "MpvqcKeyboardFocusableButtonBox"

    Component {
        id: signalSpy

        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcKeyboardFocusableButtonBox {
            property alias acceptButton: _accept
            property alias rejectButton: _reject
            property alias destructiveButton: _destructive

            Button {
                id: _accept
                text: "Accept"
                DialogButtonBox.buttonRole: DialogButtonBox.AcceptRole
            }
            Button {
                id: _reject
                text: "Reject"
                DialogButtonBox.buttonRole: DialogButtonBox.RejectRole
            }
            Button {
                id: _destructive
                text: "Destructive"
                DialogButtonBox.buttonRole: DialogButtonBox.DestructiveRole
            }
        }
    }

    function makeControl(properties = {}): Item {
        const box = createTemporaryObject(objectUnderTest, testCase, properties);
        verify(box);
        return box;
    }

    function test_defaultInitialFocusRoleIsReject(): void {
        const box = makeControl();
        compare(box.initialFocusRole, DialogButtonBox.RejectRole);
        verify(box.rejectButton.down);
        verify(!box.acceptButton.down);
        verify(!box.destructiveButton.down);
    }

    function test_initialFocusRolePicksMatchingButton_data() {
        return [
            {
                tag: "accept",
                role: DialogButtonBox.AcceptRole,
                expectDown: "acceptButton"
            },
            {
                tag: "reject",
                role: DialogButtonBox.RejectRole,
                expectDown: "rejectButton"
            },
            {
                tag: "destructive",
                role: DialogButtonBox.DestructiveRole,
                expectDown: "destructiveButton"
            },
        ];
    }

    function test_initialFocusRolePicksMatchingButton(data): void {
        const box = makeControl({
            initialFocusRole: data.role
        });
        for (const name of ["acceptButton", "rejectButton", "destructiveButton"]) {
            compare(box[name].down, name === data.expectDown, `${name}.down`);
        }
    }

    function test_initialFocusFallsBackToFirstWhenRoleAbsent(): void {
        const box = makeControl({
            initialFocusRole: DialogButtonBox.HelpRole
        });
        const first = box.contentModel.get(0);
        verify(first.down, "first button in content model should be focused");
        for (let i = 1; i < box.count; i++) {
            verify(!box.contentModel.get(i).down, `index ${i} should not be focused`);
        }
    }

    function test_returnActivatesInitiallyFocusedButton_data() {
        return [
            {
                tag: "accept",
                role: DialogButtonBox.AcceptRole,
                focused: "acceptButton"
            },
            {
                tag: "reject",
                role: DialogButtonBox.RejectRole,
                focused: "rejectButton"
            },
            {
                tag: "destructive",
                role: DialogButtonBox.DestructiveRole,
                focused: "destructiveButton"
            },
        ];
    }

    function test_returnActivatesInitiallyFocusedButton(data): void {
        const box = makeControl({
            initialFocusRole: data.role
        });
        const spy = createTemporaryObject(signalSpy, testCase, {
            target: box[data.focused],
            signalName: "clicked"
        });

        keyPress(Qt.Key_Return);
        compare(spy.count, 1);
    }

    function test_rightArrowMovesFocusForward(): void {
        const box = makeControl({
            initialFocusRole: DialogButtonBox.RejectRole
        });
        const startIndex = box._focusedIndex;
        keyPress(Qt.Key_Right);
        compare(box._focusedIndex, (startIndex + 1) % box.count);
    }

    function test_leftArrowMovesFocusBackward(): void {
        const box = makeControl({
            initialFocusRole: DialogButtonBox.RejectRole
        });
        const startIndex = box._focusedIndex;
        keyPress(Qt.Key_Left);
        compare(box._focusedIndex, (startIndex - 1 + box.count) % box.count);
    }
}
