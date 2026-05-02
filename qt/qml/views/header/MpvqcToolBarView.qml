// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import pyobjects
import "../../utility"

Item {
    id: root

    readonly property MpvqcToolBarViewModel viewModel: MpvqcToolBarViewModel {}

    readonly property int groupSpacing: 12
    readonly property int buttonPadding: 6
    readonly property int buttonSize: height - root.buttonPadding
    readonly property int itemSpacing: 2

    readonly property bool anyCycleButtonVisible: root.viewModel.cycleSubtitleTrackVisible || root.viewModel.cycleAudioTrackVisible
    readonly property bool anyButtonVisible: root.viewModel.frameStepVisible || anyCycleButtonVisible

    width: _row.width

    Row {
        id: _row

        spacing: root.itemSpacing
        anchors.verticalCenter: parent.verticalCenter

        Row {
            visible: root.viewModel.frameStepVisible
            LayoutMirroring.enabled: false

            spacing: root.itemSpacing

            MpvqcToolBarButton {
                size: root.buttonSize
                iconSource: MpvqcIcons.firstPage
                //: Tooltip for 'Frame Step Backward', %1 will be the default shortcut button identifier
                toolTipText: qsTranslate("ToolBar", "Frame Step Backward (%1)").arg(" , ")

                onPressed: root.viewModel.requestFrameStepBackward()
            }

            MpvqcToolBarButton {
                size: root.buttonSize
                iconSource: MpvqcIcons.lastPage
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

        MpvqcToolBarButton {
            size: root.buttonSize
            visible: root.viewModel.cycleSubtitleTrackVisible
            iconSource: MpvqcIcons.subtitles
            //: Tooltip for 'Cycle Subtitle Track', %1 will be the default shortcut button identifier
            toolTipText: qsTranslate("ToolBar", "Cycle Subtitle Track (%1)").arg("J")

            onPressed: root.viewModel.requestCycleSubtitleTrack()
        }

        MpvqcToolBarButton {
            size: root.buttonSize
            visible: root.viewModel.cycleAudioTrackVisible
            iconSource: MpvqcIcons.musicNote
            //: Tooltip for 'Cycle Audio Track', %1 will be the default shortcut button identifier
            toolTipText: qsTranslate("ToolBar", "Cycle Audio Track (%1)").arg("#")

            onPressed: root.viewModel.requestCycleAudioTrack()
        }
    }
}
