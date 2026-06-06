// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

ScrollView {
    id: root

    required property MpvqcAboutDialogViewModel viewModel

    readonly property MpvqcLicensesContent licensesContent: MpvqcLicensesContent {
        mpvVersion: root.viewModel.mpvVersion
        ffmpegVersion: root.viewModel.ffmpegVersion
    }

    readonly property bool isScrollBarShown: contentHeight > height

    function joinDetails(parts): string {
        // Reversed in RTL so the first entry sits rightmost, where reading starts
        return mirrored ? [...parts].reverse().join(" · ") : parts.join(" · ");
    }

    contentWidth: availableWidth

    ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
    ScrollBar.vertical.policy: isScrollBarShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff

    Flickable {
        boundsBehavior: Flickable.StopAtBounds
        contentHeight: _column.implicitHeight

        onVisibleChanged: {
            if (!visible) {
                contentY = 0;
            }
        }

        ColumnLayout {
            id: _column

            x: root.mirrored && root.isScrollBarShown ? 20 : 0
            width: root.availableWidth - (root.isScrollBarShown ? 20 : 0)
            spacing: 0

            MpvqcSectionTitle {
                text: root.licensesContent.playbackTitle
            }

            Repeater {
                model: root.licensesContent.playbackEntries

                MpvqcLicensesListItem {}
            }

            MpvqcSectionTitle {
                text: root.licensesContent.librariesTitle
            }

            Repeater {
                model: MpvqcDependencyModel {}

                MpvqcAboutListItem {
                    required property string licence
                    required property string name
                    required property string url
                    required property string version

                    text: name
                    supportingText: root.joinDetails([version, licence])
                    icon.source: MpvqcIcons.deployedCode
                    link: url

                    Layout.fillWidth: true

                    onClicked: root.viewModel.openLink(link)
                }
            }

            MpvqcSectionTitle {
                text: root.licensesContent.fontsAndIconsTitle
            }

            Repeater {
                model: root.licensesContent.fontsAndIconsEntries

                MpvqcLicensesListItem {}
            }
        }
    }

    component MpvqcSectionTitle: Label {
        color: MpvqcTheme.palette.accent
        font.pointSize: root.font.pointSize - 1
        font.weight: Font.DemiBold
        horizontalAlignment: Text.AlignLeft
        leftPadding: 16
        rightPadding: 16
        topPadding: 16
        bottomPadding: 8

        Layout.fillWidth: true
    }

    component MpvqcLicensesListItem: MpvqcAboutListItem {
        required property var modelData

        text: modelData.name
        supportingText: modelData.version ? root.joinDetails([modelData.version, modelData.licence]) : modelData.licence
        icon.source: modelData.icon
        link: modelData.url

        Layout.fillWidth: true

        onClicked: root.viewModel.openLink(link)
    }
}
