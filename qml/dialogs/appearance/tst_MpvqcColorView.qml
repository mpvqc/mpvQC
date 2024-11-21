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

    name: "MpvqcColorView"
    when: windowShown
    width: 400
    height: 400
    visible: true

    Component {
        id: objectUnderTest

        MpvqcColorView {
            id: __objectUnderTest

            width: parent.width
            mpvqcApplication: QtObject {
                property var mpvqcSettings: QtObject {
                    property string themeIdentifier: "dark"
                    property int themeColorOption: 0
                }
                property var mpvqcThemesPyObject: QtObject {
                    function getThemeSummary(name: string): variant {
                        return {
                            "isDark": true
                        };
                    }

                    function getThemeColorOption(option: int, name: string): variant {
                        return __objectUnderTest.model[option];
                    }
                }
            }

            model: [
                {
                    "foreground": "black",
                    "background": "black",
                    "rowHighlight": "black"
                },
                {
                    "foreground": "grey",
                    "background": "grey",
                    "rowHighlight": "grey"
                },
                {
                    "foreground": "white",
                    "background": "white",
                    "rowHighlight": "white"
                }
            ]
        }
    }

    function test_initialSelection_data() {
        return [
            {
                tag: 1
            },
            {
                tag: 2
            },
        ];
    }

    function test_initialSelection(data) {
        const control = createTemporaryObject(objectUnderTest, testCase, {
            "mpvqcSettings.themeColorOption": data.tag
        });
        verify(control);
        compare(control.currentIndex, data.tag);
    }

    function test_clickAndReset() {
        const initialIndex = 1;
        const temporaryIndex = 2;

        const control = createTemporaryObject(objectUnderTest, testCase, {
            "mpvqcSettings.themeColorOption": initialIndex
        });
        verify(control);
        compare(control.currentIndex, initialIndex);

        const selection = control.itemAtIndex(temporaryIndex);
        verify(selection);

        mouseClick(selection);
        compare(control.mpvqcApplication.mpvqcSettings.themeColorOption, temporaryIndex);

        control.reset();

        compare(control.mpvqcApplication.mpvqcSettings.themeColorOption, initialIndex);
    }
}
