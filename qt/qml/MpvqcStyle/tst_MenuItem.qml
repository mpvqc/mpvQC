// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

TestCase {
    id: testCase

    name: "MenuItem"
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

    function test_indicatorKind_data(): list<var> {
        return [
            {
                tag: "exclusive shows the radio indicator",
                checkable: true,
                autoExclusive: true,
                radioVisible: true,
                checkVisible: false
            },
            {
                tag: "toggle shows the check indicator",
                checkable: true,
                autoExclusive: false,
                radioVisible: false,
                checkVisible: true
            },
            {
                tag: "uncheckable shows no indicator",
                checkable: false,
                autoExclusive: false,
                radioVisible: false,
                checkVisible: false
            },
        ];
    }

    function test_indicatorKind(data): void {
        const control = makeControl({
            checkable: data.checkable,
            autoExclusive: data.autoExclusive
        });
        const radio = findChild(control, "radioIndicator");
        const check = findChild(control, "checkIndicator");
        verify(radio);
        verify(check);
        compare(radio.visible, data.radioVisible);
        compare(check.visible, data.checkVisible);
    }

    function test_checkedReachesRadioIndicator(): void {
        const control = makeControl({
            checkable: true,
            autoExclusive: true,
            checked: true
        });
        const radio = findChild(control, "radioIndicator");
        verify(radio);
        compare(radio.selected, true);
    }

    function test_checkedReachesCheckIndicator(): void {
        const control = makeControl({
            checkable: true,
            checked: true
        });
        const check = findChild(control, "checkIndicator");
        verify(check);
        compare(check.checked, true);
    }

    Component {
        id: objectUnderTest

        MenuItem {
            text: "menu item"
        }
    }
}
