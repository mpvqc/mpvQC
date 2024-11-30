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

    required property int currentTime
    required property int currentListIndex

    required property point openedAt

    required property int videoDuration
    required property var timeFormatFunc

    readonly property url iconNext: "qrc:/data/icons/keyboard_arrow_right_black_24dp.svg"
    readonly property url iconBefore: "qrc:/data/icons/keyboard_arrow_left_black_24dp.svg"

    readonly property url downIcon: mirrored ? iconNext : iconBefore
    readonly property url upIcon: mirrored ? iconBefore : iconNext

    property bool acceptValue: true

    signal timeEdited(index: int, newTime: int)
    signal timeKept(oldTime: int)
    signal timeTemporaryChanged(newTemporaryValue: int)

    function decrementValue(): void {
        _spinBox.decrease();
        _spinBox.valueModified();
    }

    function incrementValue(): void {
        _spinBox.increase();
        _spinBox.valueModified();
    }

    x: root.mirrored ? openedAt.x - width : openedAt.x
    y: openedAt.y

    visible: true
    dim: false
    modal: true
    width: 155
    padding: 6

    contentItem: SpinBox {
        id: _spinBox

        value: root.currentTime

        from: 0
        to: root.videoDuration > 0 ? root.videoDuration : 24 * 60 * 60 - 1

        textFromValue: value => root.timeFormatFunc(value) // qmllint disable

        bottomPadding: topPadding
        background: null

        down.indicator: ToolButton {
            x: root.mirrored ? _spinBox.width - width : 0
            height: _spinBox.height
            width: height
            icon.source: root.downIcon
            icon.width: 28
            icon.height: 28

            onPressed: root.decrementValue()
        }

        up.indicator: ToolButton {
            x: root.mirrored ? 0 : _spinBox.width - width
            height: _spinBox.height
            width: height
            icon.source: root.upIcon
            icon.width: 28
            icon.height: 28

            onPressed: root.incrementValue()
        }

        onValueModified: {
            if (root.acceptValue) {
                root.timeTemporaryChanged(_spinBox.value);
            }
        }
    }

    MouseArea {
        anchors.fill: _spinBox.contentItem
        hoverEnabled: true
        acceptedButtons: Qt.NoButton
        cursorShape: Qt.IBeamCursor

        onWheel: event => {
            if (event.angleDelta.y > 0) {
                root.incrementValue();
            } else {
                root.decrementValue();
            }
        }
    }

    onAboutToHide: {
        if (acceptValue && root.currentTime !== _spinBox.value) {
            root.timeEdited(root.currentListIndex, _spinBox.value);
        } else {
            root.timeKept(root.currentTime);
        }
    }

    Shortcut {
        sequence: "Esc"

        onActivated: {
            root.acceptValue = false;
            root.close();
        }
    }

    Shortcut {
        sequence: "Left"

        onActivated: root.decrementValue()
    }

    Shortcut {
        sequence: "Right"

        onActivated: root.incrementValue()
    }

    Shortcut {
        sequence: "Up"

        onActivated: root.incrementValue()
    }

    Shortcut {
        sequence: "Down"

        onActivated: root.decrementValue()
    }
}
