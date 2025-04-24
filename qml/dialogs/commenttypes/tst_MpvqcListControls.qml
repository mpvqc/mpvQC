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

MpvqcListControls {
    id: objectUnderTest

    width: 400
    height: 400

    TestCase {
        name: "MpvqcListControls"
        when: windowShown

        SignalSpy {
            id: upClickedSpy
            target: objectUnderTest
            signalName: "upClicked"
        }
        SignalSpy {
            id: downClickedSpy
            target: objectUnderTest
            signalName: "downClicked"
        }
        SignalSpy {
            id: editClickedSpy
            target: objectUnderTest
            signalName: "editClicked"
        }
        SignalSpy {
            id: deleteClickedSpy
            target: objectUnderTest
            signalName: "deleteClicked"
        }

        function cleanup() {
            upClickedSpy.clear();
            downClickedSpy.clear();
            editClickedSpy.clear();
            deleteClickedSpy.clear();
        }

        function test_click_data() {
            return [
                {
                    tag: "upButton",
                    item: objectUnderTest.upButton,
                    spy: upClickedSpy
                },
                {
                    tag: "downButton",
                    item: objectUnderTest.downButton,
                    spy: downClickedSpy
                },
                {
                    tag: "editButton",
                    item: objectUnderTest.editButton,
                    spy: editClickedSpy
                },
                {
                    tag: "deleteButton",
                    item: objectUnderTest.deleteButton,
                    spy: deleteClickedSpy
                },
            ];
        }

        function test_click(data) {
            mouseClick(data.item);
            compare(data.spy.count, 1);
        }
    }
}
