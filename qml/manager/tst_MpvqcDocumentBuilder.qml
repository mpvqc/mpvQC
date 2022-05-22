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
import "MpvqcDocumentBuilder.mjs" as MpvqcDocumentBuilder


TestCase {
    name: "MpvqcDocumentBuilder"

    function test_buildEmptyDocument(data) {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder()
        compare(builder.build(), '')
    }

    function test_buildAddFileTag() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder().addFileTag()
        compare(builder.build(), '[FILE]')
    }

    function test_buildAddDate() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder().addDate('mpvqcDate')
        compare(builder.build(), 'date      : mpvqcDate')
    }

    function test_buildAddGenerator() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder().addGenerator('mpvqcGenerator')
        compare(builder.build(), 'generator : mpvqcGenerator')
    }


    function test_buildAddNickname() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder().addNickname('mpvqcNickname')
        compare(builder.build(), 'nick      : mpvqcNickname')
    }


    function test_buildAddFilePath() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder().addFilePath('mpvqcFilePath')
        compare(builder.build(), 'path      : mpvqcFilePath')
    }


    function test_buildAddBlankLines() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder().addBlankLine().addBlankLine()
        compare(builder.build(), '\n')
    }

    function test_buildAddDataTag() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder().addDataTag()
        compare(builder.build(), '[DATA]')
    }


    function test_buildAddComments() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder()
            .addComments([
                { time: '68', commentType: 'CommentType', comment: 'Comment 1' },
                { time: 70, commentType: 'CommentType', comment: 'Comment 2' },
            ])
        compare(builder.build(), '[00:01:08] [CommentType] Comment 1\n[00:01:10] [CommentType] Comment 2')
    }


    function test_buildAddCommentSummary0() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder().addCommentSummary()
        compare(builder.build(), '# total lines: 0')
    }

    function test_buildAddCommentSummary1() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder()
            .addComments([{ time: '68', commentType: 'CommentType', comment: 'Comment 1' }])
            .addCommentSummary()
        compare(builder.build(), '[00:01:08] [CommentType] Comment 1\n# total lines: 1')
    }

    function test_buildAddCommentSummary2() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder()
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
        const builder = new MpvqcDocumentBuilder.DocumentBuilder()
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
'
        )
    }

}
