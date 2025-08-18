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

    readonly property int timeoutLongCI: 750

    when: windowShown
    name: "MpvqcFooter"
    visible: true
    width: 400
    height: 400

    Component {
        id: objectUnderTest

        MpvqcFooter {
            id: objectUnderTest

            selectedCommentIndex: 0
            totalCommentCount: 10

            anchors {
                left: parent.left
                right: parent.right
                bottom: parent.bottom
            }

            mpvqcApplication: QtObject {
                property bool maximized: false
                property var mpvqcSettings: QtObject {
                    property int timeFormat: -1
                    property bool statusbarPercentage: false
                }
                property var mpvqcMpvPlayerPropertiesPyObject: QtObject {
                    property bool video_loaded: true
                    property real percent_pos: 10.0
                    property real duration: 10.0
                    property real time_pos: 5
                    property real time_remaining: 5
                }
                property var mpvqcLabelWidthCalculator: QtObject {
                    function calculateWidthFor(items, parent) {
                        return 200;
                    }
                }
                property var mpvqcUtilityPyObject: QtObject {
                    function formatTimeToStringLong(seconds) {
                        return `time:${seconds}`;
                    }
                    function formatTimeToStringShort(seconds) {
                        return `time:${seconds}`;
                    }
                }
            }
        }
    }

    function test_toggle_percent(): void {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);
        waitForRendering(control);

        mouseClick(testCase, 395, 395);
        wait(timeoutLongCI);

        verify(!control.percentLabelText.visible);

        mouseClick(testCase, 395, 360);
        tryVerify(() => control.percentLabelText.visible);
        compare(control.percentLabelText.text, "10%");
    }

    function test_timeMode_data(): list<var> {
        return [
            {
                tag: "hide-time",
                expected: "",
                coordinates: Qt.point(395, 300)
            },
            {
                tag: "remaining-time",
                expected: "-time:5",
                coordinates: Qt.point(395, 265)
            },
            {
                tag: "current-time",
                expected: "time:5",
                coordinates: Qt.point(395, 220)
            },
            {
                tag: "default",
                expected: "time:5/time:10",
                coordinates: Qt.point(395, 185)
            },
        ];
    }

    function test_timeMode(data): void {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);
        waitForRendering(control);

        mouseClick(testCase, 395, 395);
        wait(timeoutLongCI);

        mouseClick(testCase, data.coordinates.x, data.coordinates.y);
        tryCompare(control.videoTimeLabelText, "text", data.expected);
    }

    function test_rowSelection(): void {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);
        waitForRendering(control);

        compare(control.rowSelectionLabelText.text, "1/10");
    }
}
