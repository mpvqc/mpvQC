// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtTest

TestCase {
    id: testCase

    name: "MpvqcContentKeyHandler"

    Component {
        id: signalSpy

        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcContentKeyHandler {}
    }

    function makeControl(): var {
        const control = createTemporaryObject(objectUnderTest, testCase, {});
        verify(control);
        return control;
    }

    function makeEvent(key: int, modifiers, isAutoRepeat): var {
        return {
            key: key,
            modifiers: modifiers ?? Qt.NoModifier,
            isAutoRepeat: isAutoRepeat ?? false,
            accepted: false
        };
    }

    function makeSpy(control, signalName): var {
        return createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: signalName
        });
    }

    function test_emit_data(): list<var> {
        return [
            {
                tag: "e_nomod_emits_open_menu",
                event: makeEvent(Qt.Key_E),
                signalName: "openCommentMenuRequested"
            },
            {
                tag: "f_nomod_emits_toggle_fs",
                event: makeEvent(Qt.Key_F),
                signalName: "toggleFullScreenRequested"
            },
            {
                tag: "e_with_numlock_emits_open_menu",
                event: makeEvent(Qt.Key_E, Qt.KeypadModifier),
                signalName: "openCommentMenuRequested"
            },
            {
                tag: "f_with_numlock_emits_toggle_fs",
                event: makeEvent(Qt.Key_F, Qt.KeypadModifier),
                signalName: "toggleFullScreenRequested"
            }
        ];
    }

    function test_emit(data): void {
        const control = makeControl();
        const spy = makeSpy(control, data.signalName);
        control.handleKeyPress(data.event);
        compare(spy.count, 1);
        compare(data.event.accepted, true);
    }

    function test_swallow_data(): list<var> {
        return [
            {
                tag: "e_nomod_autorepeat",
                event: makeEvent(Qt.Key_E, Qt.NoModifier, true)
            },
            {
                tag: "f_nomod_autorepeat",
                event: makeEvent(Qt.Key_F, Qt.NoModifier, true)
            },
            {
                tag: "e_with_numlock_autorepeat",
                event: makeEvent(Qt.Key_E, Qt.KeypadModifier, true)
            },
            {
                tag: "f_with_numlock_autorepeat",
                event: makeEvent(Qt.Key_F, Qt.KeypadModifier, true)
            },
            {
                tag: "up_nomod",
                event: makeEvent(Qt.Key_Up)
            },
            {
                tag: "up_nomod_autorepeat",
                event: makeEvent(Qt.Key_Up, Qt.NoModifier, true)
            },
            {
                tag: "down_nomod",
                event: makeEvent(Qt.Key_Down)
            },
            {
                tag: "up_with_numlock",
                event: makeEvent(Qt.Key_Up, Qt.KeypadModifier)
            },
            {
                tag: "return_nomod",
                event: makeEvent(Qt.Key_Return)
            },
            {
                tag: "delete_nomod",
                event: makeEvent(Qt.Key_Delete)
            },
            {
                tag: "backspace_nomod",
                event: makeEvent(Qt.Key_Backspace)
            },
            {
                tag: "ctrl_f",
                event: makeEvent(Qt.Key_F, Qt.ControlModifier)
            },
            {
                tag: "ctrl_c",
                event: makeEvent(Qt.Key_C, Qt.ControlModifier)
            },
            {
                tag: "ctrl_z",
                event: makeEvent(Qt.Key_Z, Qt.ControlModifier)
            },
            {
                tag: "ctrl_shift_z",
                event: makeEvent(Qt.Key_Z, Qt.ControlModifier | Qt.ShiftModifier)
            },
            {
                tag: "ctrl_f_with_numlock",
                event: makeEvent(Qt.Key_F, Qt.ControlModifier | Qt.KeypadModifier)
            }
        ];
    }

    function test_swallow(data): void {
        const control = makeControl();
        const openMenuSpy = makeSpy(control, "openCommentMenuRequested");
        const toggleFsSpy = makeSpy(control, "toggleFullScreenRequested");
        const forwardSpy = makeSpy(control, "forwardKeyToPlayerRequested");
        control.handleKeyPress(data.event);
        compare(openMenuSpy.count, 0);
        compare(toggleFsSpy.count, 0);
        compare(forwardSpy.count, 0);
        compare(data.event.accepted, true);
    }

    function test_forward_data(): list<var> {
        return [
            {
                tag: "space",
                event: makeEvent(Qt.Key_Space)
            },
            {
                tag: "a",
                event: makeEvent(Qt.Key_A)
            },
            {
                tag: "ctrl_e",
                event: makeEvent(Qt.Key_E, Qt.ControlModifier)
            },
            {
                tag: "ctrl_return",
                event: makeEvent(Qt.Key_Return, Qt.ControlModifier)
            },
            {
                tag: "shift_e",
                event: makeEvent(Qt.Key_E, Qt.ShiftModifier)
            },
            {
                tag: "shift_f",
                event: makeEvent(Qt.Key_F, Qt.ShiftModifier)
            },
            {
                tag: "shift_c",
                event: makeEvent(Qt.Key_C, Qt.ShiftModifier)
            },
            {
                tag: "plain_c",
                event: makeEvent(Qt.Key_C)
            },
            {
                tag: "plain_z",
                event: makeEvent(Qt.Key_Z)
            },
            {
                tag: "shift_z",
                event: makeEvent(Qt.Key_Z, Qt.ShiftModifier)
            },
            {
                tag: "ctrl_alt_z",
                event: makeEvent(Qt.Key_Z, Qt.ControlModifier | Qt.AltModifier)
            },
            {
                tag: "ctrl_shift_f",
                event: makeEvent(Qt.Key_F, Qt.ControlModifier | Qt.ShiftModifier)
            },
            {
                tag: "ctrl_shift_c",
                event: makeEvent(Qt.Key_C, Qt.ControlModifier | Qt.ShiftModifier)
            },
            {
                tag: "up_ctrl",
                event: makeEvent(Qt.Key_Up, Qt.ControlModifier)
            },
            {
                tag: "up_shift",
                event: makeEvent(Qt.Key_Up, Qt.ShiftModifier)
            },
            {
                tag: "down_ctrl_autorepeat",
                event: makeEvent(Qt.Key_Down, Qt.ControlModifier, true)
            },
            {
                tag: "return_shift",
                event: makeEvent(Qt.Key_Return, Qt.ShiftModifier)
            }
        ];
    }

    function test_forward(data): void {
        const control = makeControl();
        const spy = makeSpy(control, "forwardKeyToPlayerRequested");
        control.handleKeyPress(data.event);
        compare(spy.count, 1);
        compare(spy.signalArguments[0][0], data.event.key);
        compare(spy.signalArguments[0][1], data.event.modifiers);
        compare(data.event.accepted, true);
    }
}
