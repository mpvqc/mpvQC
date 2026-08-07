// PROTOTYPE - a small pill holding an origin icon, marking where a candidate resource comes
// from. Tint follows the row's selection state.

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

Rectangle {
    id: root

    property url icon
    property color tint: MpvqcAppearance.palette.hint
    property string toolTipText: ""
    property bool _ready: false

    readonly property int _iconSize: 18

    implicitWidth: 38
    implicitHeight: 24
    radius: height / 2
    color: Qt.alpha(root.tint, 0.12)

    ToolTip.text: root.toolTipText
    ToolTip.visible: root.toolTipText !== "" && _hover.hovered
    ToolTip.delay: MpvqcConstants.tooltipDelay

    Component.onCompleted: root._ready = true

    Behavior on tint {
        enabled: root._ready

        ColorAnimation {
            duration: 120
        }
    }

    MpvqcIconLabel {
        anchors.centerIn: parent

        iconColor: root.tint
        icon.source: root.icon
        icon.width: root._iconSize
        icon.height: root._iconSize
    }

    HoverHandler {
        id: _hover
    }
}
