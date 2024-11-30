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

MpvqcRowSelectionLabel {
    id: objectUnderTest

    width: 400
    height: 400

    mpvqcApplication: QtObject {
        property var mpvqcCommentTable: QtObject {
            property int selectedCommentIndex: -1
            property int commentCount: 0
        }
    }

    TestCase {
        name: "MpvqcRowSelectionLabel"
        when: windowShown

        function cleanup() {
            objectUnderTest.mpvqcApplication.mpvqcCommentTable.selectedCommentIndex = -1;
            objectUnderTest.mpvqcApplication.mpvqcCommentTable.commentCount = 0;
        }

        function test_label() {
            objectUnderTest.mpvqcApplication.mpvqcCommentTable.selectedCommentIndex = 0;
            objectUnderTest.mpvqcApplication.mpvqcCommentTable.commentCount = 1;
            compare(objectUnderTest.text, '1/1');

            objectUnderTest.mpvqcApplication.mpvqcCommentTable.selectedCommentIndex = 15;
            objectUnderTest.mpvqcApplication.mpvqcCommentTable.commentCount = 30;
            compare(objectUnderTest.text, '16/30');
        }
    }
}
