// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma Singleton

import QtQuick

import pyobjects

QtObject {

    readonly property MpvqcWindowPropertiesBackend windowPropertiesBackend: MpvqcWindowPropertiesBackend {}

    readonly property int appWidth: windowPropertiesBackend.appWidth
    readonly property int appHeight: windowPropertiesBackend.appHeight
    readonly property bool isFullscreen: windowPropertiesBackend.isFullscreen
    readonly property bool isMaximized: windowPropertiesBackend.isMaximized

    /**
     * Checks if local coordinates of an item are within the bottom region of the window.
     * @param {Item} item - The item whose local coordinates to convert
     * @param {real} localX - The x-coordinate relative to the item
     * @param {real} localY - The y-coordinate relative to the item
     * @param {int} pixels - The height of the bottom region in pixels
     * @returns {bool} True if the coordinates are in the bottom region
     */
    function isInBottomRegion(item, localX: real, localY: real, pixels: int): bool {
        const windowCoords = item.mapToItem(null, localX, localY);
        const windowHeight = item.Window.window.height;
        return windowCoords.y >= (windowHeight - pixels);
    }

    /**
     * Checks which window edges would be violated by positioning an item at the given coordinates.
     * @param {Item} item - The item whose local coordinates to convert
     * @param {real} localX - The x-coordinate relative to the item
     * @param {real} localY - The y-coordinate relative to the item
     * @param {real} width - The width of the element to be positioned
     * @param {real} height - The height of the element to be positioned
     * @param {int} margin - The margin/padding from window edges
     * @returns {object} Object with boolean properties: bottom, top, right, left
     */
    function getEdgeViolations(item: Item, localX: real, localY: real, width: real, height: real, margin: int): var {
        const windowCoords = item.mapToItem(null, localX, localY);
        const windowHeight = item.Window.window.height;
        const windowWidth = item.Window.window.width;

        return {
            bottom: windowCoords.y + height + margin >= windowHeight,
            top: windowCoords.y - margin <= 0,
            right: windowCoords.x + width + margin >= windowWidth,
            left: windowCoords.x - margin <= 0
        };
    }
}
