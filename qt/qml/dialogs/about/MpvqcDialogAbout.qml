// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../../shared"

MpvqcDialog {
    id: root

    readonly property int scrollBarWidth: 20
    readonly property int workaroundRtlIssueRightMargin: root.mpvqcApplication.LayoutMirroring.enabled ? 20 : 0

    contentHeight: Math.min(1080, mpvqcApplication.height * 0.6)

    contentItem: ScrollView {
        readonly property bool isVerticalScollBarShown: contentHeight > root.height

        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
        ScrollBar.vertical.policy: isVerticalScollBarShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff

        contentWidth: isVerticalScollBarShown ? root.contentWidth - root.scrollBarWidth : root.contentWidth

        ColumnLayout {
            anchors.fill: parent
            anchors.rightMargin: root.workaroundRtlIssueRightMargin

            MpvqcAboutView {
                Layout.fillWidth: true
            }

            MpvqcCreditsView {
                Layout.fillWidth: true
            }

            MpvqcLibraryView {
                Layout.fillWidth: true
                mpvqcApplication: root.mpvqcApplication
            }
        }
    }
}
