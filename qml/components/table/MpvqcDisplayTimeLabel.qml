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


Label {
    id: control
    text: control.time
    horizontalAlignment: Text.AlignHCenter
    verticalAlignment: Text.AlignVCenter

    property string time
    property bool itemSelected

    signal clicked()

    MouseArea {
        anchors.fill: parent

        onClicked: {
            if (itemSelected) {
                openTimeEditPopup()
            } else {
                triggerClicked()
            }
        }
    }

    function openTimeEditPopup() {
        console.log("Trigger editing")
    }

    function triggerClicked() {
        control.clicked()
    }

}
