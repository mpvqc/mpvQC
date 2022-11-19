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
import QtQuick.Layouts
import helpers


Item {
    height: footer.height
    visible: !appWindow.displayVideoFullScreen

    readonly property bool isMaximized: utils.isMaximized()
    readonly property int marginTop: 4
    readonly property int marginOther: isMaximized ? 6 : 0

    Column {
        id: footer
        width: parent.width
        spacing: 0

        MenuSeparator {
            topPadding: 1
            bottomPadding: 1
            width: parent.width
        }

        RowLayout {
            width: parent.width

            MpvqcRowSelectionLabel {
                Layout.bottomMargin: marginOther
                Layout.leftMargin: marginOther
            }

            Item { Layout.fillWidth: true }

            MpvqcVideoPercentLabel {
                horizontalAlignment: Text.AlignRight
                Layout.bottomMargin: marginOther
            }

            MpvqcVideoTimeLabel {
                horizontalAlignment: Text.AlignRight
                Layout.preferredWidth: preferredLabelWidth
                Layout.bottomMargin: marginOther
            }

            Item {
                height: 25
                width: 25
                Layout.bottomMargin: marginOther
                Layout.rightMargin: marginOther

                ToolButton {
                    icon.source: "qrc:/data/icons/expand_more_black_24dp.svg"
                    focusPolicy: Qt.NoFocus
                    height: parent.height
                    width: parent.width + 1
                    padding: 3

                    onClicked: {
                        menu.open()
                    }

                    MpvqcFooterSettingsMenu {
                        id: menu
                    }
                }
            }

        }
    }

}
