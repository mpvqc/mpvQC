// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Layouts
import QtQuick.Controls.Material

import pyobjects

import "../../utility"

Item {
    id: root

    required property int selectedCommentIndex
    required property int totalCommentCount

    readonly property MpvqcFooterViewModel viewModel: MpvqcFooterViewModel {}

    readonly property int bottomMargin: MpvqcWindowUtility.isMaximized ? 2 : 0
    readonly property int rightMargin: MpvqcWindowUtility.isMaximized ? 0 : 1

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
            objectName: "commentCountLabel"

            text: `${root.selectedCommentIndex + 1}/${root.totalCommentCount}`
            visible: root.totalCommentCount > 0
            verticalAlignment: Text.AlignVCenter
            Layout.bottomMargin: root.bottomMargin
            Layout.leftMargin: 3
        }

        Item {
            Layout.fillWidth: true
        }

        Label {
            objectName: "percentLabel"

            text: root.viewModel.percentText
            visible: root.viewModel.isPercentVisible
            horizontalAlignment: Text.AlignRight
            verticalAlignment: Text.AlignVCenter
            Layout.bottomMargin: root.bottomMargin
        }

        Label {
            objectName: "timeLabel"

            text: root.viewModel.timeText
            visible: root.viewModel.isTimeVisible
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
                objectName: "contextMenuButton"

                icon.source: MpvqcIcons.arrowDropDown
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
                (item as MpvqcFooterContextMenu).open();
            } else {
                active = true;
            }
        }

        active: false
        asynchronous: true

        onLoaded: (item as MpvqcFooterContextMenu).open()

        sourceComponent: MpvqcFooterContextMenu {
            x: isMirrored ? _toolButtonContainer.x : _toolButtonContainer.x + _toolButtonContainer.width - width
            y: -height
            transformOrigin: isMirrored ? Popup.BottomLeft : Popup.BottomRight

            isDefaultFormatChecked: root.viewModel.timeFormat === MpvqcTimeFormat.TimeFormat.CURRENT_TOTAL_TIME
            isCurrentTimeChecked: root.viewModel.timeFormat === MpvqcTimeFormat.TimeFormat.CURRENT_TIME
            isRemainingTimeChecked: root.viewModel.timeFormat === MpvqcTimeFormat.TimeFormat.REMAINING_TIME
            isHideTimeChecked: root.viewModel.timeFormat === MpvqcTimeFormat.TimeFormat.EMPTY
            isPercentChecked: root.viewModel.statusbarPercentage

            onDefaultFormatPicked: root.viewModel.timeFormat = MpvqcTimeFormat.TimeFormat.CURRENT_TOTAL_TIME
            onCurrentTimePicked: root.viewModel.timeFormat = MpvqcTimeFormat.TimeFormat.CURRENT_TIME
            onRemainingTimePicked: root.viewModel.timeFormat = MpvqcTimeFormat.TimeFormat.REMAINING_TIME
            onHideTimePicked: root.viewModel.timeFormat = MpvqcTimeFormat.TimeFormat.EMPTY
            onPercentToggled: root.viewModel.toggleStatusbarPercentage()
        }
    }

    MpvqcFooterContextMenuClickGuard {
        menu: _contextMenuLoader.item
    }
}
