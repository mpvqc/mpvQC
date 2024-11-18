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
import QtTest

TestCase {
    id: testCase

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
                    property string themeIdentifier: "dark"
                    property int themeColorOption: 0
                }
                property var mpvqcThemesPyObject: QtObject {
                    function getThemeSummary(name: string): variant {
                        return {
                            "isDark": !!name.includes("dark")
                        };
                    }

                    function getThemeColorOption(option: int, name: string): variant {
                        return {
                            control: "blue"
                        };
                    }
                }
            }

            model: [
                {
                    "name": "dark",
                    "isDark": true,
                    "preview": "black"
                },
                {
                    "name": "light",
                    "isDark": false,
                    "preview": "white"
                }
            ]
        }
    }

    function test_initialSelection_data() {
        return [
            {
                tag: 'dark'
            },
            {
                tag: 'light'
            },
        ];
    }

    function test_initialSelection(data) {
        const control = createTemporaryObject(objectUnderTest, testCase, {
            currentThemeIdentifier: data.tag
        });
        verify(control);

        const expected = control.model.findIndex(theme => theme["name"] === data.tag);
        compare(control.currentIndex, expected);
    }

    function test_clickAndReset() {
        const control = createTemporaryObject(objectUnderTest, testCase, {
            currentThemeIdentifier: "dark"
        });
        verify(control);

        const darkIndex = control.model.findIndex(theme => theme["name"] === "dark");
        compare(control.currentIndex, darkIndex);

        const lightIndex = control.model.findIndex(theme => theme["name"] === "light");
        const selection = control.itemAtIndex(lightIndex);
        verify(selection);

        mouseClick(selection);
        compare(control.mpvqcApplication.mpvqcSettings.themeIdentifier, "light");

        control.reset();

        compare(control.mpvqcApplication.mpvqcSettings.themeIdentifier, "dark");
    }
}
