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

import QtTest


MpvqcWindowTitle {
    id: objectUnderTest

    width: 400
    height: 400
    saved: true

    TestCase {
        name: "MpvqcWindowTitle"
        when: windowShown

        function test_label_data() {
            return [
                { tag: 'saved', saved: true },
                { tag: 'unsaved', saved: false },
            ]
        }

        function test_label(data) {
            objectUnderTest.saved = data.saved

            if (data.saved) {
                verify(!objectUnderTest.text.endsWith('(unsaved)'))
            } else {
                verify(objectUnderTest.text.endsWith('(unsaved)'))
            }
        }
    }

}
