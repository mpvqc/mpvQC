// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material as M
import QtQuick.Controls.Material.impl as MImpl
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

MpvqcDialog {
    id: root
    objectName: "aboutDialog"

    readonly property alias currentIndex: _pages.currentIndex

    readonly property MpvqcAboutDialogViewModel viewModel: MpvqcAboutDialogViewModel {}

    function showPage(index: int): void {
        if (index === _pages.currentIndex) {
            return;
        }
        if (_pageFade.running) {
            _pageFade.complete();
        }
        _pages.currentIndex = index;
        _pageFade.restart();
    }

    contentHeight: MpvqcConstants.mediumDialogContentHeight
    standardButtons: Dialog.Close

    contentItem: ColumnLayout {
        spacing: 40

        Row {
            id: _navigation

            spacing: 10

            Layout.alignment: Qt.AlignHCenter
            Layout.topMargin: 16

            MpvqcNavigationButton {
                id: _aboutButton
                objectName: "aboutNavigationButton"

                //: Label of the button displaying general application information
                text: qsTranslate("AboutDialog", "About")
                icon.source: MpvqcIcons.info
                highlighted: _pages.currentIndex === 0

                onClicked: root.showPage(0)
            }

            MpvqcNavigationButton {
                id: _creditsButton
                objectName: "creditsNavigationButton"

                //: Label of the button displaying contributors and translators
                text: qsTranslate("AboutDialog", "Credits")
                icon.source: MpvqcIcons.group
                highlighted: _pages.currentIndex === 1

                onClicked: root.showPage(1)
            }

            MpvqcNavigationButton {
                id: _licensesButton
                objectName: "licensesNavigationButton"

                //: Label of the button displaying third-party dependencies and their licenses
                text: qsTranslate("AboutDialog", "Licenses")
                icon.source: MpvqcIcons.deployedCode
                highlighted: _pages.currentIndex === 2

                onClicked: root.showPage(2)
            }
        }

        StackLayout {
            id: _pages

            readonly property list<Item> pages: [_aboutPage, _creditsPage, _licensesPage]

            clip: true

            Layout.fillWidth: true
            Layout.fillHeight: true

            MpvqcAboutTab {
                id: _aboutPage
                objectName: "aboutPage"

                viewModel: root.viewModel
            }

            MpvqcCreditsTab {
                id: _creditsPage
                objectName: "creditsPage"
            }

            MpvqcLicensesTab {
                id: _licensesPage
                objectName: "licensesPage"

                viewModel: root.viewModel
            }
        }
    }

    OpacityAnimator {
        id: _pageFade

        target: _pages.pages[_pages.currentIndex]
        from: 0
        to: 1
        duration: 100
        easing.type: Easing.OutCubic
    }

    component MpvqcNavigationButton: ToolButton {
        id: _button

        readonly property color _contentColor: !enabled ? MpvqcTheme.palette.hint : highlighted ? MpvqcTheme.palette.accent : MpvqcTheme.palette.foreground
        readonly property real _collapsedWidth: leftPadding + icon.width + rightPadding
        readonly property real _expandedWidth: _collapsedWidth + spacing + _navLabel.implicitWidth

        width: highlighted ? _expandedWidth : _collapsedWidth
        clip: true
        leftPadding: 16
        rightPadding: 16

        contentItem: Row {
            spacing: _button.spacing

            LayoutMirroring.enabled: _button.mirrored

            MpvqcIconLabel {
                icon.source: _button.icon.source
                icon.width: _button.icon.width
                icon.height: _button.icon.height
                iconColor: _button._contentColor

                anchors.verticalCenter: parent.verticalCenter
            }

            Label {
                id: _navLabel

                text: _button.text
                color: _button._contentColor
                visible: _button.highlighted || _widthAnimation.running

                anchors.verticalCenter: parent.verticalCenter
            }
        }

        background: MImpl.Ripple {
            implicitWidth: M.Material.touchTarget
            implicitHeight: M.Material.touchTarget

            x: (parent.width - width) / 2
            y: (parent.height - height) / 2
            width: parent.width
            height: Math.min(parent.height, 36)
            clip: true
            clipRadius: height / 2
            pressed: _button.pressed
            anchor: _button
            active: _button.enabled && (_button.down || _button.visualFocus || _button.hovered || _button.highlighted)
            color: Qt.alpha(_button._contentColor, 0.1)
        }

        Behavior on width {
            NumberAnimation {
                id: _widthAnimation

                duration: 150
            }
        }
    }
}
