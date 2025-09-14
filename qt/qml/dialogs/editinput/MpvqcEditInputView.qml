// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

ColumnLayout {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcPlayerFilesPyObject: mpvqcApplication.mpvqcPlayerFilesPyObject
    readonly property var mpvqcTheme: mpvqcApplication.mpvqcTheme

    readonly property alias textArea: _textArea

    signal accepted
    signal reset

    function acceptContent(): void {
        _textArea.textDocument.save();
        root.accepted();
    }

    function restorePreviousContent(): void {
        _textArea.text = mpvqcPlayerFilesPyObject.default_input_conf_content;
        root.reset();
    }

    Label {
        id: label

        property string url: "https://mpv.io/manual/master/#list-of-input-commands"
        property string text1: qsTranslate("InputConfEditDialog", "Changes to the input.conf are available after a restart.")
        property string text2: qsTranslate("InputConfEditDialog", "Learn more")

        Layout.topMargin: 20
        Layout.fillWidth: true
        horizontalAlignment: Text.AlignLeft

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
        color: root.mpvqcTheme.control

        Layout.topMargin: 20
        Layout.preferredHeight: 1
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

            textDocument.source: root.mpvqcPlayerFilesPyObject.input_conf_url
        }
    }

    Rectangle {
        color: root.mpvqcTheme.control

        Layout.preferredHeight: 1
        Layout.fillWidth: true
    }
}
