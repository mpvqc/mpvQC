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

    readonly property int initialTheme: Material.Dark

    name: "MpvqcThemeView"
    when: windowShown
    width: 400
    height: 400
    visible: true

    Component {
        id: objectUnderTest

        MpvqcThemeView {
            width: parent.width
            mpvqcApplication: QtObject {
                property var mpvqcSettings: QtObject {
                    property int theme: testCase.initialTheme
                }
            }

            function findSelected() {
                for (let idx = 0; idx < this.count; idx++) {
                    const item = this.itemAtIndex(idx)
                    if (item.selected) return item
                }
                return null
            }

            function findItemWithTheme(theme) {
                for (let idx = 0; idx < this.count; idx++) {
                    const item = this.itemAtIndex(idx)
                    if (item.theme === theme) return item
                }
                return null
            }
        }
    }

    function test_themeFromSettingsSelected_data() {
        return [
            { tag: 'dark', color: Material.Dark },
            { tag: 'light', color: Material.Light },
        ]
    }

    function test_themeFromSettingsSelected(data) {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        control.mpvqcApplication.mpvqcSettings.theme = data.color

        const selected = control.findSelected()
        verify(selected)

        compare(selected.theme, data.color)
    }

    function test_click() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        compare(control.mpvqcApplication.mpvqcSettings.theme, testCase.initialTheme)

        const selection = control.findItemWithTheme(Material.Light)
        verify(selection)
        mouseClick(selection)
        compare(control.mpvqcApplication.mpvqcSettings.theme, Material.Light)
    }

    function test_reset() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        compare(control.mpvqcApplication.mpvqcSettings.theme, testCase.initialTheme)

        const selection = control.findItemWithTheme(Material.Light)
        verify(selection)
        mouseClick(selection)
        compare(control.mpvqcApplication.mpvqcSettings.theme, Material.Light)

        control.reset()

        compare(control.mpvqcApplication.mpvqcSettings.theme, testCase.initialTheme)
    }

}
