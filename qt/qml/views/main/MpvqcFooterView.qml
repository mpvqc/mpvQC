// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Layouts
import QtQuick.Controls.Material

import pyobjects

import "../../components"
import "../../utility"

Item {
    id: root

    required property MpvqcFooterViewModel viewModel

    readonly property int bottomMargin: MpvqcWindowProperties.isMaximized ? 2 : 0
    readonly property int rightMargin: MpvqcWindowProperties.isMaximized ? 0 : 1

    height: 25

    MenuSeparator {
        id: _separator

        topPadding: 1
        bottomPadding: 1
        anchors {
            top: root.top
            left: root.left
            right: root.right
        }
    }

    RowLayout {
        spacing: 0
        anchors {
            top: _separator.top
            left: root.left
            right: root.right
            bottom: root.bottom
        }

        Label {
            text: root.viewModel.commentCountText
            visible: root.viewModel.isCommentCountVisible
            verticalAlignment: Text.AlignVCenter
            Layout.bottomMargin: root.bottomMargin
            Layout.leftMargin: 3
        }

        Item {
            Layout.fillWidth: true
        }

        Label {
            text: root.viewModel.videoPercentText
            visible: root.viewModel.isVideoPercentVisible
            horizontalAlignment: Text.AlignRight
            verticalAlignment: Text.AlignVCenter
            Layout.bottomMargin: root.bottomMargin
        }

        Label {
            text: root.viewModel.timeText
            visible: root.viewModel.isTimeTextVisible
            horizontalAlignment: Text.AlignRight
            verticalAlignment: Text.AlignVCenter
            Layout.preferredWidth: root.viewModel.timeWidth
            Layout.bottomMargin: root.bottomMargin
            Layout.leftMargin: 15
        }

        Item {
            id: _toolButtonContainer

            Layout.preferredHeight: 22
            Layout.preferredWidth: 22
            Layout.leftMargin: _toolButton.padding
            Layout.rightMargin: root.rightMargin

            ToolButton {
                id: _toolButton

                icon.source: "qrc:/data/icons/arrow_drop_down_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                focusPolicy: Qt.NoFocus
                padding: 2
                height: parent.height
                width: parent.width + 1
                onPressed: _contextMenuLoader.openContextMenu()
            }
        }
    }

    Loader {
        id: _contextMenuLoader

        function openContextMenu(): void {
            if (active) {
                item.open(); // qmllint disable
            } else {
                active = true;
            }
        }

        active: false
        asynchronous: true
        visible: active

        onLoaded: item.open() // qmllint disable

        sourceComponent: MpvqcMenu {
            x: isMirrored ? _toolButtonContainer.x : _toolButtonContainer.x + _toolButtonContainer.width - width
            y: -height
            transformOrigin: isMirrored ? Popup.BottomLeft : Popup.BottomRight
            modal: true
            dim: false

            MenuItem {
                text: qsTranslate("MainWindow", "Default format")
                checked: root.viewModel.timeFormat === MpvqcFooterViewModel.TimeFormat.CURRENT_TOTAL_TIME
                autoExclusive: true
                checkable: true

                onTriggered: root.viewModel.timeFormat = MpvqcFooterViewModel.TimeFormat.CURRENT_TOTAL_TIME
            }

            MenuItem {
                text: qsTranslate("MainWindow", "Current time")
                checked: root.viewModel.timeFormat === MpvqcFooterViewModel.TimeFormat.CURRENT_TIME
                autoExclusive: true
                checkable: true

                onTriggered: root.viewModel.timeFormat = MpvqcFooterViewModel.TimeFormat.CURRENT_TIME
            }

            MenuItem {
                text: qsTranslate("MainWindow", "Remaining time")
                checked: root.viewModel.timeFormat === MpvqcFooterViewModel.TimeFormat.REMAINING_TIME
                autoExclusive: true
                checkable: true

                onTriggered: root.viewModel.timeFormat = MpvqcFooterViewModel.TimeFormat.REMAINING_TIME
            }

            MenuItem {
                text: qsTranslate("MainWindow", "Hide time")
                checked: root.viewModel.timeFormat === MpvqcFooterViewModel.TimeFormat.EMPTY
                autoExclusive: true
                checkable: true

                onTriggered: root.viewModel.timeFormat = MpvqcFooterViewModel.TimeFormat.EMPTY
            }

            MenuSeparator {}

            Action {
                text: qsTranslate("MainWindow", "Progress in percent")
                checked: root.viewModel.isVideoPercentVisible
                checkable: true

                onTriggered: root.viewModel.toggleVideoPercentDisplay()
            }
        }
    }
}
