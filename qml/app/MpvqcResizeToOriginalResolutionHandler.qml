/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

import QtQuick
import QtQuick.Window

import dialogs


Item {
    id: root

    required property var mpvqcApplication
    required property var header
    required property var footer
    required property var splitView

    readonly property var mpvqcMpvPlayerPropertiesPyObject: mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject
    readonly property var playerContainer: splitView.playerContainer
    readonly property var tableContainer: splitView.tableContainer

    readonly property int windowBorder: mpvqcApplication.windowBorder
    readonly property int videoHeight: mpvqcMpvPlayerPropertiesPyObject.height
    readonly property int videoWidth: mpvqcMpvPlayerPropertiesPyObject.width

    readonly property int splitViewHandleHeight: splitView.height
            - playerContainer.height
            - tableContainer.height

    property int availableScreenHeight: Screen.height * 0.95
    property int availableScreenWidth: Screen.width * 0.95

    function resizeVideo() {
        if (root.canResize()) {
            root.resizeVideoInVerticalSplitView()
        }
    }

    function canResize(): bool {
        return !mpvqcApplication.fullscreen
            && !mpvqcApplication.maximized
            && mpvqcMpvPlayerPropertiesPyObject.video_loaded
            && requestedVideoSizeFitsOnScreen()
    }

    function requestedVideoSizeFitsOnScreen(): bool {
        const fitsWidth = videoWidth < availableScreenWidth
        const fitsHeight = videoHeight < availableScreenHeight
        return fitsWidth && fitsHeight
    }

    function resizeVideoInVerticalSplitView() {
        const heightWithoutTable = windowBorder
            + header.height
            + videoHeight
            + splitViewHandleHeight
            + footer.height
            + windowBorder

        let newTableHeight = tableContainer.height
        while (heightWithoutTable + newTableHeight > availableScreenHeight) {
            newTableHeight -= 5
        }

        const neededHeight = heightWithoutTable + newTableHeight
        const neededWidth = videoWidth + 2 * windowBorder

        mpvqcApplication.width = neededWidth
        mpvqcApplication.height = neededHeight

        playerContainer.setPreferredSizes(videoWidth, videoHeight)
        tableContainer.setPreferredSizes(videoWidth, newTableHeight)
    }

}
