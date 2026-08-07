// PROTOTYPE - tri-state "Select all" with a Material 3 Expressive indicator: outlined rounded
// square when nothing is selected, accent square with a rounded dash when partially selected,
// morphing into a filled circle with a check when everything is.

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

AbstractButton {
    id: root

    required property int checkedCount
    required property int totalCount

    readonly property bool allChecked: root.checkedCount === root.totalCount
    readonly property bool noneChecked: root.checkedCount === 0

    signal toggleAllRequested()

    text: "Select all"
    hoverEnabled: true
    padding: 6
    leftPadding: 10
    rightPadding: 10

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
        spacing: 8

        CheckIndicator {
            checked: root.allChecked
            partial: !root.allChecked && !root.noneChecked
        }

        Label {
            text: root.text
        }
    }

    onClicked: root.toggleAllRequested()

    HoverHandler {
        cursorShape: Qt.PointingHandCursor
    }
}
