// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Window

QtObject {
    id: root

    required property int headerHeight
    required property int appBorderSize
    required property int videoWidth
    required property int videoHeight

    required property bool isAppFullScreen
    required property bool isAppMaximized
    required property string videoPath

    required property var splitViewOrientation
    required property int splitViewHandleWidth
    required property int splitViewHandleHeight
    required property int splitViewTableContainerWidth
    required property int splitViewTableContainerHeight

    readonly property int availableScreenHeight: Screen.height * 0.95
    readonly property int availableScreenWidth: Screen.width * 0.95
    readonly property bool isVideoLoaded: root.videoPath

    readonly property int videoResizeDelayAfterVideoLoading: 150

    readonly property var _delayVideoResize: Timer {
        interval: root.videoResizeDelayAfterVideoLoading

        onTriggered: {
            root.recalculateSizes();
        }
    }

    signal appWindowSizeRequested(width: int, height: int)
    signal splitViewTableSizeRequested(width: int, height: int)

    onVideoPathChanged: {
        _delayVideoResize.restart();
    }

    function recalculateSizes(): void {
        if (canResize()) {
            if (root.splitViewOrientation === Qt.Vertical) {
                recalculateSizesForVerticalAppLayout();
            } else {
                recalculateSizesForHorizontalAppLayout();
            }
        }
    }

    function canResize(): bool {
        return !root.isAppFullScreen && !root.isAppMaximized && root.isVideoLoaded && _requestedVideoSizeFitsOnScreen();
    }

    function _requestedVideoSizeFitsOnScreen(): bool {
        const fitsWidth = root.videoWidth < root.availableScreenWidth;
        const fitsHeight = root.videoHeight < root.availableScreenHeight;
        return fitsWidth && fitsHeight;
    }

    function recalculateSizesForVerticalAppLayout(): void {
        const heightWithoutTable = 2 * root.appBorderSize + root.headerHeight + root.videoHeight + root.splitViewHandleHeight;

        let newTableHeight = root.splitViewTableContainerHeight;
        while (heightWithoutTable + newTableHeight > root.availableScreenHeight) {
            newTableHeight -= 5;
        }

        const neededHeight = heightWithoutTable + newTableHeight;
        const neededWidth = root.videoWidth + 2 * root.appBorderSize;

        root.appWindowSizeRequested(neededWidth, neededHeight);
        root.splitViewTableSizeRequested(root.videoWidth, newTableHeight);
    }

    function recalculateSizesForHorizontalAppLayout(): void {
        const widthWithoutTable = 2 * root.appBorderSize + root.videoWidth + root.splitViewHandleWidth;

        let newTableWidth = root.splitViewTableContainerWidth;
        while (widthWithoutTable + newTableWidth > root.availableScreenWidth) {
            newTableWidth -= 5;
        }

        const neededHeight = 2 * root.appBorderSize + root.headerHeight + root.videoHeight;
        const neededWidth = 2 * root.appBorderSize + root.videoWidth + root.splitViewHandleWidth + newTableWidth;

        root.appWindowSizeRequested(neededWidth, neededHeight);
        root.splitViewTableSizeRequested(newTableWidth, root.videoHeight);
    }
}
