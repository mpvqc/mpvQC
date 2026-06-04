// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material as M
import QtQuick.Layouts

Control {
    id: root

    required property string primaryLabel
    required property bool showBack
    required property bool showCancel

    signal backClicked
    signal cancelClicked
    signal primaryClicked

    spacing: 8
    horizontalPadding: 8
    verticalPadding: 2

    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset, implicitContentWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset, implicitContentHeight + topPadding + bottomPadding, M.Material.dialogButtonBoxHeight)

    component FooterButton: Button {
        required property bool shown

        visible: opacity > 0
        opacity: shown ? 1 : 0
        Layout.preferredWidth: shown ? implicitWidth : 0
        flat: true
        clip: true

        Behavior on opacity {
            NumberAnimation {
                duration: 150
                easing.type: Easing.OutCubic
            }
        }
    }

    contentItem: RowLayout {
        spacing: root.spacing

        Item {
            Layout.fillWidth: true
        }

        FooterButton {
            objectName: "backButton"
            shown: root.showBack
            //: Button that returns the import wizard to the previous step
            text: qsTranslate("ImportWizardDialog", "Back")

            onClicked: root.backClicked()
        }

        FooterButton {
            objectName: "cancelButton"
            shown: root.showCancel
            //: Button that aborts the import wizard and discards any parsed comments
            text: qsTranslate("ImportWizardDialog", "Cancel import")

            onClicked: root.cancelClicked()
        }

        Button {
            objectName: "primaryButton"
            flat: true

            text: root.primaryLabel

            onClicked: root.primaryClicked()
        }
    }
}
