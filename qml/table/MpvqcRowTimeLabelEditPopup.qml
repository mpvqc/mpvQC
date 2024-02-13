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


Popup {
    id: root

    required property var mpvqcApplication
    required property int time

    property bool acceptValue: true

    property alias spinBox: _spinBox

    signal edited(int newTime)
    signal editingAborted()
    signal valueChanged(int newTemporaryValue)

    visible: true
    dim: false
    modal: true
    width: 155
    padding: 6

    contentItem: MpvqcRowTimeLabelEditPopupSpinBox {
        id: _spinBox

        value: root.time
        mpvqcApplication: root.mpvqcApplication

        onValueModified: {
            if (root.acceptValue) {
                root.valueChanged(_spinBox.value)
            }
        }
    }

    onAboutToHide: {
        if (acceptValue) {
            root.edited(_spinBox.value)
        } else {
            root.editingAborted()
        }
    }

    onActiveFocusChanged: {
        if (!activeFocus) {
            root.close()
        }
    }

    Shortcut {
        sequence: "Esc"

        onActivated: {
            root.acceptValue = false
            root.close()
        }
    }

    Shortcut {
        sequence: 'Left'

        onActivated: _spinBox.decrementValue()
    }

    Shortcut {
        sequence: 'Right'

        onActivated: _spinBox.incrementValue()
    }

    Shortcut {
        sequence: 'Up'

        onActivated: _spinBox.incrementValue()
    }

    Shortcut {
        sequence: 'Down'

        onActivated: _spinBox.decrementValue()
    }

    Component.onCompleted: {
        _spinBox.forceActiveFocus()
    }

}
