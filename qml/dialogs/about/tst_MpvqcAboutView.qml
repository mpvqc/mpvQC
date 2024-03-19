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


MpvqcAboutView {
    id: objectUnderTest

    // Mock Qt.openUrlExternally
    property url calledUrl: ''
    openUrlExternally: openUrlExternallyMock
    function openUrlExternallyMock(url) { calledUrl = url }
    // end

    width: 400
    height: 400

    TestCase {
        name: 'MpvqcAboutView'
        when: windowShown

        function init() {
            objectUnderTest.calledUrl = ''
        }

        function test_click_data() {
            return [
                {
                     tag: 'github',
                     exec: () => { mouseClick(objectUnderTest.gitHubLabel) },
                     verify: () => { compare(objectUnderTest.calledUrl, 'https://mpvqc.github.io') },
                },
                {
                     tag: 'gnu',
                     exec: () => { mouseClick(objectUnderTest.licenceLabel) },
                     verify: () => { compare(objectUnderTest.calledUrl, 'https://www.gnu.org/licenses/gpl-3.0.html') },
                }
            ]
        }

        function test_click(data) {
            data.exec()
            data.verify()
        }
    }

}
