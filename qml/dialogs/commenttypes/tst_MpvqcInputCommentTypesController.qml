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

    property string commentType1: 'abcde'
    property string commentType2: 'vwxyz'
    property string commentType3: '-.-'

    MpvqcCommentTypesViewController {
        id: objectUnderTest

        selectedIndex: 0
        model: MpvqcCommentTypesModel {}

        property bool editClickedCalled: false
        property var editClickedParam: undefined

        function reset() {
            editClickedCalled = false
            editClickedParam = undefined

            model.clear()
            model.add(testHelper.commentType1)
            model.add(testHelper.commentType2)

            modelCopy.clear()
            modelCopy.add(testHelper.commentType1)
            modelCopy.add(testHelper.commentType2)

            selectedIndex = 0
        }

        onEditClicked: (something) => {
            editClickedCalled = true
            editClickedParam = something
        }

        TestCase {
            name: "MpvqcCommentTypesViewController"
            when: windowShown

            function _commentTypeInOriginalAtIndex(index: int): string {
                const item = objectUnderTest.model.get(index)
                return item ? item.type : undefined
            }

            function _commentTypeInCopyAtIndex(index: int): string {
                const item = objectUnderTest.modelCopy.get(index)
                return item ? item.type : undefined
            }

            function init() {
                objectUnderTest.reset()
            }

            function test_add() {
                objectUnderTest.add (testHelper.commentType3)
                compare(_commentTypeInCopyAtIndex(2), testHelper.commentType3)
            }

            function test_replaceWith() {
                const index = 1

                objectUnderTest.selectedIndex = index
                objectUnderTest.replaceWith (testHelper.commentType3)

                compare(_commentTypeInCopyAtIndex(index), testHelper.commentType3)
            }

            function test_moveUp() {
                compare(_commentTypeInCopyAtIndex(0), testHelper.commentType1)
                compare(_commentTypeInCopyAtIndex(1), testHelper.commentType2)

                objectUnderTest.selectedIndex = 1
                objectUnderTest.moveUp()

                compare(_commentTypeInCopyAtIndex(0), testHelper.commentType2)
                compare(_commentTypeInCopyAtIndex(1), testHelper.commentType1)
            }

            function test_moveDown() {
                compare(_commentTypeInCopyAtIndex(0), testHelper.commentType1)
                compare(_commentTypeInCopyAtIndex(1), testHelper.commentType2)

                objectUnderTest.selectedIndex = 0
                objectUnderTest.moveDown()

                compare(_commentTypeInCopyAtIndex(0), testHelper.commentType2)
                compare(_commentTypeInCopyAtIndex(1), testHelper.commentType1)
            }

            function test_startEditing() {
                objectUnderTest.startEditing()
                verify(objectUnderTest.editClickedCalled)
                compare(objectUnderTest.editClickedParam, testHelper.commentType1)

            }

            function test_deleteItem() {
                objectUnderTest.selectedIndex = 1
                objectUnderTest.deleteItem()

                compare(objectUnderTest.modelCopy.count, 1)
                compare(_commentTypeInCopyAtIndex(0), testHelper.commentType1)

                objectUnderTest.selectedIndex = 0
                objectUnderTest.deleteItem()

                compare(objectUnderTest.modelCopy.count, 0)
            }

            function test_acceptModelCopyEmpty() {
                objectUnderTest.modelCopy.clear()

                compare(objectUnderTest.modelCopy.count, 0)
                compare(objectUnderTest.model.count, 2)

                objectUnderTest.acceptModelCopy()

                verify(objectUnderTest.model.count > 5)
                verify(objectUnderTest.modelCopy.count > 5)
            }

            function test_acceptModelCopy() {
                objectUnderTest.add(testHelper.commentType3)

                compare(objectUnderTest.model.count, 2)
                compare(objectUnderTest.modelCopy.count, 3)
                compare(_commentTypeInCopyAtIndex(2), testHelper.commentType3)

                objectUnderTest.acceptModelCopy()

                compare(objectUnderTest.model.count, 3)
                compare(objectUnderTest.modelCopy.count, 3)

                compare(_commentTypeInCopyAtIndex(2), testHelper.commentType3)
                compare(_commentTypeInOriginalAtIndex(2), testHelper.commentType3)
            }
        }
    }

}
