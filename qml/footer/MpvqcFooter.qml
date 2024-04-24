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


Item {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    readonly property int mBottom: mpvqcApplication.maximized ? 2 : 0
    readonly property bool horizontalLayout: mpvqcSettings.layoutOrientation === Qt.Horizontal
    readonly property int mLeft: horizontalLayout
        ? 6
        : mpvqcApplication.maximized ? 2 : 0

    property alias formattingOptionsButton: _formattingOptionsButton

    height: _content.height
    visible: !mpvqcApplication.fullscreen

    Column {
        id: _content
        width: root.width
        spacing: 0

        MenuSeparator {
            topPadding: 1
            bottomPadding: 1
            width: root.width
        }

        RowLayout {
            width: _content.width

            Rectangle {
                width: root.mLeft
                color: 'transparent'
            }

            MpvqcRowSelectionLabel {
                mpvqcApplication: root.mpvqcApplication
                Layout.bottomMargin: root.mBottom
            }

            Item {
                Layout.fillWidth: true
            }

            MpvqcVideoPercentLabel {
                mpvqcApplication: root.mpvqcApplication
                horizontalAlignment: Text.AlignRight
                Layout.bottomMargin: root.mBottom
            }

            MpvqcVideoTimeLabel {
                mpvqcApplication: root.mpvqcApplication
                horizontalAlignment: Text.AlignRight
                Layout.preferredWidth: width
                Layout.bottomMargin: root.mBottom
                Layout.leftMargin: 12
            }

            Item {
                height: 25
                width: 25
                Layout.bottomMargin: root.mBottom

                ToolButton {
                    id: _formattingOptionsButton

                    property var menu: MpvqcFooterSettingsMenu
                    {
                        mpvqcApplication: root.mpvqcApplication
                        y: -height
                        transformOrigin: mirrored && !horizontalLayout ? Popup.BottomLeft : Popup.BottomRight
                    }

                    icon.source: "qrc:/data/icons/expand_more_black_24dp.svg"
                    focusPolicy: Qt.NoFocus
                    height: parent.height
                    width: parent.width + 1
                    padding: 3

                    onClicked: {
                        menu.open()
                    }
                }
            }

        }
    }

}
