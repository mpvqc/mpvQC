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


MpvqcExportView {
    id: objectUnderTest

    mpvqcApplication: QtObject {
        property var mpvqcSettings: QtObject {
            property string nickname: 'nickname'
            property bool writeHeaderDate: false
            property bool writeHeaderGenerator: false
            property bool writeHeaderNickname: false
            property bool writeHeaderVideoPath: false
        }
    }

    width: 400
    height: 400

    TestCase {
        name: "MpvqcExportView"
        when: windowShown

        function init() {
            objectUnderTest.mpvqcApplication.mpvqcSettings.nickname = 'nickname'
            objectUnderTest.mpvqcApplication.mpvqcSettings.writeHeaderDate = false
            objectUnderTest.mpvqcApplication.mpvqcSettings.writeHeaderGenerator = false
            objectUnderTest.mpvqcApplication.mpvqcSettings.writeHeaderNickname = false
            objectUnderTest.mpvqcApplication.mpvqcSettings.writeHeaderVideoPath = false
        }

        function test_export_data() {
            return [
                {
                    tag: 'nickname',
                    exec: () => { objectUnderTest.nicknameInput.input = 'other-nickname' },
                    verify: () => { compare(objectUnderTest.mpvqcApplication.mpvqcSettings.nickname, 'other-nickname') },
                },
                {
                    tag: 'header/date',
                    exec: () => { objectUnderTest.dateToggle.checked = true },
                    verify: () => { compare(objectUnderTest.mpvqcApplication.mpvqcSettings.writeHeaderDate, true) },
                },
                {
                    tag: 'header/generator',
                    exec: () => { objectUnderTest.generatorToggle.checked = true },
                    verify: () => { compare(objectUnderTest.mpvqcApplication.mpvqcSettings.writeHeaderGenerator, true) },
                },
                {
                    tag: 'header/nickname',
                    exec: () => { objectUnderTest.nicknameToggle.checked = true },
                    verify: () => { compare(objectUnderTest.mpvqcApplication.mpvqcSettings.writeHeaderNickname, true) },
                },
                {
                    tag: 'header/nickname',
                    exec: () => { objectUnderTest.pathToggle.checked = true },
                    verify: () => { compare(objectUnderTest.mpvqcApplication.mpvqcSettings.writeHeaderVideoPath, true) },
                },
            ]
        }

        function test_export(data) {
            data.exec()
            data.verify()
        }
    }

}
