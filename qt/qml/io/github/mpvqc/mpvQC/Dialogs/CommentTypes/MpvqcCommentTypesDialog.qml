// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

MpvqcDialog {
    id: root
    objectName: "commentTypesDialog"

    readonly property MpvqcCommentTypesDialogViewModel viewModel: MpvqcCommentTypesDialogViewModel {}

    contentHeight: MpvqcConstants.smallDialogContentHeight

    title: qsTranslate("CommentTypesDialog", "Comment Types")
    standardButtons: Dialog.Ok | Dialog.Cancel | Dialog.Reset

    onAboutToShow: {
        // trigger the populate animation
        _listView.model = root.viewModel.commentTypesModel;
    }

    onAccepted: {
        root.viewModel.save();
    }

    onReset: {
        root.viewModel.resetToDefaults();
        _listView.currentIndex = 0;
    }

    QtObject {
        id: _viewState

        readonly property string validationError: _draftField.text === "" ? "" : root.viewModel.validateNew(_draftField.text)
        readonly property bool isAddEnabled: _draftField.text !== "" && validationError === ""
        readonly property bool isMoveUpEnabled: _listView.currentIndex > 0
        readonly property bool isMoveDownEnabled: _listView.currentIndex >= 0 && _listView.currentIndex < _listView.count - 1
        readonly property bool isDeleteEnabled: _listView.currentIndex >= 0 && _listView.count > 1

        function addType(): void {
            if (!isAddEnabled) {
                return;
            }
            _listView.currentIndex = root.viewModel.append(_draftField.text);
            _listView.ensureVisible(0);
            _draftField.clear();
            _draftField.focusInput();
        }

        function deleteCurrent(): void {
            _listView.positionViewAtIndex(_listView.currentIndex, ListView.Contain);
            _listView.beginRemoval();
            root.viewModel.remove(_listView.currentIndex);
        }

        function moveUp(): void {
            const idx = _listView.currentIndex;
            root.viewModel.move(idx, idx - 1);
            _listView.currentIndex = idx - 1;
            _listView.ensureVisible(+1);
        }

        function moveDown(): void {
            const idx = _listView.currentIndex;
            root.viewModel.move(idx, idx + 1);
            _listView.currentIndex = idx + 1;
            _listView.ensureVisible(-1);
        }
    }

    contentItem: ColumnLayout {
        spacing: 10

        MpvqcCommentTypesDraftField {
            id: _draftField

            Layout.fillWidth: true
            Layout.topMargin: 20

            validationError: _viewState.validationError
            addEnabled: _viewState.isAddEnabled

            onAddRequested: _viewState.addType()
        }

        RowLayout {
            Layout.fillHeight: true
            Layout.fillWidth: true

            MpvqcCommentTypesListView {
                id: _listView

                Layout.fillWidth: true
                Layout.fillHeight: true

                rowHeight: 44
            }

            MpvqcCommentTypesActions {
                id: _actions

                Layout.alignment: Qt.AlignTop

                moveUpEnabled: _viewState.isMoveUpEnabled
                moveDownEnabled: _viewState.isMoveDownEnabled
                deleteEnabled: _viewState.isDeleteEnabled

                onMoveUpRequested: _viewState.moveUp()
                onMoveDownRequested: _viewState.moveDown()
                onDeleteRequested: _viewState.deleteCurrent()
            }
        }
    }
}
