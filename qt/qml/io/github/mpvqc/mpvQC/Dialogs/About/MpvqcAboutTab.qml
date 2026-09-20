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

MpvqcAboutScrollView {
    id: root

    required property MpvqcAboutDialogViewModel viewModel

    readonly property url appUrl: "https://mpvqc.github.io"
    readonly property url licenseUrl: "https://www.gnu.org/licenses/gpl-3.0.html"

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

            width: root.availableWidth
            spacing: MpvqcConstants.dialogSectionSpacing

            MpvqcSectionCard {
                Layout.fillWidth: true

                Image {
                    source: "qrc:/data/icon.svg"
                    sourceSize.width: 96
                    sourceSize.height: 96
                    asynchronous: true

                    Layout.preferredWidth: 96
                    Layout.preferredHeight: 96
                    Layout.alignment: Qt.AlignHCenter
                }

                MpvqcHeader {
                    text: root.viewModel.applicationName
                    font.pointSize: 14

                    Layout.alignment: Qt.AlignHCenter
                    Layout.topMargin: 8
                }

                Item {
                    id: _versionRow

                    implicitHeight: Math.max(_versionLabel.implicitHeight, _copyVersionButton.implicitHeight)

                    Layout.fillWidth: true

                    Label {
                        id: _versionLabel
                        objectName: "applicationVersion"

                        anchors.centerIn: parent
                        width: Math.min(implicitWidth, Math.max(0, _versionRow.width - 2 * (_copyVersionButton.width + 4)))
                        text: root.viewModel.applicationVersion
                        color: MpvqcAppearance.palette.hint
                        wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                        horizontalAlignment: Text.AlignHCenter
                    }

                    ToolButton {
                        id: _copyVersionButton
                        objectName: "copyVersionButton"

                        anchors.left: _versionLabel.right
                        anchors.leftMargin: 4
                        anchors.verticalCenter: _versionLabel.verticalCenter
                        text: qsTranslate("AboutDialog", "Copy version info to clipboard")
                        display: AbstractButton.IconOnly
                        icon.source: MpvqcIcons.contentCopy
                        icon.width: 18
                        icon.height: 18

                        ToolTip.delay: MpvqcConstants.tooltipDelay
                        ToolTip.text: text
                        ToolTip.visible: hovered || visualFocus

                        onClicked: {
                            root.viewModel.copyVersionInfoToClipboard();
                            icon.source = MpvqcIcons.check;
                        }
                    }
                }

                Label {
                    text: qsTranslate("AboutDialog", "Powered by Python %1").arg(root.viewModel.pythonVersion)
                    color: MpvqcAppearance.palette.hint
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignHCenter

                    Layout.fillWidth: true
                }

                Label {
                    //: This text is part of the software license description
                    text: qsTranslate("AboutDialog", "Copyright © mpvQC Developers")
                    color: MpvqcAppearance.palette.hint
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignHCenter

                    Layout.fillWidth: true
                }
            }

            MpvqcSectionCard {
                Layout.fillWidth: true

                MpvqcAboutListItem {
                    objectName: "websiteRow"

                    text: root.appUrl
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
            }
        }
    }
}
