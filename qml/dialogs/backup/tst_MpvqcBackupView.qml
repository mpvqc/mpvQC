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
import QtQuick.Controls.Material
import QtTest


MpvqcBackupView {
    id: objectUnderTest

    mpvqcApplication: QtObject {
        property var mpvqcSettings: QtObject {
            property bool backupEnabled: true
            property int backupInterval: 90
        }
        property var mpvqcFilePathsPyObject: QtObject {
            property url dir_backup: 'file:///hello.txt'
        }
        property var mpvqcFileSystemHelperPyObject: QtObject {
            function url_to_absolute_path(url) { return `${url}-as-abs-path` }
        }
    }

    // Mock Qt.openUrlExternally
    property url calledUrl: ''
    openBackupLocationFunc: openUrlExternallyMock
    function openUrlExternallyMock(url) { calledUrl = url }
    // end

    width: 400
    height: 400

    TestCase {
        name: "MpvqcBackupView"
        when: windowShown

        function init() {
            const settings = objectUnderTest.mpvqcApplication.mpvqcSettings
            settings.backupEnabled = true
            settings.backupInterval = 90
            objectUnderTest.calledUrl = ''
        }

        function test_backup_data() {
            return [
                {
                     tag: 'toggle',
                     exec: () => { objectUnderTest.backupEnabledSwitch.checked = false },
                     verify: () => { compare(objectUnderTest.mpvqcApplication.mpvqcSettings.backupEnabled, false) },
                },
                {
                     tag: 'interval',
                     exec: () => { objectUnderTest.backupIntervalSpinBox.increase() },
                     verify: () => { compare(objectUnderTest.mpvqcApplication.mpvqcSettings.backupInterval, 91) },
                },
                {
                     tag: 'open-directory',
                     exec: () => { mouseClick(objectUnderTest.backupLocationOpenButton) },
                     verify: () => { compare(objectUnderTest.calledUrl, 'file:///hello.txt') },
                },
            ]
        }

        function test_backup(data) {
            data.exec()
            data.verify()
        }
    }

}
