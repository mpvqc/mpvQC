// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

Control {
    id: root

    required property string label
    required property var sequences

    property string note: ""
    property bool striped: false

    height: Math.max(implicitHeight, MpvqcConstants.listRowHeight)
    horizontalPadding: 8
    verticalPadding: 10

    contentItem: RowLayout {
        id: _content

        Label {
            text: root.label
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignLeft

            Layout.maximumWidth: root.availableWidth - _sequences.width - (_noteIcon.visible ? _noteIcon.width + _content.spacing : 0) - 2 * _content.spacing
        }

        MpvqcIconLabel {
            id: _noteIcon
            objectName: "noteIcon"

            visible: root.note !== ""
            icon.source: MpvqcIcons.info
            icon.width: 16
            icon.height: 16
            iconColor: MpvqcTheme.palette.hint
            toolTipText: root.note
        }

        Item {
            Layout.fillWidth: true
        }

        Row {
            id: _sequences

            spacing: 4

            Repeater {
                model: root.sequences

                delegate: Row {
                    id: _sequence

                    required property var modelData
                    required property int index

                    spacing: 4

                    Label {
                        objectName: "sequenceSeparator"

                        text: "/"
                        visible: _sequence.index > 0

                        anchors.verticalCenter: parent.verticalCenter
                    }

                    Repeater {
                        model: _sequence.modelData

                        delegate: Row {
                            id: _key

                            required property var modelData
                            required property int index

                            spacing: 4

                            Label {
                                objectName: "keySeparator"

                                text: "+"
                                visible: _key.index > 0

                                anchors.verticalCenter: parent.verticalCenter
                            }

                            MpvqcKeycap {
                                objectName: "keycap"

                                text: _key.modelData.text ?? ""
                                icon: _key.modelData.icon ?? ""

                                anchors.verticalCenter: parent.verticalCenter
                            }
                        }
                    }
                }
            }
        }
    }

    background: Rectangle {
        radius: 4
        color: root.striped ? MpvqcTheme.listStripe : "transparent"
    }
}
