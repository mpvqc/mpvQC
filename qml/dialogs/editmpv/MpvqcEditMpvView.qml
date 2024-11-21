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

ColumnLayout {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcPlayerFilesPyObject: mpvqcApplication.mpvqcPlayerFilesPyObject
    readonly property var mpvqcTheme: mpvqcApplication.mpvqcTheme

    readonly property alias textArea: _textArea

    property var accept: () => {
        _textArea.textDocument.save();
    }

    property var reset: () => {
        _textArea.text = mpvqcPlayerFilesPyObject.default_mpv_conf_content;
    }

    Label {
        id: label

        property string url: "https://mpv.io/manual/master/#configuration-files"
        property string text1: qsTranslate("MpvConfEditDialog", "Changes to the mpv.conf are available after a restart.")
        property string text2: qsTranslate("MpvConfEditDialog", "Learn more")

        Layout.topMargin: 20
        Layout.fillWidth: true
        horizontalAlignment: Text.AlignLeft

        font.pointSize: 11
        font.weight: Font.DemiBold

        text: `${text1} <a href="${url}">${text2}</a>.`

        onLinkActivated: link => {
            Qt.openUrlExternally(link);
        }

        MouseArea {
            anchors.fill: parent
            acceptedButtons: Qt.NoButton
            cursorShape: label.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
            hoverEnabled: true
        }

        ToolTip {
            y: label.height + 5
            text: label.url
            delay: 500
            visible: label.hoveredLink
        }
    }

    Rectangle {
        height: 2
        color: root.mpvqcTheme.control
        Layout.topMargin: 20
        Layout.fillWidth: true
    }

    ScrollView {
        id: _scrollView

        Layout.fillWidth: true
        Layout.fillHeight: true

        ScrollBar.horizontal.policy: contentWidth > width ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
        ScrollBar.vertical.policy: contentHeight > height ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff

        TextArea {
            id: _textArea

            background: null
            leftPadding: _scrollView.mirrored ? 22 : 0
            font.family: "Noto Sans Mono"
            font.pointSize: 11

            textDocument.source: root.mpvqcPlayerFilesPyObject.mpv_conf_url
        }
    }

    Rectangle {
        height: 2
        color: root.mpvqcTheme.control
        Layout.fillWidth: true
    }
}
