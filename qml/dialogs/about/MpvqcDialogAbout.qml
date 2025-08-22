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

import "../../shared"

MpvqcDialog2 {
    id: root

    readonly property int scrollBarWidth: 20
    readonly property int workaroundRtlIssueRightMargin: root.mpvqcApplication.LayoutMirroring.enabled ? 20 : 0

    contentHeight: Math.min(1080, mpvqcApplication.height * 0.60)

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
