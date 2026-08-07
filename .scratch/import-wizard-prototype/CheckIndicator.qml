// PROTOTYPE - Material 3 Expressive check indicator: outlined rounded square when unchecked,
// morphing into an accent circle with a check when checked; partial shows an accent square
// with a rounded dash. The whole indicator squashes and pops on every state change, and the
// glyphs bounce in.

pragma ComponentBehavior: Bound

import QtQuick

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

Rectangle {
    id: root

    property bool checked: false
    property bool partial: false

    // Animations play only for user interaction, not while a page instantiates
    property bool _ready: false

    implicitWidth: 20
    implicitHeight: 20
    radius: root.checked ? 10 : 6
    color: root.checked || root.partial ? MpvqcAppearance.palette.accent : "transparent"
    border.width: root.checked || root.partial ? 0 : 2
    border.color: MpvqcAppearance.palette.hint

    onCheckedChanged: if (root._ready) _pop.restart()
    onPartialChanged: if (root._ready) _pop.restart()

    Component.onCompleted: root._ready = true

    Behavior on radius {
        enabled: root._ready

        NumberAnimation {
            duration: 260
            easing.type: Easing.OutBack
        }
    }

    Behavior on color {
        enabled: root._ready

        ColorAnimation {
            duration: 150
        }
    }

    MpvqcIconLabel {
        anchors.centerIn: parent

        scale: root.checked ? 1 : 0
        iconColor: MpvqcAppearance.palette.dialogBackground
        icon.source: MpvqcIcons.check
        icon.width: 14
        icon.height: 14

        Behavior on scale {
            enabled: root._ready

            NumberAnimation {
                duration: 260
                easing.type: Easing.OutBack
            }
        }
    }

    Rectangle {
        anchors.centerIn: parent

        scale: !root.checked && root.partial ? 1 : 0
        width: 10
        height: 2.5
        radius: 1.25
        color: MpvqcAppearance.palette.dialogBackground

        Behavior on scale {
            enabled: root._ready

            NumberAnimation {
                duration: 260
                easing.type: Easing.OutBack
            }
        }
    }

    SequentialAnimation {
        id: _pop

        NumberAnimation {
            target: root
            property: "scale"
            to: 0.8
            duration: 70
            easing.type: Easing.InOutQuad
        }

        NumberAnimation {
            target: root
            property: "scale"
            to: 1
            duration: 240
            easing.type: Easing.OutBack
        }
    }
}
