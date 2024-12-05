/*
mpvQC

Copyright (C) 2024 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import "../shared"

Item {
    id: root

    required property bool isApplicationMazimized

    required property int selectedCommentIndex
    required property int totalCommentCount

    required property real playerPercentPosition
    required property int playerDuration
    required property bool playerVideoLoaded
    required property int playerTimePosition
    required property int playerTimeRemaining

    required property bool isStatusbarDisplayPercentage

    required property bool isTimeFormatCurrentTotalTime
    required property bool isTimeFormatCurrentTime
    required property bool isTimeFormatRemainingTime
    required property bool isTimeFormatEmpty

    required property var formatTimeFunc

    required property int videoTimeLabelWidth

    readonly property int bottomMargin: root.isApplicationMazimized ? 2 : 0
    readonly property int rightMargin: root.isApplicationMazimized ? 0 : 1

    readonly property Label rowSelectionLabel: _rowSelectionLabelText // for tests
    readonly property Label percentLabel: _videoPercentLabel // for tests
    readonly property Label videoTimeLabel: _videoTimeLabel // for tests

    signal currentTotalTimeSelected
    signal currentTimeSelected
    signal remainingTimeSelected
    signal emptyTimeSelected
    signal statusBarPercentageToggled

    function determineTimeLabelText(): string {
        if (root.isTimeFormatCurrentTotalTime) {
            const current = root.formatTimeFunc(root.playerTimePosition); // qmllint disable
            const total = root.formatTimeFunc(root.playerDuration); // qmllint disable
            return `${current}/${total}`;
        }
        if (root.isTimeFormatCurrentTime) {
            return root.formatTimeFunc(root.playerTimePosition);  // qmllint disable
        }
        if (root.isTimeFormatRemainingTime) {
            const remaining = root.formatTimeFunc(root.playerTimeRemaining);  // qmllint disable
            return `-${remaining}`;
        }
        return "";
    }

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
            id: _rowSelectionLabelText

            text: (root.selectedCommentIndex + 1) + '/' + root.totalCommentCount
            visible: root.totalCommentCount

            verticalAlignment: Text.AlignVCenter

            Layout.bottomMargin: root.bottomMargin
            Layout.leftMargin: 3
        }

        Item {
            Layout.fillWidth: true
        }

        Label {
            id: _videoPercentLabel

            text: `${root.playerPercentPosition.toFixed(0)}%`
            visible: root.playerVideoLoaded && root.isStatusbarDisplayPercentage

            horizontalAlignment: Text.AlignRight
            verticalAlignment: Text.AlignVCenter

            Layout.bottomMargin: root.bottomMargin
        }

        Label {
            id: _videoTimeLabel

            text: root.determineTimeLabelText()
            visible: root.playerVideoLoaded && !root.isTimeFormatEmpty

            horizontalAlignment: Text.AlignRight
            verticalAlignment: Text.AlignVCenter

            Layout.preferredWidth: root.videoTimeLabelWidth
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

                onPressed: {
                    _contextMenuLoader.openContextMenu();
                }
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
                checked: root.isTimeFormatCurrentTotalTime
                autoExclusive: true
                checkable: true

                onTriggered: root.currentTotalTimeSelected()
            }

            MenuItem {
                text: qsTranslate("MainWindow", "Current time")
                checked: root.isTimeFormatCurrentTime
                autoExclusive: true
                checkable: true

                onTriggered: root.currentTimeSelected()
            }

            MenuItem {
                text: qsTranslate("MainWindow", "Remaining time")
                checked: root.isTimeFormatRemainingTime
                autoExclusive: true
                checkable: true

                onTriggered: root.remainingTimeSelected()
            }

            MenuItem {
                text: qsTranslate("MainWindow", "Hide time")
                checked: root.isTimeFormatEmpty
                autoExclusive: true
                checkable: true

                onTriggered: root.emptyTimeSelected()
            }

            MenuSeparator {}

            Action {
                text: qsTranslate("MainWindow", "Progress in percent")
                checked: root.isStatusbarDisplayPercentage
                checkable: true

                onTriggered: root.statusBarPercentageToggled()
            }
        }
    }
}
