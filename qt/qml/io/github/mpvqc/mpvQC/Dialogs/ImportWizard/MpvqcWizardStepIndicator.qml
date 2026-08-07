// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

Item {
    id: root

    required property var steps
    required property int currentStepIndex
    readonly property int glyphSize: 20
    readonly property int fadeWidth: 96
    readonly property int animationDuration: 150

    signal stepClicked(index: int)

    implicitHeight: _list.implicitHeight

    ListView {
        id: _list

        anchors.horizontalCenter: parent.horizontalCenter
        height: parent.height

        implicitHeight: 28
        cacheBuffer: 100000

        orientation: ListView.Horizontal
        spacing: 16
        clip: true
        interactive: false
        boundsBehavior: Flickable.StopAtBounds

        model: root.steps

        currentIndex: root.currentStepIndex
        highlight: Item {}
        highlightMoveDuration: root.animationDuration
        highlightMoveVelocity: -1
        highlightRangeMode: ListView.ApplyRange
        preferredHighlightBegin: width / 2
        preferredHighlightEnd: width / 2

        delegate: Row {
            id: _entry

            required property int index
            required property var modelData

            readonly property bool isLast: _entry.index === root.steps.length - 1
            readonly property bool isCompleted: _entry.index < root.currentStepIndex
            readonly property bool isCurrent: _entry.index === root.currentStepIndex

            anchors.verticalCenter: parent ? parent.verticalCenter : undefined
            spacing: 8

            AbstractButton {
                id: _entryButton
                objectName: "stepEntry"

                anchors.verticalCenter: parent.verticalCenter
                padding: 0

                contentItem: Row {
                    spacing: 8

                    MpvqcWizardStepGlyph {
                        objectName: "stepGlyph"

                        anchors.verticalCenter: parent.verticalCenter

                        completed: _entry.isCompleted
                        current: _entry.isCurrent
                        size: root.glyphSize
                        animationDuration: root.animationDuration
                    }

                    Label {
                        objectName: "stepLabel"

                        anchors.verticalCenter: parent.verticalCenter

                        horizontalAlignment: Text.AlignLeft
                        text: _entry.modelData.indicatorLabel
                    }
                }

                onClicked: root.stepClicked(_entry.index)

                HoverHandler {
                    cursorShape: _entry.isCurrent ? Qt.ArrowCursor : Qt.PointingHandCursor
                }
            }

            MpvqcIconLabel {
                objectName: "stepConnector"

                anchors.verticalCenter: parent.verticalCenter

                visible: !_entry.isLast

                icon {
                    source: Application.layoutDirection === Qt.RightToLeft ? MpvqcIcons.keyboardArrowLeft : MpvqcIcons.keyboardArrowRight
                    width: root.glyphSize
                    height: root.glyphSize
                    color: MpvqcAppearance.palette.hint
                }
            }
        }

        Binding {
            target: _list
            property: "width"
            value: Math.min(_list.contentWidth, _list.parent.width)
            delayed: true
        }
    }

    Rectangle {
        objectName: "leftFade"

        anchors {
            left: _list.left
            top: _list.top
            bottom: _list.bottom
        }
        width: root.fadeWidth

        opacity: !_list.atXBeginning ? 1 : 0
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop {
                position: 0
                color: MpvqcAppearance.palette.background
            }
            GradientStop {
                position: 1
                color: "transparent"
            }
        }

        LayoutMirroring.enabled: false

        Behavior on opacity {
            NumberAnimation {
                duration: root.animationDuration
            }
        }
    }

    Rectangle {
        objectName: "rightFade"

        anchors {
            right: _list.right
            top: _list.top
            bottom: _list.bottom
        }
        width: root.fadeWidth

        opacity: !_list.atXEnd ? 1 : 0
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop {
                position: 0
                color: "transparent"
            }
            GradientStop {
                position: 1
                color: MpvqcAppearance.palette.background
            }
        }

        LayoutMirroring.enabled: false

        Behavior on opacity {
            NumberAnimation {
                duration: root.animationDuration
            }
        }
    }
}
