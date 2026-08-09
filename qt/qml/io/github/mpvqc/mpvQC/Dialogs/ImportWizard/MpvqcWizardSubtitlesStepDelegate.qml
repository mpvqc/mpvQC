// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components

MpvqcWizardChoiceRow {
    id: root

    required property int index
    required property string filename
    required property string fullPath
    required property bool isChecked

    toolTipText: root.fullPath

    MpvqcCheckIndicator {
        objectName: "checkIndicator"

        checked: root.isChecked

        Layout.alignment: Qt.AlignVCenter
    }

    Label {
        objectName: "label"

        text: root.filename
        horizontalAlignment: Text.AlignLeft
        wrapMode: Text.WrapAtWordBoundaryOrAnywhere

        Layout.fillWidth: true
        Layout.alignment: Qt.AlignVCenter
    }
}
