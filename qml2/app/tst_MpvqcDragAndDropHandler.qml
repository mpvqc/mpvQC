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


import QtTest


MpvqcDragAndDropHandler {
    id: objectUnderTest
    width: 400
    height: 400

    supportedSubtitleFileExtensions: [ 'ass' ]

    TestCase {
        id: testCase
        name: "MpvqcDragAndDropHandler"
        when: windowShown

        property bool accepted: false

        SignalSpy { id: filesDroppedSpy; target: objectUnderTest; signalName: 'filesDropped' }

        function cleanup() {
            filesDroppedSpy.clear()
            testCase.accepted = false
        }

        function test_enter_data() {
            return [
                {
                    tag: 'accept', accepted: true,
                    event: {
                        formats: ['text/uri-list'],
                        hasUrls: true,
                        accept: (action) => { accepted = true }
                    }
                },
                { tag: 'ignore', accepted: false, event: { formats: [], hasUrls: true } },
            ]
        }

        function test_enter(data) {
            objectUnderTest.handleEnter(data.event)
            compare(testCase.accepted, data.accepted)
        }

        function test_drop_data() {
            return [
                {
                    tag: 'all', documents: ['document.txt'], video: 'video.mp4', subtitles: ['subtitle.ass'],
                    event: {
                        formats: ['text/uri-list'],
                        hasUrls: true,
                        urls: [ 'document.txt', 'video.mp4', 'subtitle.ass']
                    }
                },
                {
                    tag: 'partial', documents: ['document.txt'], video: 'video.mp4', subtitles: [],
                    event: {
                        formats: ['text/uri-list'],
                        hasUrls: true,
                        urls: [ 'document.txt', 'video.mp4', 'subtitle']
                    }
                },
                { tag: 'ignore', event: { formats: [], hasUrls: true } },
            ]
        }

        function test_drop(data) {
            objectUnderTest.handleDrop(data.event)
            if (data.event.urls) {
                const [documents, video, subtitles] = filesDroppedSpy.signalArguments[0]
                compare(data.documents, documents)
                compare(data.video, video)
                compare(data.subtitles, subtitles)
            }
        }

    }

 }
