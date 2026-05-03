// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtTest

TestCase {
    id: testCase

    name: "MpvqcCommentListKeyHandler"
    width: 400
    height: 400
    visible: true
    when: windowShown

    Component {
        id: signalSpy

        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcCommentListKeyHandler {
            hasComments: true
            ignoreEvents: false
            currentIndex: 0
        }
    }

    function makeControl(properties: var): var {
        const control = createTemporaryObject(objectUnderTest, testCase, properties ?? {});
        verify(control);
        return control;
    }

    function makeEvent(key: int, modifiers, isAutoRepeat): var {
        return {
            key: key,
            modifiers: modifiers ?? Qt.NoModifier,
            isAutoRepeat: isAutoRepeat ?? false,
            accepted: true
        };
    }

    function test_ignoreEvents_data(): list<var> {
        return [
            {
                tag: "return",
                key: Qt.Key_Return
            },
            {
                tag: "delete",
                key: Qt.Key_Delete
            },
            {
                tag: "backspace",
                key: Qt.Key_Backspace
            },
            {
                tag: "ctrl-c",
                key: Qt.Key_C
            },
            {
                tag: "ctrl-f",
                key: Qt.Key_F
            },
            {
                tag: "ctrl-z",
                key: Qt.Key_Z
            },
            {
                tag: "unknown",
                key: Qt.Key_A
            },
        ];
    }

    function test_ignoreEvents(data): void {
        const control = makeControl({
            ignoreEvents: true
        });

        let signalCount = 0;
        control.editCommentRequested.connect(() => signalCount++);
        control.deleteCommentRequested.connect(() => signalCount++);
        control.copyCommentRequested.connect(() => signalCount++);
        control.searchRequested.connect(() => signalCount++);
        control.undoRequested.connect(() => signalCount++);
        control.redoRequested.connect(() => signalCount++);

        const event = makeEvent(data.key, Qt.ControlModifier);
        control.handleKeyPress(event);

        compare(event.accepted, true);
        compare(signalCount, 0);
    }

    function test_notAccepted_data(): list<var> {
        return [
            {
                tag: "up",
                key: Qt.Key_Up
            },
            {
                tag: "down",
                key: Qt.Key_Down
            },
            {
                tag: "unknown",
                key: Qt.Key_A
            },
        ];
    }

    function test_notAccepted(data): void {
        const control = makeControl();
        const event = makeEvent(data.key);
        control.handleKeyPress(event);
        compare(event.accepted, false);
    }

    function test_return_data(): list<var> {
        return [
            {
                tag: "emits",
                props: {
                    hasComments: true,
                    currentIndex: 3,
                    isFullScreen: false
                },
                event: makeEvent(Qt.Key_Return),
                verify: spy => {
                    compare(spy.count, 1);
                    compare(spy.signalArguments[0][0], 3);
                }
            },
            {
                tag: "no-comments",
                props: {
                    hasComments: false,
                    currentIndex: 0,
                    isFullScreen: false
                },
                event: makeEvent(Qt.Key_Return),
                verify: spy => compare(spy.count, 0)
            },
            {
                tag: "auto-repeat",
                props: {
                    hasComments: true,
                    currentIndex: 0,
                    isFullScreen: false
                },
                event: makeEvent(Qt.Key_Return, Qt.NoModifier, true),
                verify: spy => compare(spy.count, 0)
            },
            {
                tag: "full-screen",
                props: {
                    hasComments: true,
                    currentIndex: 0,
                    isFullScreen: true
                },
                event: makeEvent(Qt.Key_Return),
                verify: spy => compare(spy.count, 0)
            },
        ];
    }

    function test_return(data): void {
        const control = makeControl(data.props);
        const spy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: "editCommentRequested"
        });
        control.handleKeyPress(data.event);
        data.verify(spy);
    }

    function test_delete_data(): list<var> {
        return [
            {
                tag: "delete-emits",
                props: {
                    hasComments: true,
                    currentIndex: 2,
                    isFullScreen: false
                },
                event: makeEvent(Qt.Key_Delete),
                verify: spy => {
                    compare(spy.count, 1);
                    compare(spy.signalArguments[0][0], 2);
                }
            },
            {
                tag: "backspace-emits",
                props: {
                    hasComments: true,
                    currentIndex: 2,
                    isFullScreen: false
                },
                event: makeEvent(Qt.Key_Backspace),
                verify: spy => {
                    compare(spy.count, 1);
                    compare(spy.signalArguments[0][0], 2);
                }
            },
            {
                tag: "delete-no-comments",
                props: {
                    hasComments: false,
                    currentIndex: 0,
                    isFullScreen: false
                },
                event: makeEvent(Qt.Key_Delete),
                verify: spy => compare(spy.count, 0)
            },
            {
                tag: "backspace-no-comments",
                props: {
                    hasComments: false,
                    currentIndex: 0,
                    isFullScreen: false
                },
                event: makeEvent(Qt.Key_Backspace),
                verify: spy => compare(spy.count, 0)
            },
            {
                tag: "delete-auto-repeat",
                props: {
                    hasComments: true,
                    currentIndex: 0,
                    isFullScreen: false
                },
                event: makeEvent(Qt.Key_Delete, Qt.NoModifier, true),
                verify: spy => compare(spy.count, 0)
            },
            {
                tag: "backspace-auto-repeat",
                props: {
                    hasComments: true,
                    currentIndex: 0,
                    isFullScreen: false
                },
                event: makeEvent(Qt.Key_Backspace, Qt.NoModifier, true),
                verify: spy => compare(spy.count, 0)
            },
            {
                tag: "delete-full-screen",
                props: {
                    hasComments: true,
                    currentIndex: 0,
                    isFullScreen: true
                },
                event: makeEvent(Qt.Key_Delete),
                verify: spy => compare(spy.count, 0)
            },
            {
                tag: "backspace-full-screen",
                props: {
                    hasComments: true,
                    currentIndex: 0,
                    isFullScreen: true
                },
                event: makeEvent(Qt.Key_Backspace),
                verify: spy => compare(spy.count, 0)
            },
        ];
    }

    function test_delete(data): void {
        const control = makeControl(data.props);
        const spy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: "deleteCommentRequested"
        });
        control.handleKeyPress(data.event);
        data.verify(spy);
    }

    function test_ctrlC_data(): list<var> {
        return [
            {
                tag: "emits",
                props: {
                    hasComments: true,
                    currentIndex: 4,
                    isFullScreen: false
                },
                event: makeEvent(Qt.Key_C, Qt.ControlModifier),
                verify: (spy, event) => {
                    compare(spy.count, 1);
                    compare(spy.signalArguments[0][0], 4);
                }
            },
            {
                tag: "no-ctrl",
                props: {
                    hasComments: true,
                    isFullScreen: false
                },
                event: makeEvent(Qt.Key_C, Qt.NoModifier),
                verify: (spy, event) => compare(event.accepted, false)
            },
            {
                tag: "no-comments",
                props: {
                    hasComments: false,
                    isFullScreen: false
                },
                event: makeEvent(Qt.Key_C, Qt.ControlModifier),
                verify: (spy, event) => compare(event.accepted, false)
            },
            {
                tag: "auto-repeat",
                props: {
                    hasComments: true,
                    isFullScreen: false
                },
                event: makeEvent(Qt.Key_C, Qt.ControlModifier, true),
                verify: (spy, event) => compare(event.accepted, false)
            },
            {
                tag: "full-screen",
                props: {
                    hasComments: true,
                    isFullScreen: true
                },
                event: makeEvent(Qt.Key_C, Qt.ControlModifier),
                verify: (spy, event) => compare(event.accepted, false)
            },
        ];
    }

    function test_ctrlC(data): void {
        const control = makeControl(data.props);
        const spy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: "copyCommentRequested"
        });
        control.handleKeyPress(data.event);
        data.verify(spy, data.event);
    }

    function test_ctrlF_data(): list<var> {
        return [
            {
                tag: "emits",
                props: {
                    hasComments: true,
                    isFullScreen: false
                },
                event: makeEvent(Qt.Key_F, Qt.ControlModifier),
                verify: (spy, event) => compare(spy.count, 1)
            },
            {
                tag: "no-ctrl",
                props: {
                    hasComments: true,
                    isFullScreen: false
                },
                event: makeEvent(Qt.Key_F, Qt.NoModifier),
                verify: (spy, event) => compare(event.accepted, false)
            },
            {
                tag: "no-comments",
                props: {
                    hasComments: false,
                    isFullScreen: false
                },
                event: makeEvent(Qt.Key_F, Qt.ControlModifier),
                verify: (spy, event) => compare(event.accepted, false)
            },
            {
                tag: "auto-repeat",
                props: {
                    hasComments: true,
                    isFullScreen: false
                },
                event: makeEvent(Qt.Key_F, Qt.ControlModifier, true),
                verify: (spy, event) => compare(event.accepted, false)
            },
            {
                tag: "full-screen",
                props: {
                    hasComments: true,
                    isFullScreen: true
                },
                event: makeEvent(Qt.Key_F, Qt.ControlModifier),
                verify: (spy, event) => compare(event.accepted, false)
            },
        ];
    }

    function test_ctrlF(data): void {
        const control = makeControl(data.props);
        const spy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: "searchRequested"
        });
        control.handleKeyPress(data.event);
        data.verify(spy, data.event);
    }

    function test_ctrlZ_data(): list<var> {
        return [
            {
                tag: "undo",
                signalName: "undoRequested",
                event: makeEvent(Qt.Key_Z, Qt.ControlModifier),
                verify: (spy, event) => compare(spy.count, 1)
            },
            {
                tag: "redo",
                signalName: "redoRequested",
                event: makeEvent(Qt.Key_Z, Qt.ControlModifier | Qt.ShiftModifier),
                verify: (spy, event) => compare(spy.count, 1)
            },
            {
                tag: "no-ctrl",
                signalName: "undoRequested",
                event: makeEvent(Qt.Key_Z, Qt.NoModifier),
                verify: (spy, event) => compare(event.accepted, false)
            },
            {
                tag: "auto-repeat",
                signalName: "undoRequested",
                event: makeEvent(Qt.Key_Z, Qt.ControlModifier, true),
                verify: (spy, event) => compare(event.accepted, false)
            },
        ];
    }

    function test_ctrlZ(data): void {
        const control = makeControl();
        const spy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: data.signalName
        });
        control.handleKeyPress(data.event);
        data.verify(spy, data.event);
    }
}
