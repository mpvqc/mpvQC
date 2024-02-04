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

    readonly property alias mpvqcCommentTable: _mpvqcCommentTable
    property bool haveComments: _mpvqcCommentTable.count > 0

    Column {
        width: root.width

        MpvqcPlaceholder {
            width: root.width
            height: haveComments ? 0 : root.height
        }

        MpvqcTable {
            id: _mpvqcCommentTable

            width: root.width
            height: haveComments ? root.height : 0
            focus: true
            model: MpvqcCommentModelPyObject {}
            mpvqcApplication: root.mpvqcApplication

			MpvqcSearchPopup {
				id: _searchBox

				mpvqcApplication: root.mpvqcApplication
				mpvqcCommentTable: _mpvqcCommentTable

				onNextOccurrenceRequested: {
					console.log('On nextOccurrenceRequested')
				}

				onPreviousOccurrenceRequested: {
					console.log('On previousOccurrenceRequested')
				}
			}
        }

    }

    Shortcut {
        sequence: 'ctrl+f'
        autoRepeat: false
        enabled: !mpvqcApplication.fullscreen && root.haveComments && !_mpvqcCommentTable.currentlyEditing

        onActivated: _searchBox.showSearchBox()
    }

    Shortcut {
        sequence: 'f'
        autoRepeat: false

        onActivated: root.mpvqcApplication.toggleFullScreen()
    }

    Shortcut {
        sequence: 'Esc'
        autoRepeat: false
        enabled: root.mpvqcApplication.fullscreen

        onActivated: root.mpvqcApplication.disableFullScreen()
    }
}
