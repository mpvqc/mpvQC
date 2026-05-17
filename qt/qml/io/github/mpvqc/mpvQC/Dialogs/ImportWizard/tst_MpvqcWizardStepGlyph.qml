// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    width: 80
    height: 80
    visible: true
    when: windowShown
    name: "MpvqcWizardStepGlyph"

    Component {
        id: objectUnderTest

        MpvqcWizardStepGlyph {}
    }

    function makeControl(properties = {}): Item {
        const glyph = createTemporaryObject(objectUnderTest, testCase, properties);
        verify(glyph);
        return glyph;
    }

    readonly property var stateIconNames: ["upcomingStateIcon", "currentStateIcon", "completedStateIcon"]

    function test_activatesCorrectIcon_data() {
        return [
            {
                tag: "upcoming",
                completed: false,
                current: false,
                expectActive: "upcomingStateIcon"
            },
            {
                tag: "current",
                completed: false,
                current: true,
                expectActive: "currentStateIcon"
            },
            {
                tag: "completed",
                completed: true,
                current: false,
                expectActive: "completedStateIcon"
            },
        ];
    }

    function test_activatesCorrectIcon(data): void {
        const glyph = makeControl({
            completed: data.completed,
            current: data.current
        });
        for (const name of testCase.stateIconNames) {
            const icon = findChild(glyph, name);
            verify(icon, `${name} should exist`);
            compare(icon.active, name === data.expectActive, `${name}.active`);
        }
    }
}
