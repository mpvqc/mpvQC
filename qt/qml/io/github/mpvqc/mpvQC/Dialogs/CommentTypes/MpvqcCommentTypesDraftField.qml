// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Utility

ColumnLayout {
    id: root

    required property string validationError
    required property bool addEnabled

    readonly property alias text: _addField.text

    signal addRequested

    function clear(): void {
        _addField.clear();
    }

    function focusInput(): void {
        _addField.forceActiveFocus();
    }

    spacing: 4

    RowLayout {
        spacing: 8

        Layout.fillWidth: true

        TextField {
            id: _addField
            objectName: "commentTypeTextField"

            selectByMouse: true
            bottomPadding: topPadding
            // Inherited mirroring can leave the rendered text at its old alignment.
            horizontalAlignment: root.LayoutMirroring.enabled ? Text.AlignRight : Text.AlignLeft

            Accessible.name: qsTranslate("CommentTypesDialog", "Add comment type")
            ContextMenu.menu: null
            LayoutMirroring.enabled: false
            Layout.fillWidth: true
            Layout.minimumWidth: 0

            onAccepted: root.addRequested()
        }

        Button {
            objectName: "commentTypeAddButton"

            text: qsTranslate("CommentTypesDialog", "Add")
            flat: true
            enabled: root.addEnabled

            onClicked: root.addRequested()
        }
    }

    Label {
        objectName: "commentTypeValidationLabel"

        // Keeps its line while empty, so feedback never pushes the list down.
        text: root.validationError
        color: MpvqcAppearance.palette.error
        wrapMode: Label.WordWrap
        horizontalAlignment: Text.AlignLeft

        Layout.fillWidth: true
    }
}
