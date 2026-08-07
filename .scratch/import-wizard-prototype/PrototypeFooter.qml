// PROTOTYPE - the wizard footer, with a configurable primary button.

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material as M
import QtQuick.Layouts

Control {
    id: root

    required property string primaryLabel
    property bool primaryEnabled: true
    property bool showBack: false
    property bool showCancel: true

    signal backClicked()
    signal cancelClicked()
    signal primaryClicked()

    spacing: 8
    horizontalPadding: 8
    verticalPadding: 2

    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset, implicitContentWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset, implicitContentHeight + topPadding + bottomPadding, M.Material.dialogButtonBoxHeight)

    contentItem: RowLayout {
        spacing: root.spacing

        Item {
            Layout.fillWidth: true
        }

        Button {
            flat: true
            visible: root.showBack
            text: "Back"

            onClicked: root.backClicked()
        }

        Button {
            flat: true
            visible: root.showCancel
            text: "Cancel import"

            onClicked: root.cancelClicked()
        }

        Button {
            flat: true
            enabled: root.primaryEnabled
            text: root.primaryLabel

            onClicked: root.primaryClicked()
        }
    }
}
