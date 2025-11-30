// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import "../../styles/MpvqcStyle"

import pyobjects

Item {
    id: root

    required property MpvqcToolBarViewModel viewModel: MpvqcToolBarViewModel {}

    readonly property bool isWindows: Qt.platform.os === "windows"

    readonly property int groupSpacing: 12
    readonly property int iconSize: 22
    readonly property int buttonPadding: 6
    readonly property int buttonSize: height - root.buttonPadding
    readonly property int cornerRadius: 8
    readonly property int itemSpacing: 2

    readonly property bool anyFrameStepButtonVisible: root.viewModel.frameStepBackwardVisible || root.viewModel.frameStepForwardVisible
    readonly property bool anyCycleButtonVisible: root.viewModel.cycleSubtitleTrackVisible || root.viewModel.cycleAudioTrackVisible
    readonly property bool anyButtonVisible: anyFrameStepButtonVisible || anyCycleButtonVisible

    width: _row.width

    component ToolBarButton: ToolButton {
        id: _toolBarButton

        required property url iconSource
        required property string toolTipText

        property bool pressedDuringHover: false

        width: root.buttonSize
        height: root.buttonSize
        focusPolicy: Qt.NoFocus
        icon.source: _toolBarButton.iconSource
        icon.width: root.iconSize
        icon.height: root.iconSize

        onHoveredChanged: {
            if (!hovered) {
                pressedDuringHover = false;
            }
        }

        onPressed: pressedDuringHover = true

        background: Rectangle {
            radius: root.cornerRadius
            color: _toolBarButton.hovered ? _toolBarButton.Material.rippleColor : "transparent"
        }

        ToolTip {
            y: implicitHeight + 16
            popupType: root.isWindows ? Popup.Window : Popup.Item

            text: _toolBarButton.toolTipText
            visible: _toolBarButton.hovered && !_toolBarButton.pressedDuringHover
            delay: 700
            timeout: 1500
        }
    }

    Row {
        id: _row

        spacing: root.itemSpacing
        anchors.verticalCenter: parent.verticalCenter

        Row {
            visible: root.anyFrameStepButtonVisible
            LayoutMirroring.enabled: false

            spacing: root.itemSpacing

            ToolBarButton {
                visible: root.viewModel.frameStepBackwardVisible
                iconSource: "qrc:/data/icons/first_page_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                //: Tooltip for 'Frame Step Backward', %1 will be the default shortcut button identifier
                toolTipText: qsTranslate("ToolBar", "Frame Step Backward (%1)").arg(" , ")

                onPressed: root.viewModel.requestFrameStepBackward()
            }

            ToolBarButton {
                visible: root.viewModel.frameStepForwardVisible
                iconSource: "qrc:/data/icons/last_page_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                //: Tooltip for 'Frame Step Forward', %1 will be the default shortcut button identifier
                toolTipText: qsTranslate("ToolBar", "Frame Step Forward (%1)").arg(" . ")

                onPressed: root.viewModel.requestFrameStepForward()
            }
        }

        Item {
            visible: root.anyCycleButtonVisible
            width: root.groupSpacing
            height: root.buttonSize
        }

        ToolBarButton {
            visible: root.viewModel.cycleSubtitleTrackVisible
            iconSource: "qrc:/data/icons/subtitles_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            //: Tooltip for 'Cycle Subtitle Track', %1 will be the default shortcut button identifier
            toolTipText: qsTranslate("ToolBar", "Cycle Subtitle Track (%1)").arg("J")

            onPressed: root.viewModel.requestCycleSubtitleTrack()
        }

        ToolBarButton {
            visible: root.viewModel.cycleAudioTrackVisible
            iconSource: "qrc:/data/icons/music_note_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            //: Tooltip for 'Cycle Audio Track', %1 will be the default shortcut button identifier
            toolTipText: qsTranslate("ToolBar", "Cycle Audio Track (%1)").arg("#")

            onPressed: root.viewModel.requestCycleAudioTrack()
        }
    }
}
