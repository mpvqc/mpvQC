// PROTOTYPE - Material 3 Expressive radio indicator: outlined circle when unselected, accent
// fill with a popping inner dot when selected.

pragma ComponentBehavior: Bound

import QtQuick

import io.github.mpvqc.mpvQC.Utility

Rectangle {
    id: root

    property bool selected: false

    // Animations play only for user interaction, not while a page instantiates
    property bool _ready: false

    implicitWidth: 20
    implicitHeight: 20
    radius: 10
    color: root.selected ? MpvqcAppearance.palette.accent : "transparent"
    border.width: root.selected ? 0 : 2
    border.color: MpvqcAppearance.palette.hint

    Component.onCompleted: root._ready = true

    Behavior on color {
        enabled: root._ready

        ColorAnimation {
            duration: 120
        }
    }

    Rectangle {
        anchors.centerIn: parent

        width: root.selected ? 8 : 0
        height: width
        radius: width / 2
        color: MpvqcAppearance.palette.dialogBackground

        // Deselection settles plainly and fast; only the incoming dot pops, and gently
        Behavior on width {
            enabled: root._ready

            NumberAnimation {
                duration: root.selected ? 240 : 100
                easing.type: root.selected ? Easing.OutBack : Easing.OutCubic
                easing.overshoot: 1.2
            }
        }
    }
}
