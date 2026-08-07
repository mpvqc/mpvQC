// PROTOTYPE - one fact of the import plan: icon, text, optional second line, optional trailing hint.

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

RowLayout {
    id: root

    property url icon
    property color iconColor: MpvqcAppearance.palette.foreground
    property alias text: _label.text
    property string fullPath: ""
    property string subText: ""
    property string trailing: ""

    readonly property int _iconSize: 20

    spacing: 12

    MpvqcIconLabel {
        iconColor: root.iconColor
        icon.source: root.icon
        icon.width: root._iconSize
        icon.height: root._iconSize

        Layout.preferredWidth: root._iconSize
        Layout.preferredHeight: root._iconSize
        Layout.alignment: Qt.AlignTop
        Layout.topMargin: 2
    }

    ColumnLayout {
        spacing: 2

        Layout.fillWidth: true

        Label {
            id: _label

            horizontalAlignment: Text.AlignLeft
            wrapMode: Text.WrapAtWordBoundaryOrAnywhere

            Layout.fillWidth: true

            ToolTip.text: root.fullPath
            ToolTip.visible: root.fullPath !== "" && _labelHover.hovered
            ToolTip.delay: MpvqcConstants.tooltipDelay

            HoverHandler {
                id: _labelHover
            }
        }

        Label {
            visible: root.subText !== ""
            text: root.subText
            color: MpvqcAppearance.palette.hint
            horizontalAlignment: Text.AlignLeft
            elide: Text.ElideRight

            Layout.fillWidth: true
        }
    }

    Label {
        visible: root.trailing !== ""
        text: root.trailing
        color: MpvqcAppearance.palette.hint
    }
}
