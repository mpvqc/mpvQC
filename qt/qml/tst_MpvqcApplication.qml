// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    name: "MpvqcApplication"

    readonly property MpvqcTestBridge bridge: MpvqcTestBridge {}

    property Component appComponent: Qt.createComponent("MpvqcApplication.qml")

    property var _originalWindowViewModel: null

    function makeWindow(drawsOwnFrame: bool, margin: int): var {
        windowViewModelMock.drawsOwnFrame = drawsOwnFrame;
        windowViewModelMock.dropShadowMargin = margin;
        MpvqcWindowUtility._viewModel = windowViewModelMock;

        const window = createTemporaryObject(appComponent, testCase);
        verify(window);
        return window;
    }

    function init(): void {
        if (!_originalWindowViewModel) {
            _originalWindowViewModel = MpvqcWindowUtility._viewModel;
        }
    }

    function cleanup(): void {
        MpvqcWindowUtility._viewModel = _originalWindowViewModel;
        MpvqcWindowUtility.contentFrame = null;
        bridge.switchPlatform("headless");
    }

    function test_minimumSizeCoversDropShadowMargin_data(): var {
        return [
            {
                tag: "no-margin",
                drawsOwnFrame: false,
                margin: 0,
                expectedMinimumWidth: 960,
                expectedMinimumHeight: 540
            },
            {
                tag: "drop-shadow-margin",
                drawsOwnFrame: true,
                margin: 88,
                expectedMinimumWidth: 1136,
                expectedMinimumHeight: 716
            }
        ];
    }

    function test_minimumSizeCoversDropShadowMargin(data): void {
        const window = makeWindow(data.drawsOwnFrame, data.margin);

        compare(window.minimumWidth, data.expectedMinimumWidth);
        compare(window.minimumHeight, data.expectedMinimumHeight);
    }

    function test_frameClipsOverflowingContentOnlyWithOwnFrame_data(): var {
        return [
            {
                tag: "own-frame",
                drawsOwnFrame: true,
                margin: 88,
                expectedClip: true
            },
            {
                tag: "no-own-frame",
                drawsOwnFrame: false,
                margin: 0,
                expectedClip: false
            }
        ];
    }

    function test_frameClipsOverflowingContentOnlyWithOwnFrame(data): void {
        const window = makeWindow(data.drawsOwnFrame, data.margin);

        const frame = findChild(window, "windowFrame");
        verify(frame, "windowFrame not found");
        compare(frame.clip, data.expectedClip, "with an own frame, overflowing content would paint into the drop shadow margin, so the frame must clip; without one it must not");
    }

    function test_platformDrivesFlagsAndColor_data(): var {
        return [
            {
                tag: "windows",
                platform: "windows",
                frameless: false,
                transparent: false
            },
            {
                tag: "linux-desktop",
                platform: "linux-desktop",
                frameless: true,
                transparent: true
            },
            {
                tag: "linux-tiling",
                platform: "linux-tiling",
                frameless: true,
                transparent: false
            }
        ];
    }

    function test_platformDrivesFlagsAndColor(data): void {
        bridge.switchPlatform(data.platform);
        const window = makeWindow(false, 0);

        compare(Boolean(window.flags & Qt.FramelessWindowHint), data.frameless);
        compare(Boolean(window.flags & Qt.CustomizeWindowHint), !data.frameless);
        compare(window.color.a === 0, data.transparent);
    }

    QtObject {
        id: windowViewModelMock

        readonly property int windowGeometryWidth: 1280
        readonly property int windowGeometryHeight: 720
        readonly property bool isFullscreen: false
        readonly property bool isMaximized: false
        readonly property bool isMainWindowFocused: true

        property bool drawsOwnFrame: false
        property int dropShadowMargin: 0
    }
}
