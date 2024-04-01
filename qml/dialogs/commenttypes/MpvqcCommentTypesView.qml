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
    property var mpvqcUtilityPyObject: mpvqcApplication.mpvqcUtilityPyObject
    property var mpvqcCommentTypeValidatorPyObject: mpvqcApplication.mpvqcCommentTypeValidatorPyObject

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

        onHighlightIndexRequested: index => {
            _listView.currentIndex = index
        }

        onEditClicked: (commentType) => {
            const translated = qsTranslate('CommentTypes', commentType)
            _input.startEditing(translated)
        }

        onAcceptCopyRequested: copy => {
            const newCommentTypes = copy.length === 0 ? mpvqcSettings.getDefaultCommentTypes() : copy

            mpvqcSettings.commentTypes.length = 0
            mpvqcSettings.commentTypes.push(...newCommentTypes)
        }

        onResetRequested: {
            _controller.model.length = 0
            _controller.model.push(...mpvqcSettings.getDefaultCommentTypes())
        }
    }

    MpvqcInputComponent {
        id: _input

        width: root.width
        height: 100
        topPadding: 15

        validateNewCommentType: (input) => {
            const items = _listView.model
            return mpvqcCommentTypeValidatorPyObject.validate_new_comment_type(input, items)
        }

        validateEditingOfCommentType: (input, inputBeingEdited) => {
            const items = _listView.model
            return mpvqcCommentTypeValidatorPyObject.validate_editing_of_comment_type(input, inputBeingEdited, items)
        }

        onAdded: (commentType) => {
            _controller.add(commentType)
        }

        onEdited: (commentType) => {
            const english = root.mpvqcUtilityPyObject.reverseLookupCommentType(commentType)
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
            downEnabled: controlsEnabled && _listView.currentIndex !== _listView.model.length - 1
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
