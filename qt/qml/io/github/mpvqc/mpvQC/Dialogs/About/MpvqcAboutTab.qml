// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

ScrollView {
    id: root

    required property MpvqcAboutDialogViewModel viewModel

    readonly property url appUrl: "https://mpvqc.github.io"
    readonly property url licenseUrl: "https://www.gnu.org/licenses/gpl-3.0.html"

    readonly property bool isScrollBarShown: contentHeight > height

    contentWidth: availableWidth

    ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
    ScrollBar.vertical.policy: isScrollBarShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff

    Flickable {
        boundsBehavior: Flickable.StopAtBounds
        contentHeight: _column.height

        onVisibleChanged: {
            if (!visible) {
                contentY = 0;
            }
        }

        ColumnLayout {
            id: _column

            x: root.mirrored && root.isScrollBarShown ? 20 : 0
            width: root.availableWidth - (root.isScrollBarShown ? 20 : 0)
            height: Math.max(implicitHeight, root.availableHeight)
            spacing: 0

            Image {
                source: "qrc:/data/icon.svg"
                sourceSize.width: 96
                sourceSize.height: 96
                asynchronous: true

                Layout.alignment: Qt.AlignHCenter
            }

            MpvqcHeader {
                text: root.viewModel.applicationName
                font.pointSize: 14

                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 8
            }

            Label {
                text: root.viewModel.applicationVersion
                color: MpvqcTheme.palette.hint

                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 4
            }

            Label {
                //: This text is part of the software license description
                text: qsTranslate("AboutDialog", "Copyright © mpvQC Developers")
                color: MpvqcTheme.palette.hint

                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 2
            }

            Item {
                Layout.fillHeight: true
                Layout.minimumHeight: 24
            }

            MpvqcAboutListItem {
                objectName: "websiteRow"

                //: Label of the row linking to the project website
                text: qsTranslate("AboutDialog", "Website")
                supportingText: root.appUrl
                icon.source: MpvqcIcons.language
                link: root.appUrl

                Layout.fillWidth: true

                onClicked: root.viewModel.openLink(link)
            }

            MpvqcAboutListItem {
                objectName: "licenseRow"

                //: This text is part of the software license description. This is the name of the license being used.
                text: qsTranslate("AboutDialog", "GNU General Public License, version 3 or later")
                //: This text is part of the software license description
                supportingText: qsTranslate("AboutDialog", "This program comes with absolutely no warranty.")
                icon.source: MpvqcIcons.description
                link: root.licenseUrl

                Layout.fillWidth: true

                onClicked: root.viewModel.openLink(link)
            }

            MpvqcAboutListItem {
                objectName: "copyVersionRow"

                text: qsTranslate("AboutDialog", "Copy version info to clipboard")
                supportingText: qsTranslate("AboutDialog", "Powered by Python %1").arg(root.viewModel.pythonVersion)
                icon.source: MpvqcIcons.contentCopy
                enabled: true

                Layout.fillWidth: true

                onClicked: {
                    root.viewModel.copyVersionInfoToClipboard();
                    icon.source = MpvqcIcons.check;
                }
            }
        }
    }
}
