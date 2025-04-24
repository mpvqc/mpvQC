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

import settings

TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcWindowTitle"

    Component {
        id: objectUnderTest

        MpvqcWindowTitle {
            mpvqcApplication: QtObject {
                property var mpvqcManager: QtObject {
                    property bool saved: true
                }
                property var mpvqcSettings: QtObject {
                    property var windowTitleFormat: MpvqcSettings.WindowTitleFormat.DEFAULT
                }
                property var mpvqcMpvPlayerPropertiesPyObject: QtObject {
                    property bool video_loaded: false
                    property string filename: "video-name"
                    property string path: "video-path"
                }
            }
        }
    }

    function test_title() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        Application.name = "mpvQC";

        control.mpvqcApplication.mpvqcSettings.windowTitleFormat = MpvqcSettings.WindowTitleFormat.DEFAULT;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.video_loaded = false;
        compare(control.text, "mpvQC");

        control.mpvqcApplication.mpvqcSettings.windowTitleFormat = MpvqcSettings.WindowTitleFormat.FILE_NAME;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.video_loaded = false;
        compare(control.text, "mpvQC");

        control.mpvqcApplication.mpvqcSettings.windowTitleFormat = MpvqcSettings.WindowTitleFormat.FILE_PATH;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.video_loaded = false;
        compare(control.text, "mpvQC");

        control.mpvqcApplication.mpvqcSettings.windowTitleFormat = MpvqcSettings.WindowTitleFormat.DEFAULT;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.video_loaded = true;
        compare(control.text, "mpvQC");

        control.mpvqcApplication.mpvqcSettings.windowTitleFormat = MpvqcSettings.WindowTitleFormat.FILE_NAME;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.video_loaded = true;
        compare(control.text, "video-name");

        control.mpvqcApplication.mpvqcSettings.windowTitleFormat = MpvqcSettings.WindowTitleFormat.FILE_PATH;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.video_loaded = true;
        compare(control.text, "video-path");
    }

    function test_titleSuffix() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.mpvqcApplication.mpvqcManager.saved = true;
        verify(!control.text.endsWith("(unsaved)"));

        control.mpvqcApplication.mpvqcManager.saved = false;
        verify(control.text.endsWith("(unsaved)"));
    }
}
