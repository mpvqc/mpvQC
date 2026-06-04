// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material as M
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

MpvqcDialog {
    id: root
    objectName: "appearanceDialog"

    readonly property MpvqcAppearanceDialogViewModel viewModel: MpvqcAppearanceDialogViewModel {}
    readonly property var mpvqcTheme: MpvqcTheme

    readonly property var dimensions: QtObject {
        readonly property int itemSize: 52
        readonly property int itemPadding: 8
        readonly property int borderSize: 5
        readonly property int colorGridRows: 4
        readonly property int themeSpacing: 8
    }

    readonly property var animations: QtObject {
        readonly property int highlightMoveDuration: 150
        readonly property int scaleAnimationDuration: 125
        readonly property real scalePressed: 1.1
        readonly property real scaleNormal: 1.0
        readonly property int appearDuration: 180
        readonly property int staggerInterval: 15
    }

    contentHeight: MpvqcConstants.smallDialogContentHeight

    title: qsTranslate("AppearanceDialog", "Appearance")
    standardButtons: Dialog.Ok | Dialog.Cancel

    component SelectionDelegate: ItemDelegate {
        id: delegateRoot

        required property int itemSize
        required property int borderSize
        required property color displayColor
        required property int index

        signal selected(int index)

        width: itemSize
        height: itemSize

        background: Rectangle {
            x: delegateRoot.borderSize
            y: delegateRoot.borderSize
            height: parent.height - 2 * delegateRoot.borderSize
            width: parent.width - 2 * delegateRoot.borderSize
            color: delegateRoot.displayColor
            radius: M.Material.LargeScale
        }

        Behavior on scale {
            NumberAnimation {
                duration: root.animations.scaleAnimationDuration
                easing.type: Easing.InOutQuad
            }
        }

        SequentialAnimation on opacity {
            PropertyAction {
                value: 0
            }
            PauseAnimation {
                duration: Math.max(0, delegateRoot.index * root.animations.staggerInterval)
            }
            NumberAnimation {
                to: 1
                duration: root.animations.appearDuration
                easing.type: Easing.OutCubic
            }
        }

        MouseArea {
            anchors.fill: parent

            onPressed: {
                delegateRoot.scale = root.animations.scalePressed;
                delegateRoot.selected(delegateRoot.index);
            }

            onReleased: delegateRoot.scale = root.animations.scaleNormal

            onCanceled: delegateRoot.scale = root.animations.scaleNormal
        }
    }

    component SelectionHighlight: Rectangle {
        id: _selectionHighlight

        required property int size
        required property color highlightColor
        required property int borderWidth
        required property color borderColor
        required property int moveDuration
        required property int appearIndex

        width: size
        height: size
        color: highlightColor
        radius: M.Material.SmallScale

        border {
            width: borderWidth
            color: borderColor
        }

        Behavior on color {
            ColorAnimation {
                duration: _selectionHighlight.moveDuration
            }
        }

        Behavior on border.width {
            NumberAnimation {
                duration: _selectionHighlight.moveDuration
            }
        }

        SequentialAnimation on opacity {
            PropertyAction {
                value: 0
            }
            PauseAnimation {
                duration: Math.max(0, _selectionHighlight.appearIndex * root.animations.staggerInterval)
            }
            NumberAnimation {
                to: 1
                duration: root.animations.appearDuration
                easing.type: Easing.OutCubic
            }
        }
    }

    contentItem: ScrollView {
        contentWidth: root.contentWidth

        ColumnLayout {
            anchors.fill: parent

            MpvqcHeader {
                text: qsTranslate("AppearanceDialog", "Theme")

                Layout.alignment: Qt.AlignLeft
            }

            ListView {
                id: _themeListView
                objectName: "themeListView"

                Layout.preferredHeight: root.dimensions.itemSize
                Layout.fillWidth: true

                model: MpvqcThemePreviewModel {}
                currentIndex: root.viewModel.themeIndex
                boundsBehavior: Flickable.StopAtBounds
                orientation: ListView.Horizontal
                clip: true
                spacing: root.dimensions.themeSpacing

                highlightMoveDuration: root.animations.highlightMoveDuration
                highlightMoveVelocity: -1

                highlight: SelectionHighlight {
                    size: root.dimensions.itemSize
                    highlightColor: root.mpvqcTheme.palette.accent
                    borderWidth: 0
                    borderColor: "transparent"
                    moveDuration: root.animations.highlightMoveDuration
                    appearIndex: _themeListView.currentIndex
                }

                delegate: SelectionDelegate {
                    required property string identifier
                    required property color preview

                    itemSize: root.dimensions.itemSize
                    borderSize: root.dimensions.borderSize
                    displayColor: preview

                    onSelected: root.viewModel.setTheme(identifier)
                }
            }

            MpvqcHeader {
                text: qsTranslate("AppearanceDialog", "Color")

                Layout.alignment: Qt.AlignLeft
            }

            GridView {
                id: _gridView
                objectName: "colorGridView"

                Layout.preferredHeight: {
                    const d = root.dimensions;
                    return (d.itemSize + d.itemPadding) * d.colorGridRows;
                }
                Layout.fillWidth: true

                model: MpvqcPrimaryColorModel {}

                currentIndex: root.viewModel.colorIndex
                boundsBehavior: Flickable.StopAtBounds
                clip: true

                cellWidth: root.dimensions.itemSize + root.dimensions.itemPadding
                cellHeight: root.dimensions.itemSize + root.dimensions.itemPadding

                highlightMoveDuration: root.animations.highlightMoveDuration

                highlight: SelectionHighlight {
                    size: root.dimensions.itemSize
                    highlightColor: root.mpvqcTheme.isDark ? root.mpvqcTheme.palette.foreground : root.mpvqcTheme.palette.background
                    borderWidth: root.mpvqcTheme.isDark ? 0 : 2
                    borderColor: root.mpvqcTheme.palette.rowSelected
                    moveDuration: root.animations.highlightMoveDuration
                    appearIndex: _gridView.currentIndex
                }

                delegate: SelectionDelegate {
                    required property string identifier

                    itemSize: root.dimensions.itemSize
                    borderSize: root.dimensions.borderSize

                    onSelected: root.viewModel.setPrimaryColor(identifier)
                }
            }
        }
    }

    onRejected: root.viewModel.reject()
}
