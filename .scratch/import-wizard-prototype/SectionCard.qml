// PROTOTYPE - the appearance dialog's section card, without the fold animation.

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Utility

Item {
    id: root

    property alias title: _title.text
    property alias contentSpacing: _content.spacing
    property alias titleActions: _titleActions.data
    default property alias content: _content.data

    readonly property int _padding: 20

    implicitHeight: _content.implicitHeight + 2 * root._padding

    Rectangle {
        anchors.fill: parent
        radius: 20
        color: MpvqcAppearance.palette.sectionCard
    }

    ColumnLayout {
        id: _content

        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: root._padding

        spacing: 8

        RowLayout {
            visible: _title.text !== ""
            spacing: 8

            Layout.fillWidth: true

            Label {
                id: _title

                font.weight: Font.DemiBold
                bottomPadding: 8
            }

            Item {
                Layout.fillWidth: true
            }

            RowLayout {
                id: _titleActions

                spacing: 8
            }
        }
    }
}
