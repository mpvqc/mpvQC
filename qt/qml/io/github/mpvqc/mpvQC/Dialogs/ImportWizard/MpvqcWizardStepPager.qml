// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls

import io.github.mpvqc.mpvQC.Utility

Row {
    id: root

    required property var stepNames
    required property int currentStepIndex

    readonly property int _dotWidth: 32
    readonly property int _dotHeight: 28
    readonly property int _indicatorHeight: 10
    readonly property int _pillWidth: 24
    readonly property int _stretchDuration: MpvqcConstants.wizardStepMotionDuration
    readonly property int _tintDuration: 120

    signal stepClicked(index: int)

    spacing: 0

    Repeater {
        model: root.stepNames

        delegate: AbstractButton {
            id: _dot
            objectName: "pagerDot"

            required property int index
            required property string modelData

            readonly property bool isCurrent: _dot.index === root.currentStepIndex
            readonly property bool isBehind: _dot.index < root.currentStepIndex

            width: root._dotWidth
            height: root._dotHeight
            hoverEnabled: true

            ToolTip.text: _dot.modelData
            ToolTip.visible: _dot.hovered
            ToolTip.delay: MpvqcConstants.tooltipDelay

            onClicked: root.stepClicked(_dot.index)

            HoverHandler {
                cursorShape: _dot.isCurrent ? Qt.ArrowCursor : Qt.PointingHandCursor
            }

            Rectangle {
                objectName: "pagerDotIndicator"

                anchors.centerIn: parent

                width: _dot.isCurrent ? root._pillWidth : root._indicatorHeight
                height: root._indicatorHeight
                radius: height / 2
                color: {
                    if (_dot.isCurrent) {
                        return MpvqcAppearance.palette.accent;
                    }
                    if (_dot.isBehind) {
                        return Qt.alpha(MpvqcAppearance.palette.foreground, _dot.hovered ? 0.65 : 0.45);
                    }
                    return Qt.alpha(MpvqcAppearance.palette.foreground, _dot.hovered ? 0.35 : 0.2);
                }

                Behavior on width {
                    NumberAnimation {
                        duration: root._stretchDuration
                        easing.type: Easing.OutCubic
                    }
                }

                Behavior on color {
                    ColorAnimation {
                        duration: root._tintDuration
                    }
                }
            }
        }
    }
}
