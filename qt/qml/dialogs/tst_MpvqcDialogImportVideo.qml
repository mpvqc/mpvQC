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
    name: "MpvqcDialogImportVideo"

    Component {
        id: objectUnderTest

        MpvqcDialogImportVideo {
            id: __objectUnderTest

            property bool openVideoCalled: false

            mpvqcApplication: QtObject {
                property var mpvqcManager: QtObject {
                    function openVideo(video) {
                        __objectUnderTest.openVideoCalled = true;
                    }
                }
                property var mpvqcSettings: QtObject {
                    property string lastDirectoryVideo: "initial directory"
                }
                property var mpvqcUtilityPyObject: QtObject {
                    property list<string> videoFileGlobPattern: []
                }
            }
        }
    }

    function test_import() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.currentFolder = "some directory";
        control.accepted();

        verify(control.openVideoCalled);
        verify(!control.mpvqcSettings.lastDirectoryVideo.toString().includes("initial directory"));
    }
}
