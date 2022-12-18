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


Item {
    id: testHelper

    width: 400
    height: 400

    property string videoName: ''
    property string content: ''

    MpvqcBackupper {
        id: objectUnderTest

        video: ''

        mpvqcApplication: QtObject {
            property var mpvqcSettings: QtObject {
                property string nickname: 'nickname'
                property int backupInterval: 90
                property bool backupEnabled: true
            }
            property var mpvqcFileSystemHelperPyObject: QtObject {
                function url_to_absolute_path(url) { return url }
                function url_to_filename_without_suffix(url) { return url }
            }
            property var mpvqcTimeFormatUtils: QtObject {
                function formatTimeToString(seconds) { return 'formatted' }
            }
        }

        mpvqcBackupPyObject: QtObject {
            function write_backup(videoName, content) {
                testHelper.videoName= videoName
                testHelper.content = content
            }
        }

        generator: QtObject {
            function createBackupContent(video) { return 'content' }
        }

        property var test: TestCase {
            name: "MpvqcBackupper"
            when: windowShown

            function init() {
                testHelper.videoName= ''
                testHelper.content = ''
                objectUnderTest.video = ''
                objectUnderTest.timer.interval = 1
            }

            function test_backup_data() {
                return [
                    {
                        tag: 'enabled-no-video',
                        enabled: true,
                        video: '',
                        expectedVideoName: 'untitled',
                        expectedContent: 'content'
                    },
                    {
                        tag: 'enabled-with-video',
                        enabled: true,
                        video: 'video-name',
                        expectedVideoName: 'video-name',
                        expectedContent: 'content'
                    },
                    {
                        tag: 'disabled',
                        enabled: false,
                        video: '',
                        expectedVideoName: '',
                        expectedContent: ''
                    },
                ]
            }

            function test_backup(data) {
                objectUnderTest.mpvqcSettings.backupEnabled = data.enabled
                objectUnderTest.video = data.video
                wait(25)
                compare(testHelper.videoName, data.expectedVideoName)
                compare(testHelper.content, data.expectedContent)
            }

        }

    }

}
