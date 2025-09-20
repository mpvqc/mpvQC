// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import "../../shared"

MpvqcDialog2 {
    id: root

    readonly property MpvqcAppearanceDialogController controller: MpvqcAppearanceDialogController {}

    readonly property var dimensions: QtObject {
        readonly property int itemSize: 52
        readonly property int itemPadding: 8
        readonly property int borderSize: 5
        readonly property int colorGridRows: 4
        readonly property int themeSpacing: 8
    }

    readonly property var animations: QtObject {
        readonly property int highlightMoveDuration: 150
        readonly property int highlightResizeDuration: 50
        readonly property int colorAnimationDuration: 150
        readonly property int scaleAnimationDuration: 125
        readonly property int populateDuration: 250
        readonly property real scalePressed: 1.1
        readonly property real scaleNormal: 1.0
        readonly property real scaleFrom: 0.85
    }

    readonly property int highlightMoveDuration: controller.suppressColorAnimation ? 0 : animations.highlightMoveDuration

    title: qsTranslate("AppearanceDialog", "Appearance")

    component SelectionDelegate: ItemDelegate {
        id: delegateRoot

        required property int itemSize
        required property int borderSize
        required property color displayColor

        signal selected(int index)

        width: itemSize
        height: itemSize

        background: Rectangle {
            x: delegateRoot.borderSize
            y: delegateRoot.borderSize
            height: parent.height - 2 * delegateRoot.borderSize
            width: parent.width - 2 * delegateRoot.borderSize
            color: delegateRoot.displayColor
            radius: Material.LargeScale
        }

        Behavior on scale {
            NumberAnimation {
                duration: root.animations.scaleAnimationDuration
                easing.type: Easing.InOutQuad
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

        width: size
        height: size
        color: highlightColor
        radius: Material.SmallScale

        border {
            width: borderWidth
            color: borderColor
        }

        Behavior on color {
            ColorAnimation {
                duration: _selectionHighlight.moveDuration
            }
        }
    }

    component PopulateTransition: Transition {
        ParallelAnimation {
            PropertyAnimation {
                property: "opacity"
                from: 0
                to: 1
                duration: root.animations.populateDuration
                easing.type: Easing.OutCubic
            }
            PropertyAnimation {
                property: "scale"
                from: root.animations.scaleFrom
                to: root.animations.scaleNormal
                duration: root.animations.populateDuration
                easing.type: Easing.OutBack
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
                Layout.preferredHeight: root.dimensions.itemSize
                Layout.fillWidth: true

                model: root.controller.themeModel
                currentIndex: root.controller.themeModelIndex
                boundsBehavior: Flickable.StopAtBounds
                orientation: ListView.Horizontal
                clip: true
                spacing: root.dimensions.themeSpacing

                highlightMoveDuration: root.animations.highlightMoveDuration
                highlightMoveVelocity: -1
                highlightResizeDuration: root.animations.highlightResizeDuration
                highlightResizeVelocity: -1

                highlight: SelectionHighlight {
                    size: root.dimensions.itemSize
                    highlightColor: root.controller.controlColor
                    borderWidth: 0
                    borderColor: "transparent"
                    moveDuration: root.animations.highlightMoveDuration
                }

                delegate: SelectionDelegate {
                    required property string identifier
                    required property color preview
                    required property int index

                    itemSize: root.dimensions.itemSize
                    borderSize: root.dimensions.borderSize
                    displayColor: preview

                    onSelected: root.controller.setTheme(identifier)
                }

                populate: PopulateTransition {}
            }

            MpvqcHeader {
                text: qsTranslate("AppearanceDialog", "Color")

                Layout.alignment: Qt.AlignLeft
            }

            GridView {
                Layout.preferredHeight: {
                    const d = root.dimensions;
                    return (d.itemSize + d.itemPadding) * d.colorGridRows;
                }
                Layout.fillWidth: true

                model: root.controller.colorModel
                currentIndex: root.controller.colorModelIndex
                boundsBehavior: Flickable.StopAtBounds
                clip: true

                cellWidth: root.dimensions.itemSize + root.dimensions.itemPadding
                cellHeight: root.dimensions.itemSize + root.dimensions.itemPadding

                highlightMoveDuration: root.highlightMoveDuration

                onModelChanged: root.controller.restoreColorOptionIndexAfterModelChange()

                highlight: SelectionHighlight {
                    size: root.dimensions.itemSize
                    highlightColor: root.controller.colorOptionHighlightColor
                    borderWidth: root.controller.colorOptionHighlightBorderWidth
                    borderColor: root.controller.colorOptionHighlightBorderColor
                    moveDuration: root.highlightMoveDuration
                }

                delegate: SelectionDelegate {
                    required property color rowHighlight
                    required property int index

                    itemSize: root.dimensions.itemSize
                    borderSize: root.dimensions.borderSize
                    displayColor: rowHighlight

                    onSelected: idx => root.controller.setColorOption(idx)
                }

                populate: PopulateTransition {}
            }
        }
    }

    onRejected: root.controller.reset()

    Component.onCompleted: root.controller.init()
}
