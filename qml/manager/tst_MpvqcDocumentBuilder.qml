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

    function test_buildWithFileTag() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder().withFileTag()
        compare(builder.build(), '[FILE]')
    }

    function test_buildWithDate() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder().withDate('mpvqcDate')
        compare(builder.build(), 'date      : mpvqcDate')
    }

    function test_buildWithGenerator() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder().withGenerator('mpvqcGenerator')
        compare(builder.build(), 'generator : mpvqcGenerator')
    }


    function test_buildWithNickname() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder().withNickname('mpvqcNickname')
        compare(builder.build(), 'nick      : mpvqcNickname')
    }


    function test_buildWithFilePath() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder().withFilePath('mpvqcFilePath')
        compare(builder.build(), 'path      : mpvqcFilePath')
    }


    function test_buildWithBlankLines() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder().withBlankLine().withBlankLine()
        compare(builder.build(), '\n')
    }

    function test_buildWithDataTag() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder().withDataTag()
        compare(builder.build(), '[DATA]')
    }


    function test_buildWithComments() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder()
            .withComments([
                { time: '68', commentType: 'CommentType', comment: 'Comment 1' },
                { time: 70, commentType: 'CommentType', comment: 'Comment 2' },
            ])
        compare(builder.build(), '[00:01:08] [CommentType] Comment 1\n[00:01:10] [CommentType] Comment 2')
    }


    function test_buildWithCommentSummary0() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder().withCommentSummary()
        compare(builder.build(), '# total lines: 0')
    }

    function test_buildWithCommentSummary1() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder()
            .withComments([{ time: '68', commentType: 'CommentType', comment: 'Comment 1' }])
            .withCommentSummary()
        compare(builder.build(), '[00:01:08] [CommentType] Comment 1\n# total lines: 1')
    }

    function test_buildWithCommentSummary2() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder()
            .withComments([
                { time: '68', commentType: 'CommentType', comment: 'Comment 1' },
                { time: 70, commentType: 'CommentType', comment: 'Comment 2' },
            ])
            .withCommentSummary()

        compare(
            builder.build(),
            '[00:01:08] [CommentType] Comment 1\n[00:01:10] [CommentType] Comment 2\n# total lines: 2'
        )
    }

    function test_completeDocument() {
        const builder = new MpvqcDocumentBuilder.DocumentBuilder()
            .withFileTag()
            .withDate('mpvqcDate')
            .withGenerator('mpvqcGenerator')
            .withNickname('mpvqcNickname')
            .withFilePath('mpvqcFilePath')
            .withBlankLine()
            .withDataTag()
            .withComments([
                { time: '68', commentType: 'CommentType', comment: 'Comment 1' },
                { time: 70, commentType: 'CommentType', comment: 'Comment 2' },
            ])
            .withCommentSummary()
            .withBlankLine()

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
