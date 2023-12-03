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


Item {

    MpvqcImporter {
        id: objectUnderTest

        mpvqcApplication: QtObject {
            property var mpvqcTimeFormatUtils: QtObject {
                function extractSecondsFrom(string) { return 42 }
            }
            property var mpvqcReverseTranslatorPyObject: QtObject {
                function lookup(somehing) { return something }
            }
            property var mpvqcSettings: QtObject {
                property var importWhenVideoLinkedInDocument: MpvqcSettings.ImportWhenVideoLinkedInDocument.ALWAYS
            }
        }

        property var test: TestCase {
            name: "MpvqcImporter"
            when: windowShown

            SignalSpy { id: commentsImportedSpy; target: objectUnderTest; signalName: 'commentsImported' }
            SignalSpy { id: videoImportedSpy; target: objectUnderTest; signalName: 'videoImported' }
            SignalSpy { id: subtitlesImportedSpy; target: objectUnderTest; signalName: 'subtitlesImported' }
            SignalSpy { id: stateChangedSpy; target: objectUnderTest; signalName: 'stateChanged' }
            SignalSpy { id: erroneousDocumentsImportedSpy; target: objectUnderTest; signalName: 'erroneousDocumentsImported' }

            function init() {
                commentsImportedSpy.clear()
                videoImportedSpy.clear()
                subtitlesImportedSpy.clear()
                stateChangedSpy.clear()
                erroneousDocumentsImportedSpy.clear()
            }

            function test_handleImport_data() {
                return [
                    {
                        tag: '1x-document',
                        stateChange: true,
                        video: 'standalone-video.mkv',
                        report: {
                            comments: [
                                { "time": 0, "commentType": "Translation", "comment": "abc" },
                                { "time": 12, "commentType": "Phrasing", "comment": "def" }
                            ],
                            successful: [
                                {
                                    url: "file:///existing.txt",
                                    video: "existing.mkv",
                                    comments: [
                                        { "time": 0, "commentType": "Translation", "comment": "abc" },
                                        { "time": 12, "commentType": "Phrasing", "comment": "def" }
                                    ]
                                }
                            ],
                            errors: []
                        },
                        subtitles: []
                    },
                    {
                        tag: '1x-document/error',
                        stateChange: true,
                        video: 'standalone-video.mkv',
                        report: {
                            comments: [
                                { "time": 0, "commentType": "Translation", "comment": "abc" },
                            ],
                            successful: [
                                {
                                    url: "file:///existing.txt",
                                    video: "existing.mkv",
                                    comments: [
                                        { "time": 0, "commentType": "Translation", "comment": "abc" },
                                    ]
                                }
                            ],
                            errors: ['error.txt']
                        },
                        subtitles: []
                    },
                    {
                        tag: '2x-document',
                        stateChange: true,
                        video: 'standalone-video.mkv',
                        report: {
                            comments: [
                                { "time": 0, "commentType": "Hint", "comment": "HINT" },
                                { "time": 338, "commentType": "Phrasing", "comment": "Hello!" },
                                { "time": 340, "commentType": "Phrasing", "comment": "Qes" },
                                { "time": 0, "commentType": "Translation", "comment": "Hallo du toller Blubber" },
                                { "time": 12, "commentType": "Phrasing", "comment": "Whabt" }
                            ],
                            successful: [
                                {
                                    url: "file:///existing-1.txt",
                                    video: "existing-1.mkv",
                                    comments: [
                                        {"time": 0, "commentType": "Hint", "comment": "HINT"},
                                        {"time": 338, "commentType": "Phrasing", "comment": "Hello!"},
                                        {"time": 340, "commentType": "Phrasing", "comment": "Qes"}
                                    ]
                                },
                                {
                                    url: "file:///existing-2.txt",
                                    video: "existing-2.mkv",
                                    comments: [
                                        { "time": 0, "commentType": "Translation", "comment": "Hallo du toller Blubber" },
                                        { "time": 12, "commentType": "Phrasing", "comment": "Whabt" }
                                    ]
                                }
                            ],
                            errors: []
                        },
                        subtitles: []
                    },
                    {
                        tag: '1x-video',
                        stateChange: true,
                        video: 'standalone-video.mkv',
                        report: {
                            comments: [],
                            successful: [],
                            errors: []
                        },
                        subtitles: []
                    },
                    {
                        tag: '2x-subtitles',
                        stateChange: false,
                        video: '',
                        report: {
                            comments: [],
                            successful: [],
                            errors: []
                        },
                        subtitles: [ "file:///existing-1.txt", "file:///existing-2.txt"]
                    },
                ]
            }

            function test_handleImport(data) {
                objectUnderTest.handleImport(data.report, data.video, data.subtitles)
                verifyComments(data.report.comments)
                verifyVideo(data.video)
                verifySubtitles(data.subtitles)
                verifyStateChange(data.stateChange)
                verifyErrors(data.report.errors)
            }

            function verifyComments(comments) {
                const commentsLength = comments.length
                if (commentsLength === 0) {
                    compare(commentsImportedSpy.count, 0)
                } else {
                    compare(commentsImportedSpy.count, 1)
                    const signaled = commentsImportedSpy.signalArguments[0][0]
                    compare(signaled.length, commentsLength)
                }
            }

            function verifyVideo(video) {
                const count = video ? 1 : 0
                compare(videoImportedSpy.count, count)
            }

            function verifySubtitles(subtitles) {
                const subtitlesLength = subtitles.length
                if (subtitlesLength === 0) {
                    compare(subtitlesImportedSpy.count, 0)
                } else {
                    compare(subtitlesImportedSpy.count, 1)
                    const signaled = subtitlesImportedSpy.signalArguments[0][0]
                    compare(signaled.length, subtitlesLength)
                }
            }

            function verifyStateChange(expected) {
                const count = expected ? 1 : 0
                compare(stateChangedSpy.count, count)
            }

            function verifyErrors(errors) {
                const count = errors.length > 0 ? 1 : 0
                compare(erroneousDocumentsImportedSpy.count, count)
            }

        }
    }

}
