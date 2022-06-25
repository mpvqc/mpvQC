/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick
import QtQuick.Controls
import helpers


TextField {
    id: control
    selectByMouse: true
    leftPadding: control.borderPadding
    rightPadding: control.borderPadding
    horizontalAlignment: Text.AlignLeft
    bottomPadding: topPadding
    background: Rectangle {
        anchors.fill: parent
        anchors.topMargin: control.borderPadding
        anchors.bottomMargin: control.borderPadding
        color: Material.background
    }

    required property int borderPadding
    property bool cancelling: false
    property int minimalEditingTime: 250
    property bool minimalEditingTimeExpired: false

    signal done()
    signal edited(string comment)

    Component.onCompleted: {
        focusTextField()
        MpvqcTimer.scheduleOnceAfter(minimalEditingTime, expireMinimalEditingTime)
    }

    Keys.onEscapePressed: {
        cancelling = true
        focus = false
    }

    onEditingFinished: (event) => {
        if (!minimalEditingTimeExpired) {
            focusTextField()
            return
        }
        if (!cancelling) {
            triggerEdited(control.text)
        }
        triggerDone()
    }

    function focusTextField() {
        cursorPosition = text.length
        forceActiveFocus()
    }

    function expireMinimalEditingTime() {
        minimalEditingTimeExpired = true
    }

    function triggerEdited(comment) {
        control.edited(comment)
    }

    function triggerDone() {
        control.done()
    }

}
