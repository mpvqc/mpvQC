// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

TestCase {
    id: testCase

    name: "Switch"
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

    function thumbCenter(indicator: Item, checked: bool): real {
        return checked ? indicator.width - indicator.height / 2 : indicator.height / 2;
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
        const indicator = findChild(control, "switchIndicator");
        const thumb = findChild(control, "switchThumb");
        verify(indicator);
        verify(thumb);
        compare(thumb.centerX, thumbCenter(indicator, data.checked));
    }

    function test_toggle(): void {
        const control = makeControl();
        const indicator = findChild(control, "switchIndicator");
        const thumb = findChild(control, "switchThumb");
        verify(indicator);
        verify(thumb);

        control.toggle();
        tryCompare(thumb, "centerX", thumbCenter(indicator, true));

        control.toggle();
        tryCompare(thumb, "centerX", thumbCenter(indicator, false));
    }

    Component {
        id: objectUnderTest

        Switch {
            text: "switch"
        }
    }
}
