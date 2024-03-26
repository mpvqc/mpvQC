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
import QtQuick.Controls


Label {
    id: root

    required property var mpvqcApplication
    required property int time
    required property bool rowSelected
    required property bool tableInEditMode

    readonly property var mpvqcTimeFormatUtils: mpvqcApplication.mpvqcTimeFormatUtils
    readonly property var mpvqcMpvPlayerPropertiesPyObject: mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject
    readonly property var mpv: mpvqcApplication.mpvqcMpvPlayerPyObject

    property alias loader: _loader

    signal edited(int newTime)
    signal editingStarted()
    signal editingStopped()

    horizontalAlignment: Text.AlignHCenter

    text: {
        if (mpvqcMpvPlayerPropertiesPyObject.duration >= 60 * 60) {
            return mpvqcTimeFormatUtils.formatTimeToStringLong(time)
        } else {
            return mpvqcTimeFormatUtils.formatTimeToStringShort(time)
        }
    }

    function _grabFocus(): void {
        focus = true
    }

    function _startEditing(): void {
        editingStarted()
        _pauseVideo()
        _jumpTo(root.time)
        openPopup()
    }

    function _pauseVideo(): void {
        root.mpv.pause()
    }

    function _jumpTo(newTime: int): void {
        root.mpv.jump_to(newTime)
    }

    function openPopup(): void {
        _loader.sourceComponent = _editComponent
    }

    function _stopEditing(): void {
        _closePopup()
        editingStopped()
    }

    function _closePopup(): void {
        _loader.sourceComponent = undefined
    }

    MouseArea {
        anchors.fill: parent
        enabled: root.rowSelected

        onClicked: {
            if (root.tableInEditMode) {
                root._grabFocus()
            } else {
                root._startEditing()
            }
        }
    }

    Loader { id: _loader; asynchronous: false }

    Component {
        id: _editComponent

        MpvqcRowTimeLabelEditPopup {
            y: (-1/2) * (height - root.height)
            x: mirrored ? - (width - root.width) : 0
            time: root.time
            mpvqcApplication: root.mpvqcApplication

            onClosed: root._stopEditing()

            onEdited: (newTime) => root.edited(newTime)

            onEditingAborted: root._jumpTo(root.time)

            onValueChanged: (newTemporaryTime) => root._jumpTo(newTemporaryTime)
        }
    }

}
