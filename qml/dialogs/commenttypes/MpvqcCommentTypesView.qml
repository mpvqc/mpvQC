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

    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    readonly property var mpvqcUtilityPyObject: mpvqcApplication.mpvqcUtilityPyObject
    readonly property var mpvqcCommentTypeValidatorPyObject: mpvqcApplication.mpvqcCommentTypeValidatorPyObject

    function acceptTemporaryState(): void {
        _controller.acceptModelCopy();
        mpvqcSettings.commentTypesChanged();
    }

    function resetTemporaryEdits(): void {
        _input.stopEditing();
        _controller.reset();
    }

    MpvqcCommentTypesViewController {
        id: _controller

        model: root.mpvqcSettings.commentTypes
        selectedIndex: _listView.currentIndex

        onHighlightIndexRequested: index => {
            _listView.currentIndex = index;
        }

        onEditClicked: commentType => {
            const translated = qsTranslate("CommentTypes", commentType);
            _input.startEditing(translated);
        }

        onAcceptCopyRequested: copy => {
            const newCommentTypes = copy.length === 0 ? root.mpvqcSettings.getDefaultCommentTypes() : copy;

            root.mpvqcSettings.commentTypes.length = 0;
            root.mpvqcSettings.commentTypes.push(...newCommentTypes);
        }

        onResetRequested: {
            _controller.model.length = 0;
            _controller.model.push(...root.mpvqcSettings.getDefaultCommentTypes());
        }
    }

    MpvqcInputComponent {
        id: _input

        mpvqcApplication: root.mpvqcApplication

        width: root.width
        height: 100
        topPadding: 15

        validateNewCommentType: input => {
            const items = _listView.model;
            return root.mpvqcCommentTypeValidatorPyObject.validate_new_comment_type(input, items);
        }

        validateEditingOfCommentType: (input, inputBeingEdited) => {
            const items = _listView.model;
            return root.mpvqcCommentTypeValidatorPyObject.validate_editing_of_comment_type(input, inputBeingEdited, items);
        }

        onAdded: commentType => {
            _listView.disableMovingHighlightRectangle();
            _controller.add(commentType);
            _listView.enableMovingHighlightRectangle();
        }

        onEdited: commentType => {
            _listView.disableMovingHighlightRectangle();
            const currentIndex = _listView.currentIndex;
            const english = root.mpvqcUtilityPyObject.reverseLookupCommentType(commentType);
            _controller.replaceWith(english);
            _listView.currentIndex = currentIndex;
            _listView.enableMovingHighlightRectangle();
        }
    }

    RowLayout {
        width: root.width

        MpvqcList {
            id: _listView

            mpvqcApplication: root.mpvqcApplication

            itemHeight: _listViewControls.buttonHeight
            model: _controller.modelCopy
            enabled: !_input.editing
            implicitHeight: 7 * itemHeight

            Layout.fillWidth: true
        }

        MpvqcListControls {
            id: _listViewControls

            readonly property bool controlsEnabled: !_input.textFieldHasFocus && _listView.enabled

            implicitHeight: _listView.height
            upEnabled: controlsEnabled && _listView.currentIndex > 0
            downEnabled: controlsEnabled && _listView.currentIndex !== _listView.model.length - 1
            editEnabled: controlsEnabled && _listView.currentIndex >= 0
            deleteEnabled: controlsEnabled && _listView.currentIndex >= 0

            onUpClicked: {
                _listView.disableMovingHighlightRectangle();
                _controller.moveUp();
                _listView.enableMovingHighlightRectangle();
            }

            onDownClicked: {
                _listView.disableMovingHighlightRectangle();
                _controller.moveDown();
                _listView.enableMovingHighlightRectangle();
            }

            onEditClicked: {
                _controller.startEditing();
            }

            onDeleteClicked: {
                _listView.disableMovingHighlightRectangle();
                _controller.deleteItem();
                _listView.enableMovingHighlightRectangle();
            }
        }
    }
}
