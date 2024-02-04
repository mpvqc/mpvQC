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


MouseArea {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings

    propagateComposedEvents: true

    signal afterPressed()

    function splitViewHandleHovered(state: bool): void {
		if (!state) {
			cursorShape = Qt.ArrowCursor
		} else if (mpvqcSettings.layoutOrientation === Qt.Vertical) {
			cursorShape = Qt.SizeVerCursor
		} else {
			cursorShape = Qt.SizeHorCursor
		}
    }

    onPressed: (event) => {
        event.accepted = false
        root.afterPressed()
    }

}
