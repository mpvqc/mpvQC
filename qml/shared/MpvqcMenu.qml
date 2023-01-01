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


Menu {
    id: root

    property real additionalPadding

    width: { // Adapted from: https://martin.rpdev.net/2018/03/13/qt-quick-controls-2-automatically-set-the-width-of-menus.html
        let result = 0
        let padding = 0
        for (let i = 0; i < count; ++i) {
            let item = itemAt(i)

            if (!isMenuSeparator(item)) {
                result = Math.max(item.contentItem.implicitWidth, result)
                padding = Math.max(item.padding, padding)
            }
        }
        return result + padding * 2
    }

    delegate: MenuItem {
        id: control

        property bool hasIcon: control.icon.source.toString() !== ''

        // Customized from src/quickcontrols/material/MenuItem.qml
        // We added additional padding if there's no icon and control is not checkable
        contentItem: IconLabel {
            readonly property real arrowPadding: control.subMenu && control.arrow ? control.arrow.width + control.spacing : 0
            readonly property real indicatorPadding: control.checkable && control.indicator ? control.indicator.width + control.spacing : 0
            readonly property real iconPadding: !control.hasIcon && !control.checkable ? root.additionalPadding : 0
            leftPadding: !control.mirrored ? indicatorPadding + iconPadding : arrowPadding
            rightPadding: control.mirrored ? indicatorPadding + iconPadding : arrowPadding

            spacing: control.spacing
            mirrored: control.mirrored
            display: control.display
            alignment: Qt.AlignLeft

            icon: control.icon
            text: control.text
            font: control.font
            color: control.enabled ? control.Material.foreground : control.Material.hintTextColor
        }

        Component.onCompleted: calculateLargestAdditionalPadding()

        function calculateLargestAdditionalPadding() {
            if (control.hasIcon) {
                root.additionalPadding = Math.max(root.additionalPadding, control.icon.width + control.spacing)
            }
        }

    }

    function isMenuSeparator(item: Item): bool {
        return item instanceof MenuSeparator
    }

}
