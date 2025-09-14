// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

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
    readonly property bool textFieldHasFocus: (_loader.item as MpvqcInputControls).textFieldHasFocus

    signal added(input: string)
    signal edited(input: string)

    function startEditing(text: string): void {
        _loader.startEditMode();
        _loader.setPlaceholder(text);
        _loader.setText(text);
    }

    function stopEditing(): void {
        _loader.stopEditMode();
    }

    Loader {
        id: _loader

        property bool editing: false

        width: root.width
        sourceComponent: editing ? _edit : _add

        function startEditMode(): void {
            editing = true;
        }

        function stopEditMode(): void {
            editing = false;
        }

        function setText(text: string): void {
            item.text = text;
        }

        function setPlaceholder(text: string): void {
            item.placeholderText = text;
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
