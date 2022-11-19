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
import "MpvqcDocumentFileExporter.js" as TestObject


Item {

    property var absPathGetterFunc: function(path) { return 'abs::' + path }
    property var nicknameGetterFunc: function() { return 'test-nickname' }
    property var commentGetterFunc: function() { return [
        { time: '68', commentType: 'CommentType', comment: 'Comment 1' },
    ] }
    property var timeFormatFunc: function(sec) { return 'transformed' }

    TestCase {
        name: "MpvqcDocumentFileExporter::ExportContentGenerator"

        property var classUnderTest: function(settingsGetterFunc) {
            return new TestObject.ExportContentGenerator(
                absPathGetterFunc, nicknameGetterFunc, commentGetterFunc, settingsGetterFunc, timeFormatFunc
            )
        }

        function test_content_export() {
            const settingsGetterFunc = function() {
                return {
                    writeHeaderDate: false,
                    writeHeaderGenerator: false,
                    writeHeaderNickname: false,
                    writeHeaderVideoPath: true,
                }
            }
            const testObject = classUnderTest(settingsGetterFunc)
            const video = 'test-video.mkv'
            const content = testObject.createExportContent(video)
            verify(!content.includes('date      :'), "'date      :' present")
            verify(!content.includes('generator :'), "'generator :' present")
            verify(!content.includes('nick      :'), "'nick      :' present")
            verify(content.includes('path      :'), "'path      :' missing")
            verify(content.includes(video), `'${video}' missing`)
            verify(content.includes('[FILE]'), "'[FILE]' missing")
            verify(content.includes('[DATA]'), "'[DATA]' missing")
            verify(content.includes('[transformed] '), "'[transformed] ' missing")
            verify(content.includes('# total lines:'), "'# total lines:' missing")
        }

        function test_content_backup() {
            const testObject = classUnderTest()
            const video = 'test-video.mkv'
            const content = testObject.createBackupContent(video)
            verify(content.includes('date      :'), "'date      :' missing")
            verify(content.includes('generator :'), "'generator :' missing")
            verify(content.includes('nick      :'), "'nick      :' missing")
            verify(content.includes('path      :'), "'path      :' missing")
            verify(content.includes(video), `'${video}' missing`)
            verify(content.includes('[FILE]'), "'[FILE]' missing")
            verify(content.includes('[DATA]'), "'[DATA]' missing")
            verify(content.includes('[transformed] '), "'[transformed] ' missing")
            verify(content.includes('# total lines:'), "'# total lines:' missing")
        }

    }

    TestCase {
        name: "MpvqcDocumentFileExporter::DataGenerator"

        property var classUnderTest: function(commentGetterFunc) {
            return new TestObject.DataGenerator(absPathGetterFunc, nicknameGetterFunc, commentGetterFunc)
        }

        function test_date() {
            const testObject = classUnderTest(commentGetterFunc)
            const video = ''
            const data = testObject.generateDataWith(video)
            verify(data.date)
        }

        function test_generator() {
            const testObject = classUnderTest(commentGetterFunc)
            const video = ''
            Qt.application.name = 'test-name'
            Qt.application.version = 'test-version'
            const data = testObject.generateDataWith(video)
            compare('test-name test-version', data.generator)
        }

        function test_nickname() {
            const testObject = classUnderTest(commentGetterFunc)
            const video = ''
            const data = testObject.generateDataWith(video)
            compare('test-nickname', data.nickname)
        }

        function test_videoPath_available() {
            const testObject = classUnderTest(commentGetterFunc)
            const video = 'file:///video.mp4'
            const data = testObject.generateDataWith(video)
            compare('abs::file:///video.mp4', data.videoPath)
        }

        function test_videoPath_unavailable() {
            const testObject = classUnderTest(commentGetterFunc)
            const video = ''
            const data = testObject.generateDataWith(video)
            compare('', data.videoPath)
        }

        function test_comments() {
            const testObject = classUnderTest(commentGetterFunc)
            const video = ''
            const data = testObject.generateDataWith(video)
            compare(commentGetterFunc(), data.comments)
        }

    }

    TestCase {
        name: "MpvqcDocumentFileExporter::ExportSettingsGenerator"

        property var classUnderTest: function(settingsGetterFunc) {
            return new TestObject.SettingsGenerator(settingsGetterFunc)
        }

        function test_export_settings() {
            const expected = {
                writeHeaderDate: false,
                writeHeaderGenerator: false,
                writeHeaderNickname: false,
                writeHeaderVideoPath: false,
            }
            const testObject = classUnderTest(() => expected)
            compare(expected, testObject.generateExportSettings())
        }

        function test_backup_settings() {
            const expected = {
                writeHeaderDate: true,
                writeHeaderGenerator: true,
                writeHeaderNickname: true,
                writeHeaderVideoPath: true,
            }
            const testObject = classUnderTest()
            compare(expected, testObject.generateBackupSettings())
        }
    }


    TestCase {
        name: "MpvqcDocumentFileExporter::DocumentFileCombiner::generateDocumentFrom"

        property var timeFormatFunc: function(sec) { return 'transformed' }
        property var funcUnderTest: new TestObject.DocumentFileCombiner(timeFormatFunc).generateDocumentFrom

        function test_documentStartsWithHeader() {
            const settings = provideTruthySettings()
            const data = provideData()
            const document = funcUnderTest(data, settings)
            verify(document.startsWith('[FILE]'))
        }

        function test_headerSeperatedFromComments() {
            const settings = provideTruthySettings()
            const data = provideData()
            const document = funcUnderTest(data, settings)
            verify(document.includes('\n\n[DATA]'))
        }

        function test_exportDate() {
            const settings = provideTruthySettings()
            const data = provideData()
            const document = funcUnderTest(data, settings)
            verify(document.includes(data.date))
        }

        function test_exportDateNot() {
            const settings = provideTruthySettings()
            settings.writeHeaderDate = false
            const data = provideData()
            const document = funcUnderTest(data, settings)
            verify(!document.includes(data.date))
        }

        function test_exportGenerator() {
            const settings = provideTruthySettings()
            const data = provideData()
            const document = funcUnderTest(data, settings)
            verify(document.includes(data.generator))
        }

        function test_exportGeneratorNot() {
            const settings = provideTruthySettings()
            settings.writeHeaderGenerator = false
            const data = provideData()
            const document = funcUnderTest(data, settings)
            verify(!document.includes(data.generator))
        }

        function test_exportNickname() {
            const settings = provideTruthySettings()
            const data = provideData()
            const document = funcUnderTest(data, settings)
            verify(document.includes(data.nickname))
        }

        function test_exportNicknameNot() {
            const settings = provideTruthySettings()
            settings.writeHeaderNickname = false
            const data = provideData()
            const document = funcUnderTest(data, settings)
            verify(!document.includes(data.nickname))
        }

        function test_exportVideoPath() {
            const settings = provideTruthySettings()
            const data = provideData()
            const document = funcUnderTest(data, settings)
            verify(document.includes(data.videoPath))
        }

        function test_exportVideoPathNot() {
            const settings = provideTruthySettings()
            settings.writeHeaderVideoPath = false
            const data = provideData()
            const document = funcUnderTest(data, settings)
            verify(!document.includes(data.videoPath))
        }

        function test_exportContainsComments() {
            const settings = provideTruthySettings()
            const data = provideData()
            const document = funcUnderTest(data, settings)
            for (const comment of data.comments) {
                verify(document.includes(comment.comment))
            }
        }

        function test_exportContainsCommentSummary() {
            const settings = provideTruthySettings()
            const data = provideData()
            const document = funcUnderTest(data, settings)
            verify(document.includes('# total lines:'))
        }

        function test_exportEndsWithNewLine() {
            const settings = provideTruthySettings()
            const data = provideData()
            const document = funcUnderTest(data, settings)
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
                writeHeaderDate: true,
                writeHeaderGenerator: true,
                writeHeaderNickname: true,
                writeHeaderVideoPath: true,
            }
        }
    }

    TestCase {
        name: "MpvqcDocumentFileExporter::DocumentBuilder"

        property var classUnderTest: function() { return new TestObject.DocumentBuilder(timeFormatFunc) }

        function test_build_data() { return [
            {
                tag: ' ',
                expected: '',
                actual: function() {
                    const builder = classUnderTest()
                    return builder.build()
                }
            },
            {
                tag: '[FILE]',
                expected: '[FILE]',
                actual: function() {
                    const builder = classUnderTest()
                    builder.addFileTag()
                    return builder.build()
                }
            },
            {
                tag: 'date',
                expected: 'date      : mpvqcDate',
                actual: function() {
                    const builder = classUnderTest()
                    builder.addDate('mpvqcDate')
                    return builder.build()
                }
            },
            {
                tag: 'generator',
                expected: 'generator : mpvqcGenerator',
                actual: function() {
                    const builder = classUnderTest()
                    builder.addGenerator('mpvqcGenerator')
                    return builder.build()
                }
            },
            {
                tag: 'nick',
                expected: 'nick      : mpvqcNickname',
                actual: function() {
                    const builder = classUnderTest()
                    builder.addNickname('mpvqcNickname')
                    return builder.build()
                }
            },
            {
                tag: 'path',
                expected: 'path      : mpvqcFilePath',
                actual: function() {
                    const builder = classUnderTest()
                    builder.addFilePath('mpvqcFilePath')
                    return builder.build()
                }
            },
            {
                tag: '\\n',
                expected: '\n',
                actual: function() {
                    const builder = classUnderTest()
                    builder.addBlankLine()
                    builder.addBlankLine()
                    return builder.build()
                }
            },
            {
                tag: '[DATA]',
                expected: '[DATA]',
                actual: function() {
                    const builder = classUnderTest()
                    builder.addDataTag()
                    return builder.build()
                }
            },
            {
                tag: 'comments',
                expected: '[transformed] [CommentType] Comment 1\n[transformed] [CommentType] Comment 2',
                actual: function() {
                    const builder = classUnderTest()
                    builder.addComments([
                        { time: '68', commentType: 'CommentType', comment: 'Comment 1' },
                        { time: 70, commentType: 'CommentType', comment: 'Comment 2' },
                    ])
                    return builder.build()
                }
            },
            {
                tag: '# total lines: 0',
                expected: '# total lines: 0',
                actual: function() {
                    const builder = classUnderTest()
                    builder.addCommentSummary()
                    return builder.build()
                }
            },
            {
                tag: '# total lines: 1',
                expected: '[transformed] [CommentType] Comment 1\n# total lines: 1',
                actual: function() {
                    const builder = classUnderTest()
                    builder.addComments([
                        { time: '68', commentType: 'CommentType', comment: 'Comment 1' }
                    ])
                    builder.addCommentSummary()
                    return builder.build()
                }
            },
            {
                tag: '# total lines: 2',
                expected: '[transformed] [CommentType] Comment 1\n[transformed] [CommentType] Comment 2\n# total lines: 2',
                actual: function() {
                    const builder = classUnderTest()
                    builder.addComments([
                        { time: '68', commentType: 'CommentType', comment: 'Comment 1' },
                        { time: 70, commentType: 'CommentType', comment: 'Comment 2' },
                    ])
                    builder.addCommentSummary()
                    return builder.build()
                }
            },
            {
                tag: 'complete',
                expected: _complete(),
                actual: function() {
                    const builder = classUnderTest()
                    builder.addFileTag()
                    builder.addDate('mpvqcDate')
                    builder.addGenerator('mpvqcGenerator')
                    builder.addNickname('mpvqcNickname')
                    builder.addFilePath('mpvqcFilePath')
                    builder.addBlankLine()
                    builder.addDataTag()
                    builder.addComments([
                            { time: '68', commentType: 'CommentType', comment: 'Comment 1' },
                            { time: 70, commentType: 'CommentType', comment: 'Comment 2' },
                        ])
                    builder.addCommentSummary()
                    builder.addBlankLine()
                    return builder.build()
                }
            }
        ] }

        function test_build(data) {
            compare(data.actual(), data.expected)
        }

        function _complete() {
         return '[FILE]
date      : mpvqcDate
generator : mpvqcGenerator
nick      : mpvqcNickname
path      : mpvqcFilePath

[DATA]
[transformed] [CommentType] Comment 1
[transformed] [CommentType] Comment 2
# total lines: 2
'
        }
    }

}
