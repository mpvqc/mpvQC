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
import QtQuick.Controls

import pyobjects


FocusScope {
    id: root

    required property var mpvqcApplication

    readonly property alias mpvqcCommentTable: _mpvqcTable
    readonly property alias mpvqcSearchBox: _mpvqcSearchBox
    property bool haveComments: _mpvqcTable.count > 0

    Column {
        width: root.width

        MpvqcPlaceholder {
            width: root.width
            height: haveComments ? 0 : root.height
        }

        MpvqcTable {
            id: _mpvqcTable

            width: root.width
            height: haveComments ? root.height : 0
            focus: true
            model: MpvqcCommentModelPyObject {}
            mpvqcApplication: root.mpvqcApplication

            MpvqcSearchBox {
                id: _mpvqcSearchBox

                mpvqcApplication: root.mpvqcApplication
                mpvqcCommentTable: _mpvqcTable

                onNextOccurrenceRequested: {
                    console.log('On nextOccurrenceRequested')
                }

                onPreviousOccurrenceRequested: {
                    console.log('On previousOccurrenceRequested')
                }
            }
        }

    }

}
