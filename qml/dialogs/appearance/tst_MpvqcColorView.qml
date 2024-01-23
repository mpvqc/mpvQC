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
import QtTest


MpvqcColorView {
    id: objectUnderTest

    mpvqcApplication: QtObject {
        property var mpvqcSettings: QtObject {
            property int primary: Material.Teal
        }
    }

    width: 400
    height: 400

    TestCase {
        name: "MpvqcColorView"
        when: windowShown

        function cleanup() {
            objectUnderTest.mpvqcApplication.mpvqcSettings.primary = -1
        }

        function test_settingSelected_data() {
            return [
                { tag: 'indigo', color: Material.Indigo },
                { tag: 'amber', color: Material.Amber },
            ]
        }

        function test_settingSelected(data) {
            objectUnderTest.mpvqcApplication.mpvqcSettings.primary = data.color

            const allSelected = findSelected()
            verify(allSelected.length === 1)

            const selected = allSelected[0]
            compare(selected.primary, data.color)
        }

        function findSelected() {
            const selected = []
            for (let idx = 0, count = objectUnderTest.count; idx < count; idx++) {
                const item = objectUnderTest.itemAtIndex(idx)
                if (item.selected) { selected.push(item) }
            }
            return selected
        }

        function test_click_data() {
            return [
                { tag: 'cyan/teal', firstColor: Material.Cyan, secondColor: Material.Teal },
                { tag: 'purple/lime', firstColor: Material.Purple, secondColor: Material.Lime },
            ]
        }

        function test_click(data) {
            const firstItem = findItemWith(data.firstColor)
            verify(firstItem)
            mouseClick(firstItem)
            compare(objectUnderTest.mpvqcApplication.mpvqcSettings.primary, data.firstColor)

            const secondItem = findItemWith(data.secondColor)
            verify(secondItem)
            mouseClick(secondItem)
            compare(objectUnderTest.mpvqcApplication.mpvqcSettings.primary, data.secondColor)

            verify(firstItem !== secondItem)
        }

        function findItemWith(primary) {
            for (let idx = 0, count = objectUnderTest.count; idx < count; idx++) {
                const item = objectUnderTest.itemAtIndex(idx)
                if (item.primary === primary) { return item }
            }
            return null
        }
    }

}
