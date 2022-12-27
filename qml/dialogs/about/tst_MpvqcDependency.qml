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


MpvqcDependency {
    id: objectUnderTest

    width: 400
    height: 400

    dependency: 'https://github.com/mpvqc/mpvQC'
    version: '1.0.0'
    licence: 'MIT'
    url: 'https://github.com/mpvqc/mpvQC'

    // Mock Qt.openUrlExternally
    property url calledUrl: ''
    openUrlExternally: openUrlExternallyMock
    function openUrlExternallyMock(url) { calledUrl = url }
    // end

    TestCase {
        name: 'MpvqcDependency'
        when: windowShown

        function init() {
            objectUnderTest.calledUrl = ''
        }

        function test_click() {
            mouseClick(objectUnderTest.urlLabel)
            compare(objectUnderTest.calledUrl, objectUnderTest.url)
        }
    }

}
