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

MpvqcDialog {
    id: root
    objectName: "aboutDialog"

    readonly property MpvqcAboutDialogViewModel viewModel: MpvqcAboutDialogViewModel {}

    readonly property alias currentIndex: _pages.currentIndex

    component MpvqcNavigationButton: TabButton {
        id: button

        implicitHeight: 48
        padding: 12

        contentItem: Label {
            text: button.text
            font: button.font
            color: button.checked ? MpvqcAppearance.palette.accent : MpvqcAppearance.palette.foreground
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        background: Rectangle {
            radius: height / 2
            color: button.checked ? Qt.alpha(MpvqcAppearance.palette.accent, 0.15) : "transparent"
            border.width: button.visualFocus ? 2 : 0
            border.color: MpvqcAppearance.palette.accent

            Rectangle {
                anchors.fill: parent
                radius: parent.radius
                color: Qt.alpha(MpvqcAppearance.palette.foreground, button.down ? 0.12 : button.hovered ? 0.07 : 0)
            }
        }
    }

    contentHeight: MpvqcConstants.mediumDialogContentHeight + 40
    standardButtons: Dialog.Close

    contentItem: ColumnLayout {
        spacing: 20

        TabBar {
            id: _navigation

            spacing: 8
            background: null
            contentItem: ListView {
                model: _navigation.contentModel
                currentIndex: _navigation.currentIndex
                orientation: ListView.Horizontal
                spacing: _navigation.spacing
                interactive: false
                keyNavigationEnabled: true
            }

            Layout.fillWidth: true

            MpvqcNavigationButton {
                objectName: "aboutNavigationButton"

                //: Label of the button displaying general application information
                text: qsTranslate("AboutDialog", "About")
            }

            MpvqcNavigationButton {
                objectName: "creditsNavigationButton"

                //: Label of the button displaying contributors and translators
                text: qsTranslate("AboutDialog", "Credits")
            }

            MpvqcNavigationButton {
                objectName: "licensesNavigationButton"

                //: Label of the button displaying third-party dependencies and their licenses
                text: qsTranslate("AboutDialog", "Licenses")
            }
        }

        StackLayout {
            id: _pages

            currentIndex: _navigation.currentIndex
            clip: true

            Layout.fillWidth: true
            Layout.fillHeight: true

            MpvqcAboutTab {
                objectName: "aboutPage"

                viewModel: root.viewModel
            }

            MpvqcCreditsTab {
                objectName: "creditsPage"
            }

            MpvqcLicensesTab {
                objectName: "licensesPage"

                viewModel: root.viewModel
            }
        }
    }
}
