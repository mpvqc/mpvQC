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

import models


Item {
    id: testHelper

    width: 400
    height: 400

    MpvqcCommentTypesValidator {
        id: objectUnderTest

        model: MpvqcCommentTypesModel {}
        reverseTranslator: QtObject {
            function lookup(commentType) {
                if (commentType.startsWith('i am matching a reverse translation')) {
                    return 'Translation'
                }
                return commentType
            }
        }
    }

    TestCase {
        name: "MpvqcCommentTypesValidator"
        when: windowShown

        function init() {
            if (objectUnderTest.model) objectUnderTest.model.destroy()
            objectUnderTest.model = Qt.createQmlObject('import models; MpvqcCommentTypesModel {}', testHelper)
        }

        function test_validateNewCommentType_data() {
            return [
                { tag: 'empty', commentType: '', error: 'A comment type must not be blank' },
                { tag: 'existing', commentType: 'Translation', error: 'Comment type already exists' },
                { tag: 'english', commentType: 'i am matching a reverse translation', error: 'Comment type already exists' },
                { tag: 'characters', commentType: ',', error: 'Characters \',[]\' not allowed' },
                { tag: 'correct', commentType: 'anything', error: null },
            ]
        }

        function test_validateNewCommentType(data) {
            const error = objectUnderTest.validateNewCommentType(data.commentType)
            compare(error, data.error)
        }

        function test_validateEditingOf_data() {
            return [
                { tag: 'empty', commentType: '', error: 'A comment type must not be blank' },
                { tag: 'existing-1', commentType: 'Translation', error: null },
                { tag: 'existing-2', commentType: 'Spelling', error: 'Comment type already exists' },
                { tag: 'english', commentType: 'i am matching a reverse translation', error: null },
                { tag: 'characters', commentType: ',', error: 'Characters \',[]\' not allowed' },
                { tag: 'correct', commentType: 'anything', error: null },
            ]
        }

        function test_validateEditingOf(data) {
            const error = objectUnderTest.validateEditingOf('Translation', data.commentType)
            compare(error, data.error)
        }

    }

}
