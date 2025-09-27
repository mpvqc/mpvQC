// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtTest

TestCase {
    id: testCase

    visible: false
    name: "MpvqcAppHeaderViewController"

    Component {
        id: signalSpy

        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcAppHeaderViewController {
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
