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
import QtQuick.Layouts


Column {
    id: root

    required property var mpvqcApplication

    property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    property var mpvqcReverseTranslatorPyObject: mpvqcApplication.mpvqcReverseTranslatorPyObject

    function acceptTemporaryState(): void {
        _controller.acceptModelCopy()
        mpvqcSettings.commentTypesChanged()
    }

    function resetTemporaryEdits(): void {
        _input.stopEditing()
        _controller.reset()
    }

    MpvqcCommentTypesViewController {
        id: _controller

        model: mpvqcSettings.commentTypes
        selectedIndex: _listView.currentIndex

        onEditClicked: (commentType) => {
            const translated = qsTranslate('CommentTypes', commentType)
            _input.startEditing(translated)
        }
    }

    MpvqcCommentTypesValidator {
        id: _validator

        model: _listView.model
        language: root.mpvqcSettings.language
        reverseTranslator: root.mpvqcReverseTranslatorPyObject
    }

    MpvqcInputComponent {
        id: _input

        validator: _validator
        width: root.width
        height: 100
        topPadding: 15

        onAdded: (commentType) => {
            _controller.add(commentType)
        }

        onEdited: (commentType) => {
            const english = root.mpvqcReverseTranslatorPyObject.lookup_specific_language(root.mpvqcSettings.language, commentType)
            _controller.replaceWith(english)
        }
    }

    RowLayout {
        width: root.width

        MpvqcList {
            id: _listView

            itemHeight: _listViewControls.buttonHeight
            model: _controller.modelCopy
            enabled: !_input.editing
            height: 7 * itemHeight

            Layout.fillWidth: true
        }

        MpvqcListControls {
            id: _listViewControls

            readonly property bool controlsEnabled: !_input.textFieldHasFocus && _listView.enabled

            height: _listView.height
            upEnabled: controlsEnabled && _listView.currentIndex > 0
            downEnabled: controlsEnabled && _listView.currentIndex !== _listView.model.count - 1
            editEnabled: controlsEnabled && _listView.currentIndex >= 0
            deleteEnabled: controlsEnabled && _listView.currentIndex >= 0

            onUpClicked: {
                _controller.moveUp()
            }

            onDownClicked: {
                _controller.moveDown()
            }

            onEditClicked: {
                _controller.startEditing()
            }

            onDeleteClicked: {
                _controller.deleteItem()
            }
        }
    }

}
