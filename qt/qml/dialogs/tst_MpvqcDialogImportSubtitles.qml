// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtTest

TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcDialogImportSubtitles"

    Component {
        id: objectUnderTest

        MpvqcDialogImportSubtitles {
            id: __objectUnderTest

            property bool openSubtitlesCalled: false

            mpvqcApplication: QtObject {
                property var mpvqcManager: QtObject {
                    function openSubtitles(files) {
                        __objectUnderTest.openSubtitlesCalled = true;
                    }
                }
                property var mpvqcSettings: QtObject {
                    property string lastDirectorySubtitles: "initial directory"
                }
                property var mpvqcUtilityPyObject: QtObject {
                    property list<string> subtitleFileGlobPattern: []
                }
            }
        }
    }

    function test_import() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.currentFolder = "some directory";
        control.accepted();

        verify(control.openSubtitlesCalled);
        verify(!control.mpvqcSettings.lastDirectorySubtitles.toString().includes("initial directory"));
    }
}
