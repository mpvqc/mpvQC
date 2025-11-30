// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import "../../styles/MpvqcStyle"

Item {
    id: root

    required property var viewModel
    required property int buttonHeight
    required property int largeSpacing

    readonly property bool isWindows: Qt.platform.os === "windows"

    readonly property int groupSpacing: 12
    readonly property int iconSize: 22
    readonly property int buttonPadding: 6
    readonly property int buttonSize: root.buttonHeight - root.buttonPadding
    readonly property int cornerRadius: 8
    readonly property int itemSpacing: 2

    height: root.buttonHeight
    width: _row.width

    component ToolBarButton: ToolButton {
        id: _toolBarButton

        required property url iconSource
        required property string toolTipText

        width: root.buttonSize
        height: root.buttonSize
        focusPolicy: Qt.NoFocus
        icon.source: _toolBarButton.iconSource
        icon.width: root.iconSize
        icon.height: root.iconSize

        background: Rectangle {
            radius: root.cornerRadius
            color: _toolBarButton.hovered ? _toolBarButton.Material.rippleColor : "transparent"
        }

        ToolTip {
            y: implicitHeight + 16
            popupType: root.isWindows ? Popup.Window : Popup.Item

            text: _toolBarButton.toolTipText
            visible: _toolBarButton.hovered
            delay: 1000
            timeout: 2000
        }
    }

    Row {
        id: _row

        spacing: root.itemSpacing
        anchors.verticalCenter: parent.verticalCenter

        ToolBarButton {
            iconSource: "qrc:/data/icons/edit_note_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            //: Tooltip for 'Add Comment', %1 will be the shortcut button identifier
            toolTipText: qsTranslate("ToolBar", "Add Comment (%1)").arg("E")

            onPressed: root.viewModel.requestNewCommentMenu()
        }

        Item {
            width: root.largeSpacing
            height: root.buttonSize
        }

        Row {
            LayoutMirroring.enabled: false

            spacing: root.itemSpacing

            ToolBarButton {
                iconSource: "qrc:/data/icons/first_page_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                //: Tooltip for 'Frame Step Backward', %1 will be the default shortcut button identifier
                toolTipText: qsTranslate("ToolBar", "Frame Step Backward (%1)").arg(" , ")

                onPressed: {
                    console.log("Frame Step Backward pressed");
                }
            }

            ToolBarButton {
                iconSource: "qrc:/data/icons/last_page_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                //: Tooltip for 'Frame Step Forward', %1 will be the default shortcut button identifier
                toolTipText: qsTranslate("ToolBar", "Frame Step Forward (%1)").arg(" . ")

                onPressed: {
                    console.log("Frame Step Forward pressed");
                }
            }
        }

        Item {
            width: root.groupSpacing
            height: root.buttonSize
        }

        ToolBarButton {
            iconSource: "qrc:/data/icons/subtitles_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            //: Tooltip for 'Cycle Subtitle Track', %1 will be the default shortcut button identifier
            toolTipText: qsTranslate("ToolBar", "Cycle Subtitle Track (%1)").arg("J")

            onPressed: {
                console.log("Cycle Subtitle Track pressed");
            }
        }

        ToolBarButton {
            iconSource: "qrc:/data/icons/music_history_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            //: Tooltip for 'Cycle Audio Track', %1 will be the default shortcut button identifier
            toolTipText: qsTranslate("ToolBar", "Cycle Audio Track (%1)").arg("#")

            onPressed: {
                console.log("Cycle Audio Track pressed");
            }
        }
    }
}
