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
import QtQuick.Layouts
import components
import helpers


Popup {
    id: popup
    dim: false
    modal: true
    width: 180
    padding: 6
    closePolicy: Popup.CloseOnPressOutside

    property int currentTime
    property bool _canceling: false

    signal edited(int time)
    signal editingAborted()
    signal valueChanged(int time)

    contentItem: SpinBox {
        id: spinBox
        width: popup.width
        editable: true
        from: 0
        to: 3600 * 24 -1
        value: popup.currentTime
        anchors.centerIn: parent
        textFromValue: (value) => MpvqcTimeFormatUtils.formatTimeToString(value)
        valueFromText: (text) => MpvqcTimeFormatUtils.extractSecondsFrom(text)
        validator: RegularExpressionValidator {
            regularExpression: /^([\d:]{8})$/
        }
        up.indicator: MpvqcIncrementButton {
            x: spinBox.mirrored ? 0 : parent.width - width
            height: spinBox.height

            onClicked: {
                spinBox.increase()
                spinBox.valueModified()
            }
        }
        down.indicator: MpvqcDecrementButton {
            x: spinBox.mirrored ? parent.width - width : 0
            height: spinBox.height

            onClicked: {
                spinBox.decrease()
                spinBox.valueModified()
            }
        }

        onValueModified: {
            triggerValueChanged()
        }
    }

    function triggerValueChanged() {
        if (!_canceling) {
            popup.valueChanged(spinBox.value)
        }
    }

    Shortcut {
        sequence: "Esc"

        onActivated: {
            _canceling = true
            popup.close()
        }
    }

    onAboutToHide: {
        if (_canceling) {
            triggerEditingAborted()
        } else {
            triggerEdited()
        }
    }

    function triggerEditingAborted() {
        popup.editingAborted()
    }

    function triggerEdited() {
        popup.edited(spinBox.value)
    }

}
