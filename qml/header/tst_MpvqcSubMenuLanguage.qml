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

Item {
    id: testHelper
    width: 400
    height: 400

    property var settingsLanguage: undefined

    MpvqcSubMenuLanguage {
        id: objectUnderTest

        mpvqcApplication: QtObject {
            property var mpvqcSettings: QtObject {
                property alias language: testHelper.settingsLanguage
            }
        }
    }

    TestCase {
        name: "MpvqcSubMenuLanguage"

        function cleanup() {
            Qt.uiLanguage = "";
            testHelper.settingsLanguage = "";
        }

        function test_checked_data() {
            return [
                {
                    tag: "en-US",
                    qtUiLanguage: "en-US"
                },
                {
                    tag: "he-IL",
                    qtUiLanguage: "he-IL"
                },
            ];
        }

        function test_checked(data) {
            Qt.uiLanguage = data.qtUiLanguage;
            const checkedItem = findCheckedItem();
            verify(checkedItem);
            compare(checkedItem.identifier, data.qtUiLanguage);
        }

        function findCheckedItem() {
            const count = objectUnderTest.repeater.count;
            for (let idx = 0; idx < count; idx++) {
                const item = objectUnderTest.repeater.itemAt(idx);
                if (item.checked) {
                    return item;
                }
            }
            return null;
        }

        function test_selectLanguage_data() {
            return [
                {
                    tag: "de-DE",
                    select: "de-DE"
                },
                {
                    tag: "it-IT",
                    select: "it-IT"
                },
            ];
        }

        function test_selectLanguage(data) {
            const item = findItemWith(data.select);
            item.timer.interval = 0;
            item.changeLanguage();
            wait(10);
            compare(testHelper.settingsLanguage, data.select);
            compare(Qt.uiLanguage, data.select);
        }

        function findItemWith(identifier) {
            const count = objectUnderTest.repeater.count;
            for (let idx = 0; idx < count; idx++) {
                const item = objectUnderTest.repeater.itemAt(idx);
                if (item.identifier === identifier) {
                    return item;
                }
            }
            return null;
        }
    }
}
