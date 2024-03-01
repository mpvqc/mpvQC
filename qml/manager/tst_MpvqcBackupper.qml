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

    width: 400
    height: 400
    visible: true
    name: 'MpvqcBackupper'

    Component {
        id: objectUnderTest

        MpvqcBackupper {
            property bool backupCalled: false

            mpvqcApplication: QtObject {
                property var mpvqcSettings: QtObject
                {
                    property int backupInterval: 1
                    property bool backupEnabled: false
                }
                property var mpvqcCommentTable: QtObject
                {
                    property int count: -1
                }
                property var mpvqcDocumentExporterPyObject: QtObject
                {
                    function backup() {
                        backupCalled = true
                    }
                }
                property var mpvqcMpvPlayerPropertiesPyObject: QtObject
                {
                    property bool video_loaded: false
                }
            }

        }
    }

    function test_backup_data() {
        return [
            {tag: 'enabled-❌️-comments-❌', enabled: false, haveComments: false, backup: false},
            {tag: 'enabled-❌️-comments-✔️', enabled: false, haveComments: true, backup: false},
            {tag: 'enabled-✔️-comments-❌', enabled: true, haveComments: false, backup: false},
            {tag: 'enabled-✔️-comments-✔️', enabled: true, haveComments: true, backup: true},
        ]
    }

    function test_backup(data) {
        let control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)
        verify(!control.backupCalled)

        control.mpvqcApplication.mpvqcSettings.backupEnabled = data.enabled
        control.mpvqcApplication.mpvqcCommentTable.count = data.haveComments ? 100 : 0

        control.interval = 1
        wait(25)

        compare(control.backupCalled, data.backup)
    }

}
