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
import QtQuick.Controls.Material

Menu {

    readonly property bool mMirrored: count > 0 && (itemAt(0) as MenuItem).mirrored

    /**
     * Qt cannot reliably position menus in RTL layouts. Therefore, we need to work around this.
     * Implementations of this menu need to configure if they want to manage positioning on their own.
     */
    property bool implementationManagesPositioning: false

    z: 2
    popupType: Qt.platform.os === "windows" ? Popup.Window : Popup.Item
    dim: false

    width: calculateMenuWidths()

    function calculateMenuWidths(): int {
        // Adapted from: https://martin.rpdev.net/2018/03/13/qt-quick-controls-2-automatically-set-the-width-of-menus.html
        let result = 0;
        let padding = 0;
        for (let i = 0; i < count; ++i) {
            let item = itemAt(i) as MenuItem;

            if (item && !isMenuSeparator(item)) {
                result = Math.max(item.contentItem.implicitWidth, result);
                padding = Math.max(item.padding, padding);
            }
        }
        return (result + padding * 2) * 1.03;
    }

    function isMenuSeparator(item: Item): bool {
        return item instanceof MenuSeparator;
    }

    function _positionMenu(): void {
        if (mMirrored) {
            x = -width + parent.width;
        } else {
            x = 0;
        }
    }

    onAboutToShow: {
        // fixme: Workaround QTBUG-131786 to fake modal behavior on Windows
        enableFakeModal(); // qmllint disable

        if (!implementationManagesPositioning) {
            _positionMenu();
        }
    }

    onAboutToHide: {
        // fixme: Workaround QTBUG-131786 to fake modal behavior on Windows
        disableFakeModal(); // qmllint disable
    }
}
