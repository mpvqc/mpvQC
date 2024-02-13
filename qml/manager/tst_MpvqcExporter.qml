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

    property string filePath: ''
    property string content: ''

    MpvqcExporter {
        id: objectUnderTest

        video: ''
        document: ''

        mpvqcApplication: QtObject {
            property var mpvqcSettings: QtObject {
                property string nickname: 'nickname'
            }
            property var mpvqcCommentTable: QtObject {
                function getAllComments() { return [] }
            }
            property var mpvqcFileSystemHelperPyObject: QtObject {
                function url_to_absolute_path(url) { return 'absolute::' +url }
                function url_to_parent_file_url(url) { return 'parent::' + url }
                function url_to_filename_without_suffix(url) { return 'fileNameWithoutSuffix::' + url }
                function write(filePath, content) {
                    testHelper.filePath = filePath
                    testHelper.content = content
                }
            }
            property var mpvqcTimeFormatUtils: QtObject {
                function formatTimeToStringLong(seconds) { return 'formatted' }
            }
        }

        generator: QtObject {
            function createExportContent(video) { return 'content' }
        }

        property var test: TestCase {
            name: "MpvqcExporter"
            when: windowShown

            SignalSpy { id: savedSpy; target: objectUnderTest; signalName: 'saved' }

            function init() {
                testHelper.filePath= ''
                testHelper.content = ''

                objectUnderTest.video = ''
                objectUnderTest.document = ''
                objectUnderTest.exportDialog.selectedFile = ''

                savedSpy.clear()
            }

            function test_requestSave_data() {
                return [
                    { tag: 'document', document: 'something', expectedEmptyFilePathProposal: true },
                    { tag: 'no-document', document: '', expectedEmptyFilePathProposal: false },
                ]
            }

            function test_requestSave(data) {
                objectUnderTest.document = data.document
                objectUnderTest.requestSave()

                if (data.expectedEmptyFilePathProposal) {
                    verify(!objectUnderTest.exportDialog.selectedFile.toString().includes('file:///'))
                } else {
                    verify(objectUnderTest.exportDialog.selectedFile.toString().includes('file:///'))
                }
            }

            function test_requestSaveAs_data() {
                return [
                    { tag: 'saved', saved: true, acceptDialog: true, },
                    { tag: 'rejected', saved: false, acceptDialog: false, },
                ]
            }

            function test_requestSaveAs(data) {
                objectUnderTest.requestSaveAs()

                if (data.acceptDialog) {
                    objectUnderTest.exportDialog.accepted()
                }

                compare(savedSpy.count, data.saved ? 1 : 0)
            }

            function test_save() {
                const document = 'a-new-document.txt'

                objectUnderTest.save(document)

                compare(testHelper.filePath, document)
                compare(testHelper.content, 'content')
                compare(savedSpy.count, 1)
            }

            function test_getVideoDirectory_data() {
                return [
                    {
                        tag: 'video',
                        video: 'any-video.mkv',
                        verify: (actual) => compare(actual, 'parent::any-video.mkv')
                    },
                    {
                        tag: 'no-video',
                        video: '',
                        verify: (actual) => verify(actual.toString().includes('file:///'))
                    },
                ]
            }

            function test_getVideoDirectory(data) {
                objectUnderTest.video = data.video
                const actual = objectUnderTest.getVideoDirectory()
                data.verify(actual)
            }

            function test_getVideoName_data() {
                return [
                    {
                        tag: 'video',
                        video: 'any-video.mkv',
                        expected: 'fileNameWithoutSuffix::any-video.mkv'
                    },
                    { tag: 'no-video', video: '', expected: 'untitled' },
                ]
            }

            function test_getVideoName(data) {
                objectUnderTest.video = data.video
                compare(objectUnderTest.getVideoName(), data.expected)
            }

            function test_getFileNameWith_data() {
                return [
                    { tag: 'nickname', video: 'any-video', nickname: 'saitama', expected: '[QC]_any-video_saitama.txt' },
                    { tag: 'no-nickname', video: 'any-video', nickname: '', expected: '[QC]_any-video.txt' },
                    { tag: 'no-nickname-no-video', video: '', nickname: '', expected: '[QC]_.txt' },
                ]
            }

            function test_getFileNameWith(data) {
                objectUnderTest.mpvqcApplication.mpvqcSettings.nickname = data.nickname
                const proposal = objectUnderTest.getFileNameWith(data.video)
                compare(proposal, data.expected)
            }

        }

    }

}
