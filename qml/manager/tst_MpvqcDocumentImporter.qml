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


import QtQuick 2.0
import QtTest
import "MpvqcDocumentImporter.js" as TestObject


Item {

    TestCase {
        name: "MpvqcDocumentImporter::Extractor"

        function test_extractVideo_data() {
            const content = ['[FILE]', 'path      : myExampleVideo.mkv', 'nick      : mpvqcNickname']
            return [
                {
                    expected: '',
                    content: [
                        '[FILE]',
                        'path      : ',
                        'nick      : mpvqcNickname'
                    ].join('\n'),
                    tag: ' '
                },
                { expected: 'myExampleVideo.mkv', content: content.join('\n'), tag: '\\n' },
                { expected: 'myExampleVideo.mkv', content: content.join('\r\n'), tag: '\\r\\n' },

            ]
        }

        function test_extractVideo(data) {
            const extractor = new TestObject.Extractor(data.content)
            extractor.extract()
            compare(extractor.video, data.expected)
        }

        function test_extractComments_data() {
            const content1 = [
                '[DATA]',
                '[00:00:00] [Translation] remark',
                '# total lines: 1'
            ]
            const expected1 = [
                {"time":0,"commentType":"Translation","comment":"remark"},
            ]
            const content2 = [
                '[DATA]',
                '[00:00:00] [Translation] remark',
                '[00:00:01] [Punctuation] remark 2',
                '# total lines: 2'
            ]
            const expected2 = [
                {"time":0,"commentType":"Translation","comment":"remark"},
                {"time":1,"commentType":"Punctuation","comment":"remark 2"},
            ]
            return [
                {
                    expected: [],
                    content: [
                        '[FILE]',
                        'path      : ',
                        'nick      : mpvqcNickname'
                    ].join('\n'),
                    tag: ' '
                },
                { expected: expected1, content: content1.join('\n'), tag: '1 comment \\n' },
                { expected: expected1, content: content1.join('\r\n'), tag: '1 comment \\r\\n' },
                { expected: expected2, content: content2.join('\n'), tag: '2 comments \\n' },
                { expected: expected2, content: content2.join('\r\n'), tag: '2 comments \\r\\n' },
            ]
        }

        function test_extractComments(data) {
            const extractor = new TestObject.Extractor(data.content)
            extractor.extract()
            compare(JSON.stringify(extractor.comments), JSON.stringify(data.expected))
        }

    }

    TestCase {
        name: "MpvqcDocumentImporter::Document"

        function test_isTextFile_data() {
            return [
                { expected: true, url: "file.txt", tag: 'true' },
                { expected: false, url: "file.yml", tag: 'false' },
            ]
        }

        function test_isTextFile(data) {
            const document = new TestObject.Document(data.url)
            compare(document.isTextFile(), data.expected)
            compare(document.isNotTextFile(), !data.expected)
        }

        function test_startsWithFileTag_data() {
            return [
                { expected: true, tag: '[FILE]' },
                { expected: true, tag: ' [FILE]' },
                { expected: false, tag: 'other' },
            ]
        }

        function test_startsWithFileTag(data) {
            const document = new TestObject.Document(undefined, data.tag)
            compare(document.startsWithFileTag(), data.expected)
            compare(document.startsNotWithFileTag(), !data.expected)
        }

    }

}
