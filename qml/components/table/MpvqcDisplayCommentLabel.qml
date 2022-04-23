/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick
import QtQuick.Controls
import pyobjects


Loader {
    id: control
    sourceComponent: editing ? editComponent : displayComponent

    property string comment
    property bool itemSelected
    property bool editing: false
    property int borderPadding: 4

    signal clicked()
    signal edited(string comment)

    Component {
        id: displayComponent

        Label {
            text: control.comment
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            elide: LayoutMirroring.enabled ? Text.ElideLeft: Text.ElideRight
            leftPadding: control.borderPadding
            rightPadding: control.borderPadding
            anchors.fill: control

            MouseArea {
                anchors.fill: parent

                onClicked: {
                    if (itemSelected) {
                        startEditing()
                    } else {
                        triggerClicked()
                    }
                }
            }
        }
    }

    Component {
        id: editComponent

        MpvqcEditCommentTextField {
            text: control.comment
            anchors.fill: control
            borderPadding: control.borderPadding

            onEdited: (comment) => {
                triggerCommentEdited(comment)
            }

            onDone: {
                stopEditing()
            }
        }
    }

    function startEditing() {
        control.editing = true
    }

    function stopEditing() {
        control.editing = false
    }

    function triggerClicked() {
        control.clicked()
    }

    function triggerCommentEdited(comment) {
        control.edited(comment)
    }
}
