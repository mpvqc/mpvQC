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
import helpers
import pyobjects


Loader {
    id: loader

    property string comment
    property bool editing: false
    property int customPadding: 4

    signal edited(string comment)

    sourceComponent: editing ? textFieldComponent : labelComponent

    Component {
        id: labelComponent

        Label {
            id: label

            text: loader.comment
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
            elide: TranslationPyObject.rtl_enabled ? Text.ElideLeft: Text.ElideRight
            leftPadding: loader.customPadding
            rightPadding: loader.customPadding
            anchors.fill: loader

            TapHandler {
                onDoubleTapped: startEditing()
            }
        }
    }

    Component {
        id: textFieldComponent

        TextField {
            id: textInput

            property bool cancelling: false

            property int minimalEditingTime: 250
            property bool minimalEditingTimeExpired: false

            text: loader.comment
            selectByMouse: true
            anchors.fill: loader
            leftPadding: loader.customPadding
            rightPadding: loader.customPadding
            horizontalAlignment: Text.AlignLeft
            bottomPadding: topPadding
            background: Rectangle {
                anchors.fill: parent
                anchors.topMargin: loader.customPadding
                anchors.bottomMargin: loader.customPadding
                color: Material.background
            }

            Component.onCompleted: {
                focusTextField()
                MpvqcTimer.scheduleOnceAfter(minimalEditingTime, function() { expireMinimalEditingTime() })
            }

            Keys.onEscapePressed: {
                cancelling = true
                focus = false
            }

            onEditingFinished: (event) => {
                if (!minimalEditingTimeExpired) {
                    focusTextField()
                    return
                }
                if (!cancelling) {
                    triggerCommentEdited()
                }
                stopEditing()
            }

            function focusTextField() {
                cursorPosition = text.length
                forceActiveFocus()
            }

            function expireMinimalEditingTime() {
                minimalEditingTimeExpired = true
            }

            function triggerCommentEdited() {
                loader.edited(textInput.text)
            }
        }
    }

    function startEditing() {
        loader.editing = true
    }

    function stopEditing() {
        loader.editing = false
    }

}
