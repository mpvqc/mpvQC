// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtTest

import io.github.mpvqc.mpvQC.Components

TestCase {
    id: testCase

    width: 600
    height: 600
    visible: true
    when: windowShown
    name: "MpvqcPositionedMenu"

    Component {
        id: container

        Item {
            width: testCase.width
            height: testCase.height
        }
    }

    Component {
        id: objectUnderTest

        MpvqcPositionedMenu {
            MenuItem {
                text: "Test Item 1"
            }
            MenuItem {
                text: "Test Item 2"
            }
            MenuItem {
                text: "Test Item 3"
            }
        }
    }

    Component {
        id: objectUnderTestOverwriteCalculatePosition

        MpvqcPositionedMenu {
            function calculatePosition(): point {
                return Qt.point(200, 300);
            }
            MenuItem {
                text: "Test Item 1"
            }
            MenuItem {
                text: "Test Item 2"
            }
            MenuItem {
                text: "Test Item 3"
            }
        }
    }

    function makeControl(properties = {}): Item {
        const parent = createTemporaryObject(container, testCase);
        verify(parent);

        const menu = createTemporaryObject(objectUnderTest, parent, properties);
        verify(menu);

        return menu;
    }

    function test_top_left_no_violations() {
        const menu = makeControl();

        menu.position = Qt.point(100, 100);
        menu.open();

        tryVerify(() => menu.opened);

        // Menu should appear at cursor position (no violations)
        fuzzyCompare(menu.x, 100, 2);
        fuzzyCompare(menu.y, 100, 2);
        compare(menu.transformOrigin, Popup.TopLeft);
    }

    function test_bottom_right_violations() {
        const menu = makeControl();

        const posX = testCase.width - 10;
        const posY = testCase.height - 10;

        menu.position = Qt.point(posX, posY);
        menu.open();

        tryVerify(() => menu.opened);

        // Menu should flip left and up
        fuzzyCompare(menu.x, posX - menu.width, 2);
        fuzzyCompare(menu.y, posY - menu.height, 2);
        compare(menu.transformOrigin, Popup.BottomRight);
    }

    function test_bottom_violation_only() {
        const menu = makeControl();

        const posX = 100;
        const posY = testCase.height - 10;

        menu.position = Qt.point(posX, posY);
        menu.open();

        tryVerify(() => menu.opened);

        // Menu should flip up but not left
        fuzzyCompare(menu.x, posX, 2);
        fuzzyCompare(menu.y, posY - menu.height, 2);
        compare(menu.transformOrigin, Popup.BottomLeft);
    }

    function test_right_violation_only() {
        const menu = makeControl();

        const posX = testCase.width - 10;
        const posY = 100;

        menu.position = Qt.point(posX, posY);
        menu.open();

        tryVerify(() => menu.opened);

        // Menu should flip left but not up
        fuzzyCompare(menu.x, posX - menu.width, 2);
        fuzzyCompare(menu.y, posY, 2);
        compare(menu.transformOrigin, Popup.TopRight);
    }

    function test_mirrored_no_violations() {
        const menu = makeControl({
            isMirrored: true
        });

        menu.position = Qt.point(400, 100);
        menu.open();

        tryVerify(() => menu.opened);

        // In mirrored mode, menu extends to the left by default
        fuzzyCompare(menu.x, 400 - menu.width, 2);
        fuzzyCompare(menu.y, 100, 2);
        compare(menu.transformOrigin, Popup.TopRight);
    }

    function test_mirrored_left_violation() {
        const menu = makeControl({
            isMirrored: true
        });

        menu.position = Qt.point(10, 100);
        menu.open();

        tryVerify(() => menu.opened);

        // Menu should flip to the right
        fuzzyCompare(menu.x, 10, 2);
        fuzzyCompare(menu.y, 100, 2);
        compare(menu.transformOrigin, Popup.TopLeft);
    }

    function test_deferred_action() {
        const menu = makeControl();

        let actionExecuted = false;

        menu.position = Qt.point(100, 100);
        menu.open();

        tryVerify(() => menu.opened);

        menu.deferToOnClose = () => {
            actionExecuted = true;
        };

        menu.close();

        tryVerify(() => !menu.opened);
        tryVerify(() => actionExecuted);
    }

    function test_custom_calculate_position() {
        const parent = createTemporaryObject(container, testCase);
        verify(parent);

        const menu = createTemporaryObject(objectUnderTestOverwriteCalculatePosition, parent);
        verify(menu);

        menu.position = Qt.point(100, 100); // This should be ignored
        menu.open();

        tryVerify(() => menu.opened);

        // Menu should use the overridden position
        fuzzyCompare(menu.x, 200, 2);
        fuzzyCompare(menu.y, 300, 2);
    }
}
