// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

TestCase {
    id: testCase

    name: "RadioButton"
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
                checked: false
            },
            {
                tag: "checked",
                checked: true
            },
        ];
    }

    function test_states(data): void {
        const control = makeControl({
            checked: data.checked
        });
        const indicator = findChild(control, "radioIndicator");
        verify(indicator);
        compare(indicator.selected, data.checked);
    }

    Component {
        id: objectUnderTest

        RadioButton {
            text: "radio button"
        }
    }
}
