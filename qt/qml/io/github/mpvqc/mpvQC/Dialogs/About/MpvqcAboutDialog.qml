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

    contentHeight: MpvqcConstants.mediumDialogContentHeight
    standardButtons: Dialog.Close

    contentItem: ColumnLayout {
        spacing: MpvqcConstants.dialogSectionSpacing

        TabBar {
            id: _navigation

            implicitWidth: 0
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
            Layout.topMargin: MpvqcConstants.dialogContentTopMargin

            MpvqcPillTabButton {
                objectName: "aboutNavigationButton"

                //: Label of the button displaying general application information
                text: qsTranslate("AboutDialog", "About")
            }

            MpvqcPillTabButton {
                objectName: "creditsNavigationButton"

                //: Label of the button displaying contributors and translators
                text: qsTranslate("AboutDialog", "Credits")
            }

            MpvqcPillTabButton {
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
