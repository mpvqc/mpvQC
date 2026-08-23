// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase
    name: "MpvqcWindowUtility"

    property var _originalViewModel: null

    function init(): void {
        if (!_originalViewModel) {
            _originalViewModel = MpvqcWindowUtility._viewModel;
        }
    }

    function cleanup(): void {
        MpvqcWindowUtility._viewModel = _originalViewModel;
        MpvqcWindowUtility.contentFrame = null;
    }

    function test_windowRadiusFollowsOwnFrame_data(): var {
        return [
            {
                tag: "no_own_frame_has_square_corners",
                drawsOwnFrame: false,
                expectedRadius: 0
            },
            {
                tag: "own_frame_has_rounded_corners",
                drawsOwnFrame: true,
                expectedRadius: 8
            }
        ];
    }

    function test_windowRadiusFollowsOwnFrame(data): void {
        windowViewModelMock.drawsOwnFrame = data.drawsOwnFrame;
        MpvqcWindowUtility._viewModel = windowViewModelMock;

        compare(MpvqcWindowUtility.windowRadius, data.expectedRadius);
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

    Item {
        id: frame
        width: 300
        height: 200
    }

    QtObject {
        id: windowViewModelMock

        readonly property int windowGeometryWidth: 1280
        readonly property int windowGeometryHeight: 720
        readonly property bool isFullscreen: false
        readonly property bool isMaximized: false
        readonly property int dropShadowMargin: 0
        readonly property bool isMainWindowFocused: true

        property bool drawsOwnFrame: false
    }
}
