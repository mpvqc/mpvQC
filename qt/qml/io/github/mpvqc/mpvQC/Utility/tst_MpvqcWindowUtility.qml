// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase
    name: "MpvqcWindowUtility"

    Item {
        id: frame
        width: 300
        height: 200
    }

    function cleanup(): void {
        MpvqcWindowUtility.contentFrame = null;
    }

    function test_getEdgeViolations_data(): var {
        return [
            {
                tag: "interior_violates_nothing",
                x: 100,
                y: 80,
                width: 50,
                height: 40,
                margin: 8,
                bottom: false,
                top: false,
                left: false,
                right: false
            },
            {
                tag: "near_right_edge_violates_right",
                x: 270,
                y: 80,
                width: 50,
                height: 40,
                margin: 8,
                bottom: false,
                top: false,
                left: false,
                right: true
            },
            {
                tag: "near_bottom_edge_violates_bottom",
                x: 100,
                y: 180,
                width: 50,
                height: 40,
                margin: 8,
                bottom: true,
                top: false,
                left: false,
                right: false
            },
            {
                tag: "near_top_left_violates_top_and_left",
                x: 4,
                y: 4,
                width: 50,
                height: 40,
                margin: 8,
                bottom: false,
                top: true,
                left: true,
                right: false
            }
        ];
    }

    function test_getEdgeViolations(data): void {
        MpvqcWindowUtility.contentFrame = frame;

        const violations = MpvqcWindowUtility.getEdgeViolations(frame, data.x, data.y, data.width, data.height, data.margin);

        compare(violations.bottom, data.bottom, "bottom");
        compare(violations.top, data.top, "top");
        compare(violations.left, data.left, "left");
        compare(violations.right, data.right, "right");
    }

    function test_isInBottomRegion_data(): var {
        return [
            {
                tag: "above_region",
                y: 10,
                pixels: 50,
                expected: false
            },
            {
                tag: "inside_region",
                y: 180,
                pixels: 50,
                expected: true
            }
        ];
    }

    function test_isInBottomRegion(data): void {
        MpvqcWindowUtility.contentFrame = frame;

        const result = MpvqcWindowUtility.isInBottomRegion(frame, 0, data.y, data.pixels);

        compare(result, data.expected);
    }
}
