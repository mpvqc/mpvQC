// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

MpvqcAboutScrollView {
    id: root

    required property MpvqcAboutDialogViewModel viewModel

    readonly property MpvqcLicensesContent licensesContent: MpvqcLicensesContent {
        mpvVersion: root.viewModel.mpvVersion
        ffmpegVersion: root.viewModel.ffmpegVersion
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

    function joinDetails(parts): string {
        // Reversed in RTL so the first entry sits rightmost, where reading starts
        return mirrored ? [...parts].reverse().join(" · ") : parts.join(" · ");
    }

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

            width: root.availableWidth
            spacing: MpvqcConstants.dialogSectionSpacing

            MpvqcSectionCard {
                title: root.licensesContent.playbackTitle

                Layout.fillWidth: true

                Repeater {
                    model: root.licensesContent.playbackEntries

                    MpvqcLicensesListItem {}
                }
            }

            MpvqcSectionCard {
                title: root.licensesContent.librariesTitle

                Layout.fillWidth: true

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
            }

            MpvqcSectionCard {
                title: root.licensesContent.fontsAndIconsTitle

                Layout.fillWidth: true

                Repeater {
                    model: root.licensesContent.fontsAndIconsEntries

                    MpvqcLicensesListItem {}
                }
            }
        }
    }
}
