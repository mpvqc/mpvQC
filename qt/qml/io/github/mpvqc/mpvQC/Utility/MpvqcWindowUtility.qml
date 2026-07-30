// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma Singleton

import QtQuick

import io.github.mpvqc.mpvQC.Python

QtObject {

    // Mutable, not readonly: the QML test harness swaps in a fresh view model per test.
    property var _viewModel: MpvqcWindowViewModel {}

    readonly property int windowGeometryWidth: _viewModel.windowGeometryWidth
    readonly property int windowGeometryHeight: _viewModel.windowGeometryHeight
    readonly property bool isFullscreen: _viewModel.isFullscreen
    readonly property bool isMaximized: _viewModel.isMaximized
    readonly property int windowRadius: _viewModel.radius
    readonly property int dropShadowMargin: _viewModel.dropShadowMargin
    readonly property bool keepsNativeFrame: _viewModel.keepsNativeFrame
    readonly property bool drawsDropShadow: _viewModel.drawsDropShadow
    readonly property bool isMainWindowFocused: _viewModel.isMainWindowFocused
    readonly property bool isMirrored: Application.layoutDirection === Qt.RightToLeft

    property Item contentFrame: null

    function minimize(): void {
        _viewModel.minimize();
    }

    function toggleMaximized(): void {
        _viewModel.toggleMaximized();
    }

    function toggleFullScreen(): void {
        _viewModel.toggleFullScreen();
    }

    function disableFullScreen(): void {
        _viewModel.disableFullScreen();
    }

    /**
     * Resolves the visible content frame to measure against. Falls back to the
     * window's content item when no frame is registered (e.g. in tests).
     */
    function _visibleFrame(item: Item): Item {
        return contentFrame ?? item.Window.window.contentItem;
    }

    /**
     * Checks if local coordinates of an item are within the bottom region of the visible content.
     */
    function isInBottomRegion(item: Item, localX: real, localY: real, pixels: int): bool {
        const frame = _visibleFrame(item);
        const coords = item.mapToItem(frame, localX, localY);
        return coords.y >= frame.height - pixels;
    }

    /**
     * Checks which visible-content edges would be violated by positioning an item at the given coordinates.
     */
    function getEdgeViolations(item: Item, localX: real, localY: real, width: real, height: real, margin: int): var {
        const frame = _visibleFrame(item);
        const coords = item.mapToItem(frame, localX, localY);

        return {
            bottom: coords.y + height + margin >= frame.height,
            top: coords.y - margin <= 0,
            right: coords.x + width + margin >= frame.width,
            left: coords.x - margin <= 0
        };
    }
}
