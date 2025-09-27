// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import pyobjects

import "../shared"
import "../models"

MpvqcDialog {
    id: root

    readonly property MpvqcAboutDialogControllerPyObject controller: MpvqcAboutDialogControllerPyObject {}

    readonly property string applicationName: Qt.application.name
    readonly property string applicationVersion: `${Qt.application.version} - >>>commit-id<<<`

    //: This text is part of the software license description. This is the name of the license being used.
    readonly property string licenseDescription: qsTranslate("AboutDialog", "GNU General Public License, version 3 or later")
    //: This text is part of the software license description
    readonly property string licenseText1: qsTranslate("AboutDialog", "This program comes with absolutely no warranty.")
    //: This text is part of the software license description. Argument %1 will be the link to the license
    readonly property string licenseText2: qsTranslate("AboutDialog", "See the %1 for details.").arg(root.licenseWebsite)

    readonly property QtObject urls: QtObject {
        readonly property url app: "https://mpvqc.github.io"
        readonly property url license: "https://www.gnu.org/licenses/gpl-3.0.html"
    }

    readonly property string applicationWebsite: `<a href="${urls.app}">${urls.app}</a>`
    readonly property string licenseWebsite: `<a href="${urls.license}">${licenseDescription}</a>`

    readonly property int rowSpacing: 10

    contentHeight: Math.min(720, MpvqcWindowProperties.appHeight * 0.65)

    contentItem: ScrollView {
        readonly property bool isVerticalScollBarShown: contentHeight > root.contentHeight

        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
        ScrollBar.vertical.policy: isVerticalScollBarShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff

        contentWidth: isVerticalScollBarShown ? root.contentWidth - 20 : root.contentWidth

        ColumnLayout {
            anchors.fill: parent
            anchors.rightMargin: root.isMirrored ? 20 : 0

            Image {
                source: "qrc:/data/icon.svg"
                sourceSize.width: 160
                sourceSize.height: 160
                asynchronous: true

                Layout.alignment: Qt.AlignHCenter
            }

            MpvqcHeader {
                text: root.applicationName
                font.pointSize: 14

                Layout.alignment: Qt.AlignHCenter
            }

            Label {
                text: root.applicationVersion
                font.weight: Font.DemiBold

                Layout.alignment: Qt.AlignHCenter
            }

            Label {
                text: root.applicationWebsite

                Layout.alignment: Qt.AlignHCenter

                onLinkActivated: link => root.controller.openLink(link)

                MouseArea {
                    anchors.fill: parent
                    acceptedButtons: Qt.NoButton
                    cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
                }
            }

            Label {
                //: This text is part of the software license description
                text: qsTranslate("AboutDialog", "Copyright © mpvQC Developers")

                Layout.alignment: Qt.AlignHCenter
            }

            Label {
                text: root.licenseText1 + "<br>" + root.licenseText2

                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.WordWrap

                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter

                onLinkActivated: link => root.controller.openLink(link)

                MouseArea {
                    anchors.fill: parent
                    acceptedButtons: Qt.NoButton
                    cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
                }

                MpvqcTooltip {
                    y: -parent.height + 35
                    visible: (parent as Label).hoveredLink
                    text: root.urls.license
                }
            }

            MpvqcHeader {
                text: qsTranslate("AboutDialog", "Made by")

                Layout.alignment: Qt.AlignHCenter
            }

            Repeater {
                model: MpvqcCreditsModel {}

                MpvqcTwoColumnRow {
                    required property string name
                    required property string contribution

                    leftText: name
                    rightText: contribution

                    Layout.fillWidth: true
                }
            }

            MpvqcSpacer {}

            Repeater {
                model: MpvqcLanguageModel {}

                MpvqcTwoColumnRow {
                    required property string translator
                    required property string language

                    leftText: translator
                    rightText: qsTranslate("Languages", language)

                    Layout.fillWidth: true
                }
            }

            MpvqcHeader {
                text: qsTranslate("AboutDialog", "Powered by")

                Layout.alignment: Qt.AlignHCenter
            }

            MpvqcTwoColumnDependencyRow {
                dependencyName: "libmpv"
                dependencyUrl: "https://mpv.io/"
                dependencyLicence: "GPL-2.0+"
                dependencyVersion: root.controller.mpvVersion

                Layout.fillWidth: true
            }

            MpvqcTwoColumnDependencyRow {
                dependencyName: "ffmpeg"
                dependencyUrl: "https://ffmpeg.org/"
                dependencyLicence: "GPL-2.0+"
                dependencyVersion: root.controller.ffmpegVersion

                Layout.fillWidth: true
            }

            MpvqcSpacer {}

            Repeater {
                model: MpvqcLibraryModel {}

                MpvqcTwoColumnDependencyRow {
                    required property string licence
                    required property string name
                    required property string os
                    required property string url
                    required property string version

                    dependencyName: name
                    dependencyUrl: url
                    dependencyLicence: licence
                    dependencyVersion: version
                    visible: os.indexOf(Qt.platform.os) >= 0

                    Layout.fillWidth: true
                }
            }

            MpvqcSpacer {}

            MpvqcTwoColumnDependencyRow {
                dependencyName: "Noto Sans"
                dependencyUrl: "https://fonts.google.com/noto/specimen/Noto+Sans"
                dependencyLicence: "OFL"

                Layout.fillWidth: true
            }

            MpvqcTwoColumnDependencyRow {
                dependencyName: "material-design-icons"
                dependencyUrl: "https://github.com/google/material-design-icons"
                dependencyLicence: "Apache-2.0"

                Layout.fillWidth: true
            }
        }
    }

    component MpvqcSpacer: Item {
        Layout.preferredHeight: 6
        Layout.fillWidth: true
    }

    component MpvqcTwoColumnRow: Row {
        property string leftText: ""
        property string rightText: ""

        height: Math.max(leftLabel.implicitHeight, rightLabel.implicitHeight)
        visible: leftText
        spacing: root.rowSpacing

        Label {
            id: leftLabel
            text: parent.leftText
            horizontalAlignment: Text.AlignRight
            width: parent.width / 2
        }

        Label {
            id: rightLabel
            text: parent.rightText
            font.italic: true
            horizontalAlignment: Text.AlignLeft
            width: parent.width / 2
        }
    }

    component MpvqcTwoColumnDependencyRow: Row {
        id: _row

        required property string dependencyName

        property string dependencyLicence: ""
        property string dependencyUrl: ""
        property string dependencyVersion: ""

        spacing: root.rowSpacing
        height: Math.max(leftLabel.implicitHeight, rightLabel.implicitHeight)

        Label {
            id: leftLabel

            text: `<a href="${_row.dependencyUrl}">${_row.dependencyName} ${_row.dependencyVersion}</a>`
            elide: LayoutMirroring.enabled ? Text.ElideRight : Text.ElideLeft
            horizontalAlignment: Text.AlignRight
            width: _row.width / 2

            onLinkActivated: link => root.controller.openLink(link)

            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.NoButton
                cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
            }

            MpvqcTooltip {
                y: -parent.height - 15
                z: 10
                visible: leftLabel.hoveredLink
                text: _row.dependencyUrl
            }
        }

        Label {
            id: rightLabel

            text: parent.dependencyLicence
            font.italic: true
            horizontalAlignment: Text.AlignLeft
            width: parent.width / 2
        }
    }
}
