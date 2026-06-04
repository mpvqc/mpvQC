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

    readonly property var mpvqcTheme: MpvqcTheme

    signal addRequested

    function clear(): void {
        _addField.text = "";
    }

    function focusInput(): void {
        _addField.forceActiveFocus();
    }

    spacing: 10

    RowLayout {
        Layout.fillWidth: true

        TextField {
            id: _addField
            objectName: "commentTypeTextField"

            Layout.fillWidth: true
            ContextMenu.menu: null

            selectByMouse: true
            horizontalAlignment: Text.AlignLeft
            placeholderText: qsTranslate("CommentTypesDialog", "New comment type")

            onAccepted: root.addRequested()
        }

        ToolButton {
            objectName: "commentTypeAddButton"
            enabled: root.addEnabled

            icon {
                width: 20
                height: 20
                source: MpvqcIcons.add
            }

            onPressed: root.addRequested()
        }
    }

    Item {
        Layout.fillWidth: true
        Layout.preferredHeight: (fontMetrics.lineSpacing * _errorLabel.lineCount) + _errorLabel.topPadding + _errorLabel.bottomPadding

        Label {
            id: _errorLabel
            objectName: "commentTypeValidationLabel"

            anchors.fill: parent

            topPadding: 4
            bottomPadding: 6

            text: root.validationError
            maximumLineCount: 3
            color: root.mpvqcTheme.palette.error
            wrapMode: Label.WordWrap
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignTop

            FontMetrics {
                id: fontMetrics
                font: _errorLabel.font
            }
        }
    }
}
