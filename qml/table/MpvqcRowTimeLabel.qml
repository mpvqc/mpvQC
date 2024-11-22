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

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls

Label {
    id: root

    required property var mpvqcApplication
    required property int time
    required property bool rowSelected
    required property bool tableInEditMode

    readonly property var mpvqcUtilityPyObject: mpvqcApplication.mpvqcUtilityPyObject
    readonly property var mpvqcMpvPlayerPropertiesPyObject: mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject
    readonly property var mpv: mpvqcApplication.mpvqcMpvPlayerPyObject

    property var popup: undefined
    readonly property var popupFactory: Component {
        MpvqcRowTimeLabelEditPopup {
            readonly property int additionalSpace: 7

            y: additionalSpace
            x: mirrored ? -(width - root.width + additionalSpace) : additionalSpace

            transformOrigin: mirrored ? Popup.TopRight : Popup.TopLeft

            time: root.time
            mpvqcApplication: root.mpvqcApplication

            onClosed: root.editingStopped()

            onEdited: newTime => root.edited(newTime)

            onEditingAborted: root._jumpTo(root.time)

            onValueChanged: newTemporaryTime => root._jumpTo(newTemporaryTime)
        }
    }

    signal edited(int newTime)
    signal editingStarted
    signal editingStopped

    horizontalAlignment: Text.AlignHCenter

    text: {
        if (mpvqcMpvPlayerPropertiesPyObject.duration >= 60 * 60) {
            return mpvqcUtilityPyObject.formatTimeToStringLong(time);
        } else {
            return mpvqcUtilityPyObject.formatTimeToStringShort(time);
        }
    }

    function _grabFocus(): void {
        focus = true;
    }

    function _startEditing(mouseX: int, mouseY: int): void {
        editingStarted();
        _pauseVideo();
        _jumpTo(root.time);
        openPopup(mouseX, mouseY);
    }

    function _pauseVideo(): void {
        root.mpv.pause();
    }

    function _jumpTo(newTime: int): void {
        root.mpv.jump_to(newTime);
    }

    function openPopup(mouseX: int, mouseY: int): void {
        const mirrored = LayoutMirroring.enabled;
        popup = popupFactory.createObject(root);
        popup.closed.connect(popup.destroy);
        popup.y = mouseY;
        popup.x = mirrored ? mouseX - popup.width : mouseX;
        popup.transformOrigin = mirrored ? Popup.TopRight : Popup.TopLeft;
        popup.open();
    }

    MouseArea {
        anchors.fill: parent
        enabled: root.rowSelected

        onPressed: {
            if (root.tableInEditMode) {
                root._grabFocus();
            } else {
                root._startEditing(mouseX, mouseY);
            }
        }
    }
}
