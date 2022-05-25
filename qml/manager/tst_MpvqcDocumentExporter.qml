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
        name: "generateDocumentFrom"

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
        name: "DocumentBuilder"

        function test_buildEmptyDocument(data) {
            const builder = new TestObject.DocumentBuilder()
            compare(builder.build(), '')
        }

        function test_buildAddFileTag() {
            const builder = new TestObject.DocumentBuilder().addFileTag()
            compare(builder.build(), '[FILE]')
        }

        function test_buildAddDate() {
            const builder = new TestObject.DocumentBuilder().addDate('mpvqcDate')
            compare(builder.build(), 'date      : mpvqcDate')
        }

        function test_buildAddGenerator() {
            const builder = new TestObject.DocumentBuilder().addGenerator('mpvqcGenerator')
            compare(builder.build(), 'generator : mpvqcGenerator')
        }


        function test_buildAddNickname() {
            const builder = new TestObject.DocumentBuilder().addNickname('mpvqcNickname')
            compare(builder.build(), 'nick      : mpvqcNickname')
        }


        function test_buildAddFilePath() {
            const builder = new TestObject.DocumentBuilder().addFilePath('mpvqcFilePath')
            compare(builder.build(), 'path      : mpvqcFilePath')
        }


        function test_buildAddBlankLines() {
            const builder = new TestObject.DocumentBuilder().addBlankLine().addBlankLine()
            compare(builder.build(), '\n')
        }

        function test_buildAddDataTag() {
            const builder = new TestObject.DocumentBuilder().addDataTag()
            compare(builder.build(), '[DATA]')
        }


        function test_buildAddComments() {
            const builder = new TestObject.DocumentBuilder()
                .addComments([
                    { time: '68', commentType: 'CommentType', comment: 'Comment 1' },
                    { time: 70, commentType: 'CommentType', comment: 'Comment 2' },
                ])
            compare(builder.build(), '[00:01:08] [CommentType] Comment 1\n[00:01:10] [CommentType] Comment 2')
        }


        function test_buildAddCommentSummary0() {
            const builder = new TestObject.DocumentBuilder().addCommentSummary()
            compare(builder.build(), '# total lines: 0')
        }

        function test_buildAddCommentSummary1() {
            const builder = new TestObject.DocumentBuilder()
                .addComments([{ time: '68', commentType: 'CommentType', comment: 'Comment 1' }])
                .addCommentSummary()
            compare(builder.build(), '[00:01:08] [CommentType] Comment 1\n# total lines: 1')
        }

        function test_buildAddCommentSummary2() {
            const builder = new TestObject.DocumentBuilder()
                .addComments([
                    { time: '68', commentType: 'CommentType', comment: 'Comment 1' },
                    { time: 70, commentType: 'CommentType', comment: 'Comment 2' },
                ])
                .addCommentSummary()

            compare(
                builder.build(),
                '[00:01:08] [CommentType] Comment 1\n[00:01:10] [CommentType] Comment 2\n# total lines: 2'
            )
        }

        function test_buildCompleteDocument() {
            const builder = new TestObject.DocumentBuilder()
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
                .addBlankLine()

        compare(
            builder.build(),
'[FILE]
date      : mpvqcDate
generator : mpvqcGenerator
nick      : mpvqcNickname
path      : mpvqcFilePath

[DATA]
[00:01:08] [CommentType] Comment 1
[00:01:10] [CommentType] Comment 2
# total lines: 2
')
        }
    }

}
