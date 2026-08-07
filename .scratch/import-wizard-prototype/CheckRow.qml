// PROTOTYPE - checkbox choice row, borrowed from the wizard's subtitles step delegate.

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Utility

ItemDelegate {
    id: root

    required property bool isChecked

    property string fullPath: ""

    signal toggleRequested()

    // One shared row height across all wizard lists keeps page transitions calm
    implicitHeight: Math.max(implicitContentHeight + topPadding + bottomPadding, MpvqcConstants.listRowHeight)
    verticalPadding: 10
    horizontalPadding: 14

    background: Rectangle {
        radius: height / 2
        color: root.hovered ? Qt.alpha(MpvqcAppearance.palette.foreground, 0.08) : "transparent"

        Behavior on color {
            ColorAnimation {
                duration: 150
            }
        }
    }

    contentItem: RowLayout {
        spacing: 12

        CheckIndicator {
            checked: root.isChecked

            Layout.alignment: Qt.AlignVCenter
        }

        Label {
            text: root.text
            horizontalAlignment: Text.AlignLeft
            wrapMode: Text.WrapAtWordBoundaryOrAnywhere

            Layout.fillWidth: true
            Layout.alignment: Qt.AlignVCenter

            ToolTip.text: root.fullPath
            ToolTip.visible: root.fullPath !== "" && _labelHover.hovered
            ToolTip.delay: MpvqcConstants.tooltipDelay

            HoverHandler {
                id: _labelHover
            }
        }
    }

    onClicked: root.toggleRequested()
}
