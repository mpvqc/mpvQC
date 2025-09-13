/*
 * Copyright (C) 2024 mpvQC developers
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Layouts
import QtQuick.Controls.Material

import "../settings"
import "../shared"

Item {
    id: root

    required property MpvqcFooterController controller

    property int selectedCommentIndex: 0
    property int totalCommentCount: 0

    readonly property alias rowSelectionLabelText: _rowSelectionLabelText
    readonly property alias percentLabelText: _videoPercentLabel
    readonly property alias videoTimeLabelText: _videoTimeLabel
    readonly property alias loader: _contextMenuLoader

    height: 25
    visible: !controller.isApplicationFullscreen

    readonly property int bottomMargin: controller.isApplicationMazimized ? 2 : 0
    readonly property int rightMargin: controller.isApplicationMazimized ? 0 : 1

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
        id: _row
        spacing: 0
        anchors {
            top: _separator.top
            left: root.left
            right: root.right
            bottom: root.bottom
        }

        Label {
            id: _rowSelectionLabelText
            text: (root.selectedCommentIndex + 1) + "/" + root.totalCommentCount
            visible: root.totalCommentCount > 0
            verticalAlignment: Text.AlignVCenter
            Layout.bottomMargin: root.bottomMargin
            Layout.leftMargin: 3
        }

        Item {
            Layout.fillWidth: true
        }

        Label {
            id: _videoPercentLabel
            text: `${root.controller.playerPercentPosition.toFixed(0)}%`
            visible: root.controller.playerVideoLoaded && root.controller.isStatusbarDisplayPercentage
            horizontalAlignment: Text.AlignRight
            verticalAlignment: Text.AlignVCenter
            Layout.bottomMargin: root.bottomMargin
        }

        Label {
            id: _videoTimeLabel
            text: root.controller.determineTimeLabelText()
            visible: root.controller.playerVideoLoaded && !root.controller.isTimeFormatEmpty
            horizontalAlignment: Text.AlignRight
            verticalAlignment: Text.AlignVCenter
            Layout.preferredWidth: root.controller.videoTimeLabelWidth
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
                icon.source: "qrc:/data/icons/expand_more_black_24dp.svg"
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
            x: mMirrored ? _toolButtonContainer.x : _toolButtonContainer.x + _toolButtonContainer.width - width
            y: -height
            transformOrigin: mMirrored ? Popup.BottomLeft : Popup.BottomRight
            modal: true
            dim: false

            MenuItem {
                text: qsTranslate("MainWindow", "Default format")
                checked: root.controller.isTimeFormatCurrentTotalTime
                autoExclusive: true
                checkable: true

                onTriggered: root.controller.setTimeFormat(MpvqcSettings.TimeFormat.CURRENT_TOTAL_TIME)
            }

            MenuItem {
                text: qsTranslate("MainWindow", "Current time")
                checked: root.controller.isTimeFormatCurrentTime
                autoExclusive: true
                checkable: true

                onTriggered: root.controller.setTimeFormat(MpvqcSettings.TimeFormat.CURRENT_TIME)
            }

            MenuItem {
                text: qsTranslate("MainWindow", "Remaining time")
                checked: root.controller.isTimeFormatRemainingTime
                autoExclusive: true
                checkable: true

                onTriggered: root.controller.setTimeFormat(MpvqcSettings.TimeFormat.REMAINING_TIME)
            }

            MenuItem {
                text: qsTranslate("MainWindow", "Hide time")
                checked: root.controller.isTimeFormatEmpty
                autoExclusive: true
                checkable: true

                onTriggered: root.controller.setTimeFormat(MpvqcSettings.TimeFormat.EMPTY)
            }

            MenuSeparator {}

            Action {
                text: qsTranslate("MainWindow", "Progress in percent")
                checked: root.controller.isStatusbarDisplayPercentage
                checkable: true

                onTriggered: root.controller.toggleStatusBarPercentage()
            }
        }
    }
}
