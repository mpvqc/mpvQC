// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

TestCase {
    id: testCase

    name: "CheckBox"
    width: 400
    height: 400
    visible: true
    when: windowShown

    function makeControl(properties = {}): Item {
        const control = createTemporaryObject(objectUnderTest, testCase, properties);
        verify(control);
        waitForRendering(control);
        return control;
    }

    function test_states_data(): list<var> {
        return [
            {
                tag: "unchecked",
                checkState: Qt.Unchecked,
                checked: false,
                partial: false
            },
            {
                tag: "checked",
                checkState: Qt.Checked,
                checked: true,
                partial: false
            },
            {
                tag: "partially checked",
                checkState: Qt.PartiallyChecked,
                checked: false,
                partial: true
            },
        ];
    }

    function test_states(data): void {
        const control = makeControl({
            tristate: true,
            checkState: data.checkState
        });
        const indicator = findChild(control, "checkIndicator");
        verify(indicator);
        compare(indicator.checked, data.checked);
        compare(indicator.partial, data.partial);
    }

    Component {
        id: objectUnderTest

        CheckBox {
            text: "check box"
        }
    }
}
