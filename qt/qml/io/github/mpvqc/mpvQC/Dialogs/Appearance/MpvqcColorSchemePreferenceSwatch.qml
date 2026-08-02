// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Shapes

import io.github.mpvqc.mpvQC.Utility

Column {
    id: root
    objectName: `colorSchemePreferenceSwatch_${root.preference}`

    required property string preference
    required property string caption
    required property color preview
    required property string alternatePreview
    required property string accent
    required property bool selected

    // System owns no color scheme: it carries the second preview and no accent
    readonly property bool split: root.alternatePreview !== ""
    readonly property bool badged: root.accent !== ""

    property int frameSize: 70

    readonly property int _swatchSize: 60
    readonly property int _swatchRadius: 20
    readonly property int _badgeSize: 20

    // The corner to corner diagonal runs through the corner arcs' centers,
    // so it leaves the outline this far off the corner
    readonly property real _splitOffset: root._swatchRadius * Math.SQRT1_2

    // The halves overlap along the diagonal, otherwise both blend with the
    // background there and leave a seam
    readonly property real _splitOverlap: 0.5

    signal picked(preference: string)

    spacing: 6

    // Only the swatch answers the press: a caption that scales with it reads as a wobble
    Item {
        width: root.frameSize
        height: root.frameSize
        scale: _tap.pressed ? 1.1 : 1.0

        Rectangle {
            anchors.centerIn: parent
            width: root._swatchSize
            height: root._swatchSize
            radius: root._swatchRadius
            color: root.split ? "transparent" : root.preview

            // Both halves are paths of their own: a half painted over a full
            // rounded rectangle blends its antialiased edge into the color
            // underneath, which rims the swatch in grey.
            Shape {
                id: _splitPreview
                objectName: "splitPreview"

                anchors.fill: parent
                visible: root.split
                preferredRendererType: Shape.CurveRenderer

                ShapePath {
                    fillColor: root.alternatePreview
                    strokeColor: "transparent"
                    startX: root._swatchSize - root._swatchRadius + root._splitOffset
                    startY: root._swatchRadius - root._splitOffset

                    PathArc {
                        x: root._swatchSize
                        y: root._swatchRadius
                        radiusX: root._swatchRadius
                        radiusY: root._swatchRadius
                    }
                    PathLine {
                        x: root._swatchSize
                        y: root._swatchSize - root._swatchRadius
                    }
                    PathArc {
                        x: root._swatchSize - root._swatchRadius
                        y: root._swatchSize
                        radiusX: root._swatchRadius
                        radiusY: root._swatchRadius
                    }
                    PathLine {
                        x: root._swatchRadius
                        y: root._swatchSize
                    }
                    PathArc {
                        x: root._swatchRadius - root._splitOffset
                        y: root._swatchSize - root._swatchRadius + root._splitOffset
                        radiusX: root._swatchRadius
                        radiusY: root._swatchRadius
                    }
                }

                ShapePath {
                    fillColor: root.preview
                    strokeColor: "transparent"
                    startX: root._swatchRadius
                    startY: 0

                    PathLine {
                        x: root._swatchSize - root._swatchRadius
                        y: 0
                    }
                    PathArc {
                        x: root._swatchSize - root._swatchRadius + root._splitOffset + root._splitOverlap
                        y: root._swatchRadius - root._splitOffset + root._splitOverlap
                        radiusX: root._swatchRadius
                        radiusY: root._swatchRadius
                    }
                    PathLine {
                        x: root._swatchRadius - root._splitOffset + root._splitOverlap
                        y: root._swatchSize - root._swatchRadius + root._splitOffset + root._splitOverlap
                    }
                    PathArc {
                        x: 0
                        y: root._swatchSize - root._swatchRadius
                        radiusX: root._swatchRadius
                        radiusY: root._swatchRadius
                    }
                    PathLine {
                        x: 0
                        y: root._swatchRadius
                    }
                    PathArc {
                        x: root._swatchRadius
                        y: 0
                        radiusX: root._swatchRadius
                        radiusY: root._swatchRadius
                    }
                }
            }

            Rectangle {
                objectName: "accentBadge"

                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.margins: 6
                width: root._badgeSize
                height: root._badgeSize
                radius: root._badgeSize / 2
                visible: root.badged
                color: root.badged ? root.accent : "transparent"

                Behavior on color {
                    ColorAnimation {
                        duration: 150
                    }
                }
            }
        }

        Behavior on scale {
            NumberAnimation {
                duration: 125
                easing.type: Easing.InOutQuad
            }
        }
    }

    Label {
        objectName: "caption"

        width: root.frameSize
        text: root.caption
        color: root.selected ? MpvqcAppearance.palette.accent : MpvqcAppearance.palette.foreground
        elide: Text.ElideRight
        horizontalAlignment: Text.AlignHCenter
        font.pointSize: MpvqcFonts.applicationFont.pointSize - 1
        font.weight: root.selected ? Font.DemiBold : Font.Normal
    }

    TapHandler {
        id: _tap

        onTapped: root.picked(root.preference)
    }
}
