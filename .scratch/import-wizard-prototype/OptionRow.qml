// PROTOTYPE - radio-style choice row, Material 3 look: full pill, tonal fill when selected.

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

ItemDelegate {
    id: root

    required property bool selected

    property string fullPath: ""
    property bool _ready: false
    property bool fromDocument: false
    property bool fromSubtitle: false

    // One shared row height across all wizard lists keeps page transitions calm
    implicitHeight: Math.max(implicitContentHeight + topPadding + bottomPadding, MpvqcConstants.listRowHeight)
    verticalPadding: 10
    horizontalPadding: 14

    background: Rectangle {
        radius: height / 2
        color: root.selected ? Qt.alpha(MpvqcAppearance.palette.accent, 0.16)
            : root.hovered ? Qt.alpha(MpvqcAppearance.palette.foreground, 0.08)
            : "transparent"

        Behavior on color {
            enabled: root._ready

            ColorAnimation {
                duration: 120
            }
        }
    }

    Component.onCompleted: root._ready = true

    contentItem: RowLayout {
        spacing: 12

        RadioIndicator {
            selected: root.selected
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

        OriginPill {
            visible: root.fromDocument
            icon: MpvqcIcons.description
            tint: root.selected ? MpvqcAppearance.palette.accent : MpvqcAppearance.palette.hint
            toolTipText: "Referenced by an imported QC document"
        }

        OriginPill {
            visible: root.fromSubtitle
            icon: MpvqcIcons.subtitles
            tint: root.selected ? MpvqcAppearance.palette.accent : MpvqcAppearance.palette.hint
            toolTipText: "Referenced by an imported subtitle file"
        }
    }
}
