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
import QtQuick.Controls.Material
import QtQuick.Layouts

Dialog {
    id: root

    required property var mpvqcApplication

    popupType: Qt.platform.os === "windows" ? Popup.Window : Popup.Item
    anchors.centerIn: parent
    parent: mpvqcApplication.contentItem
    contentWidth: 370
    contentHeight: 450
    modal: true
    dim: false
    z: 2
    closePolicy: Popup.CloseOnEscape
    standardButtons: Dialog.Ok

}
