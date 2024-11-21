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

MpvqcVideoPercentLabel {
    id: objectUnderTest

    width: 400
    height: 400

    mpvqcApplication: QtObject {
        property var mpvqcSettings: QtObject {
            property bool statusbarPercentage: false
        }
        property var mpvqcMpvPlayerPropertiesPyObject: QtObject {
            property real percent_pos: 42.42
            property bool video_loaded: false
        }
    }

    TestCase {
        name: "MpvqcVideoPercentLabel"
        when: windowShown

        function init() {
            objectUnderTest.mpvqcApplication.mpvqcSettings.statusbarPercentage = false;
            objectUnderTest.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.video_loaded = false;
        }

        function test_text(data) {
            objectUnderTest.mpvqcApplication.mpvqcSettings.statusbarPercentage = true;
            objectUnderTest.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.video_loaded = true;
            compare(objectUnderTest.text, '42%');
        }

        function test_visibility_data() {
            return [
                {
                    tag: 'visable',
                    statusbarPercentage: true,
                    video_loaded: true,
                    expected: true
                },
                {
                    tag: 'disabled',
                    statusbarPercentage: false,
                    video_loaded: true,
                    expected: false
                },
                {
                    tag: 'no-video',
                    statusbarPercentage: true,
                    video_loaded: false,
                    expected: false
                },
                {
                    tag: 'neither',
                    statusbarPercentage: false,
                    video_loaded: false,
                    expected: false
                },
            ];
        }

        function test_visibility(data) {
            objectUnderTest.mpvqcApplication.mpvqcSettings.statusbarPercentage = data.statusbarPercentage;
            objectUnderTest.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.video_loaded = data.video_loaded;
            compare(objectUnderTest.visible, data.expected);
        }
    }
}
