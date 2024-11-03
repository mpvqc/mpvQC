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


TestCase {
    id: testCase

    readonly property int initialColor: Material.Teal

    name: "MpvqcColorView"
    when: windowShown
    width: 400
    height: 400
    visible: true

    Component {
        id: objectUnderTest

        MpvqcColorView {
            width: parent.width
            mpvqcApplication: QtObject {
                property var mpvqcSettings: QtObject {
                    property int primary: testCase.initialColor
                }
            }

            function findSelected() {
                for (let idx = 0; idx < this.count; idx++) {
                    const item = this.itemAtIndex(idx)
                    if (item.selected) return item
                }
                return null
            }

            function findItemWithColor(primary) {
                for (let idx = 0; idx < this.count; idx++) {
                    const item = this.itemAtIndex(idx)
                    if (item.primary === primary) {
                        return item
                    }
                }
                return null
            }
        }
    }

    function test_colorFromSettingsSelected_data() {
        return [
            { tag: 'indigo', color: Material.Indigo },
            { tag: 'amber', color: Material.Amber },
        ]
    }

    function test_colorFromSettingsSelected(data) {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        control.mpvqcApplication.mpvqcSettings.primary = data.color

        const selected = control.findSelected()
        verify(selected)

        compare(selected.primary, data.color)
    }

    function test_click_data() {
        return [
            { tag: 'cyan/teal', firstColor: Material.Cyan, secondColor: Material.Teal },
            { tag: 'purple/lime', firstColor: Material.Purple, secondColor: Material.Lime },
        ]
    }

    function test_click(data) {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const selection1 = control.findItemWithColor(data.firstColor)
        verify(selection1)
        mouseClick(selection1)
        compare(control.mpvqcApplication.mpvqcSettings.primary, data.firstColor)

        const selection2 = control.findItemWithColor(data.secondColor)
        verify(selection2)
        mouseClick(selection2)
        compare(control.mpvqcApplication.mpvqcSettings.primary, data.secondColor)

        verify(selection1 !== selection2)
    }

    function test_reset() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        compare(control.mpvqcApplication.mpvqcSettings.primary, testCase.initialColor)

        const selection = control.findItemWithColor(Material.Purple)
        verify(selection)
        mouseClick(selection)
        compare(control.mpvqcApplication.mpvqcSettings.primary, Material.Purple)

        control.reset()
        compare(control.mpvqcApplication.mpvqcSettings.primary, testCase.initialColor)
    }

}
