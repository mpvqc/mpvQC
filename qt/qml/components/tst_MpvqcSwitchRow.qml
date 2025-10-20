// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtTest

TestCase {
    id: testCase

    width: 400
    height: 400
    when: windowShown
    name: "MpvqcSwitchRow"
    visible: true

    Component {
        id: signalSpy

        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcSwitchRow {}
    }

    function test_toggle() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        const spy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: "toggled"
        });
        verify(spy);

        verify(!control.checked);

        mouseClick(control.toggle);
        compare(spy.count, 1);
        verify(control.checked);

        mouseClick(control.toggle);
        compare(spy.count, 2);
        verify(!control.checked);
    }
}
