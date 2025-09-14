// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material
import QtTest

Item {

    MpvqcMenu {
        id: objectUnderTest1

        Action {
            text: "Short text"
        }
    }

    MpvqcMenu {
        id: objectUnderTest2

        Action {
            text: "Short text"
        }
        MenuSeparator {}
    }

    MpvqcMenu {
        id: objectUnderTest3

        Action {
            text: "Very very long text so that we can compare"
        }
    }

    TestCase {
        name: "MpvqcMenu"

        function test_width_data() {
            return [
                {
                    tag: "same",
                    equals: "equals",
                    obj1: objectUnderTest1,
                    obj2: objectUnderTest2
                },
                {
                    tag: "different",
                    obj1: objectUnderTest1,
                    obj2: objectUnderTest3
                },
            ];
        }

        function test_width(data) {
            if (data.equals) {
                verify(data.obj1.width === data.obj2.width);
            } else {
                verify(data.obj1.width < data.obj2.width);
            }
        }
    }
}
