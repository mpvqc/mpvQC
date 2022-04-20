/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick
import QtQuick.Controls
import pyobjects


Item {
    id: headerBarContent
    width: parent.width
    height: menuBar.height

    Row {
        width: parent.width
        spacing: 0

        MenuBar {
            id: menuBar
            background: Rectangle {
                color: "transparent"
            }

            MpvqcFileMenu {}
            MpvqcVideoMenu {}
            MpvqcOptionsMenu {}
            MpvqcHelpMenu {}
        }

        Label {
            text: "mpvQC"
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            width: headerBarContent.width - menuBar.width * 2
            height: menuBar.height
            elide: TranslationPyObject.rtl_enabled ? Text.ElideLeft: Text.ElideRight
        }

        Item {
            id: buttonWrapper
            width: menuBar.width
            height: menuBar.height

            MpvqcWindowMinimizeButton {
                height: buttonWrapper.height
                anchors.right: maximizeButton.left

                onClicked: {
                    appWindow.showMinimized()
                }
            }

            MpvqcWindowMaximizeButton {
                id: maximizeButton
                height: buttonWrapper.height
                anchors.right: closeButton.left
                maximized: appWindow.visibility === Window.Maximized

                onClicked: {
                    utils.toggleMaximized()
                }
            }

            MpvqcWindowCloseButton {
                id: closeButton
                height: buttonWrapper.height
                anchors.right: buttonWrapper.right

                onClicked: {
                    appWindow.close()
                }
            }
        }
    }

}
