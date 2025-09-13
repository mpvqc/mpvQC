/*
 * Copyright (C) 2025 mpvQC developers
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

import QtQuick
import QtTest

TestCase {
    id: testCase

    visible: false
    name: "MpvqcAppHeaderController"

    Component {
        id: signalSpy

        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcAppHeaderController {
            mpvqcTheme: QtObject {}
            mpvqcSettings: QtObject {
                property int layoutOrientation: Qt.Vertical
                property int windowTitleFormat: 0
                property string language: "en"
            }
            isVisible: true
            isMaximized: true
            isStateSaved: true
            isVideoLoaded: true
            isDebugEnabled: false

            applicationLayout: 0
            windowTitleFormat: 0
            playerVideoName: "playerVideoName"
            playerVideoPath: "playerVideoPath"

            extendedExportTemplatesModel: []
        }
    }

    function test_configureWindowTitleFormat() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        compare(control.mpvqcSettings.windowTitleFormat, 0);
        const updated = 1;
        control.configureWindowTitleFormat(updated);
        compare(control.mpvqcSettings.windowTitleFormat, 1);
    }

    function test_configureApplicationLayout() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        compare(control.mpvqcSettings.layoutOrientation, Qt.Vertical);
        control.configureApplicationLayout(Qt.Horizontal);
        compare(control.mpvqcSettings.layoutOrientation, Qt.Horizontal);
    }

    function test_configureLanguage() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        compare(control.mpvqcSettings.language, "en");
        control.configureLanguage("de");
        compare(control.mpvqcSettings.language, "de");
    }
}
