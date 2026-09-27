// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material as M
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Utility

Item {
    id: root
    objectName: "commentTypeRow"

    required property string commentType
    required property real gutter

    readonly property alias dragHandle: _dragHandle

    property bool lifted: false
    property bool hoverFeedback: true
    property bool deleteEnabled: true

    readonly property color _hoverColor: Qt.alpha(MpvqcAppearance.palette.foreground, MpvqcAppearance.isDark ? 0.08 : 0.12)

    signal deleteClicked

    implicitHeight: MpvqcConstants.listRowHeight

    Rectangle {
        objectName: "commentTypeRowBase"

        anchors.fill: _background
        radius: _background.radius
        color: root.lifted ? MpvqcAppearance.palette.sectionCard : "transparent"
    }

    Rectangle {
        id: _background
        objectName: "commentTypeRowBackground"

        anchors.fill: parent
        anchors.rightMargin: root.gutter
        radius: 8
        color: root.lifted || root.hoverFeedback && (_hover.hovered || _deleteButton.visualFocus) ? root._hoverColor : "transparent"

        HoverHandler {
            id: _hover
        }

        RowLayout {
            anchors.fill: parent
            spacing: 8

            Item {
                id: _dragHandle
                objectName: "commentTypeDragHandle"

                implicitWidth: 32

                Layout.fillHeight: true

                Grid {
                    anchors.centerIn: parent
                    columns: 2
                    spacing: 3

                    Repeater {
                        model: 6

                        Rectangle {
                            width: 3
                            height: 3
                            radius: 1.5
                            color: MpvqcAppearance.palette.hint
                        }
                    }
                }

                HoverHandler {
                    cursorShape: Qt.OpenHandCursor
                }
            }

            Label {
                objectName: "commentTypeLabel"

                text: qsTranslate("CommentTypes", root.commentType)
                textFormat: Text.PlainText
                color: MpvqcAppearance.palette.foreground
                elide: LayoutMirroring.enabled ? Text.ElideLeft : Text.ElideRight
                horizontalAlignment: Text.AlignLeft

                Layout.fillWidth: true
                Layout.minimumWidth: 0
            }

            ToolButton {
                id: _deleteButton
                objectName: "commentTypeDeleteButton"

                //: Accessible name of the icon-only button that deletes a comment type
                text: qsTranslate("CommentTypesDialog", "Delete")
                display: AbstractButton.IconOnly
                enabled: root.deleteEnabled
                hoverEnabled: !root.lifted
                focusPolicy: root.lifted ? Qt.NoFocus : Qt.StrongFocus
                icon.source: MpvqcIcons.delete_

                background: Rectangle {
                    radius: 8
                    color: _deleteButton.down ? Qt.alpha(MpvqcAppearance.palette.foreground, 0.16) : _deleteButton.hovered || _deleteButton.visualFocus ? root._hoverColor : "transparent"
                }

                M.Material.foreground: MpvqcAppearance.palette.error
                Layout.margins: 4
                Layout.leftMargin: 0
                // A delegate created before the dialog is in a window loads its icon at another
                // device pixel ratio; the button must not take its size from that icon.
                Layout.fillHeight: true
                Layout.preferredWidth: height

                onClicked: root.deleteClicked()
            }
        }
    }
}
