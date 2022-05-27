/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick 2.0
import QtTest
import "MpvqcDocumentExporter.js" as TestObject


Item {

    TestCase {
        name: "MpvqcDocumentExporter::generateDocumentFrom"

        function test_documentStartsWithHeader() {
            const settings = provideTruthySettings()
            const data = provideData()
            const document = TestObject.generateDocumentFrom(data, settings)
            verify(document.startsWith('[FILE]'))
        }

        function test_headerSeperatedFromComments() {
            const settings = provideTruthySettings()
            const data = provideData()
            const document = TestObject.generateDocumentFrom(data, settings)
            verify(document.includes('\n\n[DATA]'))
        }

        function test_exportHeader() {
            const settings = provideTruthySettings()
            const data = provideData()
            const document = TestObject.generateDocumentFrom(data, settings)
            verify(document.includes(data.date))
            verify(document.includes(data.generator))
            verify(document.includes(data.nickname))
            verify(document.includes(data.videoPath))
        }

        function test_exportHeaderNot() {
            const settings = provideTruthySettings()
            settings.writeHeader = false
            const data = provideData()
            const document = TestObject.generateDocumentFrom(data, settings)
            verify(!document.includes(data.date))
            verify(!document.includes(data.generator))
            verify(!document.includes(data.nickname))
            verify(!document.includes(data.videoPath))

        }

        function test_exportDate() {
            const settings = provideTruthySettings()
            const data = provideData()
            const document = TestObject.generateDocumentFrom(data, settings)
            verify(document.includes(data.date))
        }

        function test_exportDateNot() {
            const settings = provideTruthySettings()
            settings.writeHeaderDate = false
            const data = provideData()
            const document = TestObject.generateDocumentFrom(data, settings)
            verify(!document.includes(data.date))
        }

        function test_exportGenerator() {
            const settings = provideTruthySettings()
            const data = provideData()
            const document = TestObject.generateDocumentFrom(data, settings)
            verify(document.includes(data.generator))
        }

        function test_exportGeneratorNot() {
            const settings = provideTruthySettings()
            settings.writeHeaderGenerator = false
            const data = provideData()
            const document = TestObject.generateDocumentFrom(data, settings)
            verify(!document.includes(data.generator))
        }

        function test_exportNickname() {
            const settings = provideTruthySettings()
            const data = provideData()
            const document = TestObject.generateDocumentFrom(data, settings)
            verify(document.includes(data.nickname))
        }

        function test_exportNicknameNot() {
            const settings = provideTruthySettings()
            settings.writeHeaderNickname = false
            const data = provideData()
            const document = TestObject.generateDocumentFrom(data, settings)
            verify(!document.includes(data.nickname))
        }

        function test_exportVideoPath() {
            const settings = provideTruthySettings()
            const data = provideData()
            const document = TestObject.generateDocumentFrom(data, settings)
            verify(document.includes(data.videoPath))
        }

        function test_exportVideoPathNot() {
            const settings = provideTruthySettings()
            settings.writeHeaderVideoPath = false
            const data = provideData()
            const document = TestObject.generateDocumentFrom(data, settings)
            verify(!document.includes(data.videoPath))
        }

        function test_exportContainsComments() {
            const settings = provideTruthySettings()
            const data = provideData()
            const document = TestObject.generateDocumentFrom(data, settings)
            for (const comment of data.comments) {
                verify(document.includes(comment.comment))
            }
        }

        function test_exportContainsCommentSummary() {
            const settings = provideTruthySettings()
            const data = provideData()
            const document = TestObject.generateDocumentFrom(data, settings)
            verify(document.includes('# total lines:'))
        }

        function test_exportEndsWithNewLine() {
            const settings = provideTruthySettings()
            const data = provideData()
            const document = TestObject.generateDocumentFrom(data, settings)
            verify(document.endsWith('\n'))
        }

        function provideData() {
            return {
                date: 'mpvqcDate',
                generator: 'mpvqcGenerator',
                nickname: 'mpvqcNickname',
                videoPath: 'mpvqcVideoPath',
                comments: [
                    { time: '68', commentType: 'CommentType', comment: 'Comment 1' },
                    { time: '69', commentType: 'CommentType', comment: 'Comment 2' },
                    { time: '70', commentType: 'CommentType', comment: 'Comment 3' },
                ],
            }
        }

        function provideTruthySettings() {
            return {
                writeHeader: true,
                writeHeaderDate: true,
                writeHeaderGenerator: true,
                writeHeaderNickname: true,
                writeHeaderVideoPath: true,
            }
        }
    }

    TestCase {
        name: "DocumentBuilder::build"

        function test_build_data() {
            return [
                {
                    expected: '',
                    actual: new TestObject.DocumentBuilder(),
                    tag: ' '
                },
                {
                    expected: '[FILE]',
                    actual: new TestObject.DocumentBuilder().addFileTag(),
                    tag: '[FILE]'
                },
                {
                    expected: 'date      : mpvqcDate',
                    actual: new TestObject.DocumentBuilder().addDate('mpvqcDate'),
                    tag: 'date'
                },
                {
                    expected: 'generator : mpvqcGenerator',
                    actual: new TestObject.DocumentBuilder().addGenerator('mpvqcGenerator'),
                    tag: 'generator'
                },
                {
                    expected: 'nick      : mpvqcNickname',
                    actual: new TestObject.DocumentBuilder().addNickname('mpvqcNickname'),
                    tag: 'nick'
                },
                {
                    expected: 'path      : mpvqcFilePath',
                    actual: new TestObject.DocumentBuilder().addFilePath('mpvqcFilePath'),
                    tag: 'path'
                },
                {
                    expected: '\n',
                    actual: new TestObject.DocumentBuilder().addBlankLine().addBlankLine(),
                    tag: '\\n'
                },
                {
                    expected: '[DATA]',
                    actual: new TestObject.DocumentBuilder().addDataTag(),
                    tag: '[DATA]'
                },
                {
                    expected: '[00:01:08] [CommentType] Comment 1\n[00:01:10] [CommentType] Comment 2',
                    actual: new TestObject.DocumentBuilder().addComments([
                            { time: '68', commentType: 'CommentType', comment: 'Comment 1' },
                            { time: 70, commentType: 'CommentType', comment: 'Comment 2' },
                        ]),
                    tag: 'comments'
                },
                {
                    expected: '# total lines: 0',
                    actual: new TestObject.DocumentBuilder().addCommentSummary(),
                    tag: '# total lines: 0'
                },
                {
                    expected: '[00:01:08] [CommentType] Comment 1\n# total lines: 1',
                    actual: new TestObject.DocumentBuilder().addComments([
                            { time: '68', commentType: 'CommentType', comment: 'Comment 1' }
                        ]).addCommentSummary(),
                    tag: '# total lines: 1'
                },
                {
                    expected: '[00:01:08] [CommentType] Comment 1\n[00:01:10] [CommentType] Comment 2\n# total lines: 2',
                    actual: new TestObject.DocumentBuilder().addComments([
                            { time: '68', commentType: 'CommentType', comment: 'Comment 1' },
                            { time: 70, commentType: 'CommentType', comment: 'Comment 2' },
                        ]).addCommentSummary(),
                    tag: '# total lines: 2'
                },
                {
                    expected: _complete(),
                    actual: new TestObject.DocumentBuilder()
                        .addFileTag()
                        .addDate('mpvqcDate')
                        .addGenerator('mpvqcGenerator')
                        .addNickname('mpvqcNickname')
                        .addFilePath('mpvqcFilePath')
                        .addBlankLine()
                        .addDataTag()
                        .addComments([
                            { time: '68', commentType: 'CommentType', comment: 'Comment 1' },
                            { time: 70, commentType: 'CommentType', comment: 'Comment 2' },
                        ])
                        .addCommentSummary()
                        .addBlankLine(),
                    tag: 'complete'
                },

            ]
        }

        function test_build(data) {
            compare(data.actual.build(), data.expected)
        }

        function _complete() {
         return '[FILE]
date      : mpvqcDate
generator : mpvqcGenerator
nick      : mpvqcNickname
path      : mpvqcFilePath

[DATA]
[00:01:08] [CommentType] Comment 1
[00:01:10] [CommentType] Comment 2
# total lines: 2
'
        }
    }

}
