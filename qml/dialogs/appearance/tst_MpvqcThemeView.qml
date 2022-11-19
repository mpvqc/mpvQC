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


MpvqcThemeView {
    id: objectUnderTest

    mpvqcApplication: QtObject {
        property var mpvqcSettings: QtObject {
            property int theme: Material.Dark
        }
    }

    width: 400
    height: 400

    TestCase {
        name: "MpvqcThemeView"
        when: windowShown

        function cleanup() {
            objectUnderTest.mpvqcApplication.mpvqcSettings.theme = -1
        }

        function test_settingSelected_data() {
            return [
                { tag: 'dark', color: Material.Dark },
                { tag: 'light', color: Material.Light },
            ]
        }

        function test_settingSelected(data) {
            objectUnderTest.mpvqcApplication.mpvqcSettings.theme = data.color

            const allSelected = findSelected()
            verify(allSelected.length === 1)

            const selected = allSelected[0]
            compare(selected.theme, data.color)
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
                { tag: 'dark', firstColor: Material.Dark, secondColor: Material.Light },
                { tag: 'light', firstColor: Material.Light, secondColor: Material.Dark },
            ]
        }

        function test_click(data) {
            const firstItem = findItemWith(data.firstColor)
            verify(firstItem)
            mouseClick(firstItem)
            compare(objectUnderTest.mpvqcApplication.mpvqcSettings.theme, data.firstColor)

            const secondItem = findItemWith(data.secondColor)
            verify(secondItem)
            mouseClick(secondItem)
            compare(objectUnderTest.mpvqcApplication.mpvqcSettings.theme, data.secondColor)

            verify(firstItem !== secondItem)
        }

        function findItemWith(theme) {
            for (let idx = 0, count = objectUnderTest.count; idx < count; idx++) {
                const item = objectUnderTest.itemAtIndex(idx)
                if (item.theme === theme) { return item }
            }
            return null
        }
    }

}
