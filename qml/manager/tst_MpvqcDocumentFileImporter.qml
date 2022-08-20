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
import "MpvqcDocumentFileImporter.js" as TestObject


Item {

    TestCase {
        name: "MpvqcDocumentFileImporter::Importer"

        property var timeExtractorFunc: function(timeString) { return 1 }
        property var reverseTranslatorFunc: function(translation) { return translation }
        property var urlTransformerFunc: function(path) { return 'url::' + path }

        property var classUnderTest: function(fileReaderFunc) {
            return new TestObject.Importer(timeExtractorFunc, reverseTranslatorFunc, fileReaderFunc, urlTransformerFunc)
        }

        function test_importFrom_data() {
            return [
                {
                    tag: 'report',
                    input: [
                        { url: 'file1.txt', fileContent: '' },
                        { url: 'file2.txt', fileContent: '[FILE]\npath      : myExampleVideo2.mkv' },
                        {
                            url: 'file3.txt',
                            fileContent: '[FILE]\n[00:00:01] [Translation] remark\n[00:00:01] [Punctuation] remark 2',
                        },
                        { url: 'file4.txt', fileContent: _fullReport() },
                        { url: 'file5.yml', fileContent: '' },
                    ],
                    expected: {
                        comments: [
                            { time: 1, commentType: "Translation", comment: "remark" },
                            { time: 1, commentType: "Punctuation", comment: "remark 2" },
                            { time: 1, commentType: "CommentType", comment: "Comment 1" },
                            { time: 1, commentType: "CommentType", comment: "Comment 2" }
                        ],
                        videos: [ "url::myExampleVideo2.mkv","url::mpvqcFilePath42" ],
                        errors: [
                            { url: "file1.txt", message: "Document is not a valid quality check report" },
                            { url: "file5.yml", message: "Document is not a valid quality check report" },
                        ],
                    }
                }
            ]
        }

        function test_importFrom(data) {
            let input = 0, fileReaderFunc = function(url) { return data.input[input++].fileContent }
            const urls = data.input.map(v => v.url)

            const importer = classUnderTest(fileReaderFunc)
            const actual = JSON.stringify(importer.importFrom(urls))
            const expected = JSON.stringify(data.expected)
            compare(actual, expected)
        }

    }


    TestCase {
        name: "MpvqcDocumentFileImporter::DocumentFileImporter"

        property var timeExtractorFunc: function(timeString) { return 1 }
        property var reverseTranslatorLookupFunc: function(translation) { return translation }

        property var classUnderTest: function(fileReaderFunc) {
            return new TestObject.DocumentFileImporter(timeExtractorFunc, reverseTranslatorLookupFunc, fileReaderFunc)
        }

        function test_importFrom_data() {
            return [
                {
                    input: [
                        { url: 'file.txt', fileContent: '' },
                        { url: 'file.yml', fileContent: '' },
                    ],
                    expected: {
                        errors: [
                            { url: "file.txt", message: "Document is not a valid quality check report" },
                            { url: "file.yml", message: "Document is not a valid quality check report" },
                         ],
                        imports: []
                    },
                    tag: 'invalid docs'
                },
                {
                    input: [ { url: 'file.txt', fileContent: '[FILE]' } ],
                    expected: { errors: [], imports: [ { url: "file.txt", video:"", comments: [] } ] },
                    tag: 'valid - empty'
                },
                {
                    input: [ { url: 'file.txt', fileContent: '[FILE]\nnick : mpvqcNickname\npath : myExampleVideo.mkv\n\n', } ],
                    expected: { errors: [], imports: [ { url: "file.txt", video: "myExampleVideo.mkv", comments: [] } ] },
                    tag: 'valid - video'
                },
                {
                    input: [
                        {
                            url: 'file.txt',
                            fileContent: '[FILE]\n[00:00:01] [Translation] remark\n[00:00:01] [Punctuation] remark 2',
                        }
                    ],
                    expected: {
                        errors: [],
                        imports: [
                            {
                                url: "file.txt",
                                video:"", comments: [
                                    { time: 1, commentType: 'Translation', comment: 'remark' },
                                    { time: 1, commentType: 'Punctuation', comment: 'remark 2' },
                                ]
                            }
                        ]
                    },
                    tag: 'valid - comments'
                },
                {
                    input: [
                        { url: 'file1.txt', fileContent: '', },
                        { url: 'file2.txt', fileContent: '[FILE]\npath      : myExampleVideo2.mkv', },
                        {
                            url: 'file3.txt',
                            fileContent: '[FILE]\n[00:00:01] [Translation] remark\n[00:00:01] [Punctuation] remark 2',
                        },
                        { url: 'file4.txt', fileContent: _fullReport(), },
                        { url: 'file5.yml', fileContent: '', },
                    ],
                    expected: {
                        errors: [
                            { url: "file1.txt", message: "Document is not a valid quality check report" },
                            { url: "file5.yml", message: "Document is not a valid quality check report" },
                        ],
                        imports: [
                            { url: "file2.txt", video: "myExampleVideo2.mkv", comments: [] },
                            {
                                url: "file3.txt",
                                video: "",
                                comments: [
                                    { time: 1, commentType: "Translation", comment: "remark" },
                                    { time: 1, commentType: "Punctuation", comment: "remark 2" },
                                ]
                            },
                            {
                                url: "file4.txt",
                                video: "mpvqcFilePath42",
                                comments: [
                                    { time: 1, commentType: "CommentType", comment: "Comment 1" },
                                    { time: 1, commentType: "CommentType", comment: "Comment 2" }
                                ]
                            }
                        ]
                    },
                    tag: 'full mix'
                }
            ]
        }

        function test_importFrom(data) {
            let input = 0, fileReaderFunc = function(url) { return data.input[input++].fileContent }
            const urls = data.input.map(v => v.url)

            const importer = classUnderTest(fileReaderFunc)
            const actual = JSON.stringify(importer.importFrom(urls))
            const expected = JSON.stringify(data.expected)
            compare(actual, expected)
        }

    }

    TestCase {
        name: "MpvqcDocumentFileImporter::DocumentReader"

        property var classUnderTest: function(fileReaderFunc) {
            return new TestObject.DocumentReader(fileReaderFunc)
        }

        function test_read_data() {
            return [
                {
                    url: 'file.yml', fileContent: '', tag: 'invalid type',
                    expected: { error: 'Document is not a valid quality check report' },
                },
                {
                    url: 'file.txt', fileContent: '', tag: 'invalid header',
                    expected: { error: 'Document is not a valid quality check report' },
                },
                {
                    url: 'file.txt', fileContent: '[FILE]', tag: 'valid',
                    expected: { textContent: '[FILE]' },
                },
            ]
        }

        function test_read(data) {
            const fileReaderFunc = function(url) { return data.fileContent }
            const reader = classUnderTest(fileReaderFunc)
            compare(JSON.stringify(reader.read(data.url)), JSON.stringify(data.expected))
        }
    }

    TestCase {
        name: "MpvqcDocumentFileImporter::QcContentExtractor"

        property var timeExtractorFunc: function(timeString) { return 1 }
        property var reverseTranslatorLookupFunc: function(translation) { return translation }

        property var classUnderTest: function() {
            return new TestObject.QcContentExtractor(timeExtractorFunc, reverseTranslatorLookupFunc)
        }

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
            const extractor = classUnderTest()
            extractor.extract(data.content)
            compare(extractor.video, data.expected)
        }

        function test_extractComments_data() {
            const content1 = [
                '[DATA]',
                '[00:00:01] [Translation] remark',
                '# total lines: 1'
            ]
            const expected1 = [
                { time: 1, commentType: "Translation", comment: "remark" },
            ]
            const content2 = [
                '[DATA]',
                '[00:00:01] [Translation] remark',
                '[00:00:01] [Punctuation] remark 2',
                '# total lines: 2'
            ]
            const expected2 = [
                { time: 1, commentType: "Translation", comment: "remark" },
                { time: 1, commentType: "Punctuation", comment: "remark 2" },
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
            const extractor = classUnderTest()
            extractor.extract(data.content)
            compare(JSON.stringify(extractor.comments), JSON.stringify(data.expected))
        }

    }

    function _fullReport() {
        const lines = [
            '[FILE]',
            'date      : mpvqcDate',
            'generator : mpvqcGenerator',
            'nick      : mpvqcNickname',
            'path      : mpvqcFilePath42',
            '',
            '[DATA]',
            '[00:00:01] [CommentType] Comment 1',
            '[00:00:01] [CommentType] Comment 2',
            '# total lines: 2',
            '',
            '',
            '',
        ]
        return lines.join('\n')
    }

}
