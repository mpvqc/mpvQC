// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma Singleton

import QtQuick

import io.github.mpvqc.mpvQC.Python

QtObject {

    readonly property MpvqcWindowPropertiesViewModel viewModel: MpvqcWindowPropertiesViewModel {}
    readonly property MpvqcWindowRadiusViewModel radiusViewModel: MpvqcWindowRadiusViewModel {}

    readonly property int appWidth: viewModel.appWidth
    readonly property int appHeight: viewModel.appHeight
    readonly property bool isFullscreen: viewModel.isFullscreen
    readonly property bool isMaximized: viewModel.isMaximized
    readonly property int windowRadius: radiusViewModel.radius
    readonly property bool isMirrored: Application.layoutDirection === Qt.RightToLeft

    property Item contentFrame: null

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
