// PROTOTYPE - ScrollView for a column of section cards. No scrollbar: gradient scrims at the
// top and bottom edges let content dissolve into the background, signalling more in that
// direction - the same cue the shipped wizard's step indicator uses horizontally.

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Utility

ScrollView {
    id: root

    property alias sectionSpacing: _column.spacing
    default property alias content: _column.data

    readonly property int _fadeHeight: 24

    function scrollToTop(): void {
        contentItem.contentY = 0;
    }

    contentWidth: availableWidth
    contentHeight: _column.implicitHeight

    ScrollBar.vertical: ScrollBar {
        policy: ScrollBar.AlwaysOff
    }

    Component.onCompleted: contentItem.boundsBehavior = Flickable.StopAtBounds

    ColumnLayout {
        id: _column

        width: root.availableWidth
    }

    Rectangle {
        parent: root

        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right

        height: root._fadeHeight
        // Proportional to the distance from the edge: gone the instant the top is reached
        opacity: Math.min(1, Math.max(0, root.contentItem.contentY) / root._fadeHeight)
        gradient: Gradient {
            GradientStop {
                position: 0
                color: MpvqcAppearance.palette.dialogBackground
            }
            GradientStop {
                position: 1
                color: "transparent"
            }
        }
    }

    Rectangle {
        parent: root

        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right

        height: root._fadeHeight
        // Proportional to the distance from the edge: gone the instant the end is reached
        opacity: Math.min(1, Math.max(0, root.contentHeight - root.height - root.contentItem.contentY) / root._fadeHeight)
        gradient: Gradient {
            GradientStop {
                position: 0
                color: "transparent"
            }
            GradientStop {
                position: 1
                color: MpvqcAppearance.palette.dialogBackground
            }
        }
    }
}
