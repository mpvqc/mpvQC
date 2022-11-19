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


Item {
    id: root

    required property var mpvqcApplication
    property var mpvqcManager: mpvqcApplication.mpvqcManager

    height: menuBar.height
    visible: !mpvqcApplication.fullscreen

    MpvqcWindowMoveHandler {
        mpvqcApplication: root.mpvqcApplication
    }

    MpvqcHeaderTapHandler {
        mpvqcApplication: root.mpvqcApplication
    }

    Row {
        width: root.width
        spacing: 0

        MenuBar {
            id: menuBar

            background: Rectangle {
                color: "transparent"
            }

            MpvqcMenuFile {
                mpvqcApplication: root.mpvqcApplication
            }

            MpvqcMenuVideo {
                mpvqcApplication: root.mpvqcApplication
            }

            MpvqcMenuOptions {
               mpvqcApplication: root.mpvqcApplication
            }

            MpvqcMenuHelp {
                mpvqcApplication: root.mpvqcApplication
            }
        }

        MpvqcWindowTitle {
            saved: root.mpvqcManager.saved
            width: root.width - menuBar.width * 2
            height: menuBar.height
        }

        MpvqcWindowControls {
            mpvqcApplication: root.mpvqcApplication
            width: menuBar.width
            height: menuBar.height
        }
    }

}
