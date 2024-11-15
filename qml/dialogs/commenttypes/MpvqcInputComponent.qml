/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

import QtQuick


Column {
    id: root

    required property var mpvqcApplication

    required property var validateNewCommentType        // function with:
                                                        //   param :  input
                                                        //   return:  string or null | validation error if error exists
    required property var validateEditingOfCommentType  // function with:
                                                        //   param :  input
                                                        //   param :  comment type being edited
                                                        //   return:  string or null | validation error if error exists

    readonly property alias loader: _loader
    readonly property alias editing: _loader.editing
    readonly property bool textFieldHasFocus: _loader.item.textFieldHasFocus

    signal added(string input)
    signal edited(string input)

    function startEditing(text: string): void {
        _loader.startEditMode()
        _loader.setPlaceholder(text)
        _loader.setText(text)
    }

    function stopEditing() {
        _loader.stopEditMode()
    }

    Loader {
        id: _loader

        property bool editing: false

        width: root.width
        sourceComponent: editing ? _edit : _add

        function startEditMode(): void {
            editing = true
        }

        function stopEditMode(): void {
            editing = false
        }

        function setText(text: string): void {
            item.text = text
        }

        function setPlaceholder(text: string): void {
            item.placeholderText = text
        }

    }

    Component {
        id: _add

        MpvqcInputControls {
            objectName: "MpvqcInputControls::add"

            mpvqcApplication: root.mpvqcApplication
            focusTextFieldOnCompletion: false

            placeholderText: qsTranslate("CommentTypesDialog", "New comment type")

            validateInput: input => root.validateNewCommentType(input)

            onAccepted: input => root.added(input)
        }
    }

    Component {
        id: _edit

        MpvqcInputControls {
            objectName: "MpvqcInputControls::edit"

            mpvqcApplication: root.mpvqcApplication
            focusTextFieldOnCompletion: true

            validateInput: input => root.validateEditingOfCommentType(input, placeholderText)

            onAccepted: input => root.edited(input)

            onDone: _loader.stopEditMode()
        }
    }

}
