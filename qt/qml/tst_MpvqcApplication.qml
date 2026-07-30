// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    name: "MpvqcApplication"

    property Component appComponent: Qt.createComponent("MpvqcApplication.qml")

    property var _originalWindowViewModel: null

    function makeWindow(margin: int): var {
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
    }

    function test_minimumSizeCoversDropShadowMargin_data(): var {
        return [
            {
                tag: "no-margin",
                margin: 0,
                expectedMinimumWidth: 960,
                expectedMinimumHeight: 540
            },
            {
                tag: "drop-shadow-margin",
                margin: 88,
                expectedMinimumWidth: 1136,
                expectedMinimumHeight: 716
            }
        ];
    }

    function test_minimumSizeCoversDropShadowMargin(data): void {
        const window = makeWindow(data.margin);

        compare(window.minimumWidth, data.expectedMinimumWidth);
        compare(window.minimumHeight, data.expectedMinimumHeight);
    }

    function test_frameClipsOverflowingContent(): void {
        const window = makeWindow(88);

        const frame = findChild(window, "windowFrame");
        verify(frame, "windowFrame not found");
        verify(frame.clip, "the frame must clip, otherwise content paints into the drop shadow margin");
    }

    QtObject {
        id: windowViewModelMock

        readonly property int windowGeometryWidth: 1280
        readonly property int windowGeometryHeight: 720
        readonly property bool isFullscreen: false
        readonly property bool isMaximized: false
        readonly property int radius: 0
        readonly property bool keepsNativeFrame: false
        readonly property bool drawsDropShadow: true
        readonly property bool isMainWindowFocused: true

        property int dropShadowMargin: 0
    }
}
