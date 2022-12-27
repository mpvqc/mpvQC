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
import QtQuick.Controls
import QtTest

import settings


Item {

    MpvqcVideoSelector {
        id: objectUnderTest

        mpvqcApplication: ApplicationWindow {
            property real windowRadius: 12
            property var mpvqcSettings: QtObject {
                property var importWhenVideoLinkedInDocument: MpvqcSettings.ImportWhenVideoLinkedInDocument.NEVER
            }
            property var mpvqcFileSystemHelperPyObject: QtObject {
                function absolute_path_to_url(path) { return path }
                function url_is_file(url) { return url === 'existing.mkv' }
            }
        }

        property var test: TestCase {
            name: "MpvqcVideoSelector"
            when: windowShown

            SignalSpy { id: videoSelectedSpy; target: objectUnderTest; signalName: 'videoSelected' }

            function init() {
                videoSelectedSpy.clear()
                objectUnderTest.dialog = null
            }

            function test_chooseBetween_data() {
                return [
                    {
                        tag: 'standalone',
                        setting: MpvqcSettings.ImportWhenVideoLinkedInDocument.NEVER,
                        videoStandalone: 'standalone-exists.mkv',
                        possiblyLinkedDocuments: [ { 'video': 'existing.mkv' } ],
                        handleDialog: (dialog) => {},
                        expected: 'standalone-exists.mkv'
                    },
                    {
                        tag: 'linked-never',
                        setting: MpvqcSettings.ImportWhenVideoLinkedInDocument.NEVER,
                        videoStandalone: '',
                        possiblyLinkedDocuments: [ { 'video': 'existing.mkv' } ],
                        handleDialog: (dialog) => {},
                        expected: ''
                    },
                    {
                        tag: 'linked-empty',
                        setting: MpvqcSettings.ImportWhenVideoLinkedInDocument.ALWAYS,
                        videoStandalone: '',
                        possiblyLinkedDocuments: [ { 'video': '' } ],
                        handleDialog: (dialog) => {},
                        expected: ''
                    },
                    {
                        tag: 'linked-not-existing',
                        setting: MpvqcSettings.ImportWhenVideoLinkedInDocument.ALWAYS,
                        videoStandalone: '',
                        possiblyLinkedDocuments: [ { 'video': 'not-existing.mkv' } ],
                        handleDialog: (dialog) => {},
                        expected: ''
                    },
                    {
                        tag: 'linked-existing',
                        setting: MpvqcSettings.ImportWhenVideoLinkedInDocument.ALWAYS,
                        videoStandalone: '',
                        possiblyLinkedDocuments: [ { 'video': 'existing.mkv' } ],
                        handleDialog: (dialog) => {},
                        expected: 'existing.mkv'
                    },
                    {
                        tag: 'linked-existing-yes',
                        setting: MpvqcSettings.ImportWhenVideoLinkedInDocument.ASK_EVERY_TIME,
                        videoStandalone: '',
                        possiblyLinkedDocuments: [ { 'video': 'existing.mkv' } ],
                        handleDialog: (dialog) => { dialog.positive() },
                        expected: 'existing.mkv'
                    },
                    {
                        tag: 'linked-existing-no',
                        setting: MpvqcSettings.ImportWhenVideoLinkedInDocument.ASK_EVERY_TIME,
                        videoStandalone: '',
                        possiblyLinkedDocuments: [ { 'video': 'existing.mkv' } ],
                        handleDialog: (dialog) => { dialog.negative() },
                        expected: ''
                    },
                ]
            }

            function test_chooseBetween(data) {
                objectUnderTest.mpvqcApplication.mpvqcSettings.importWhenVideoLinkedInDocument = data.setting
                objectUnderTest.chooseBetween(data.videoStandalone, data.possiblyLinkedDocuments)
                data.handleDialog(objectUnderTest.dialog)

                compare(videoSelectedSpy.count, 1)
                const actual = videoSelectedSpy.signalArguments[0][0]
                compare(actual, data.expected)
            }
        }

    }

}
