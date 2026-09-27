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

    width: Math.min(contentWidth + leftPadding + rightPadding, Math.max(0, (Overlay.overlay?.width ?? 0) - 2 * margins))
    contentWidth: MpvqcConstants.smallDialogContentWidth
    contentHeight: MpvqcConstants.mediumDialogContentHeight
    margins: MpvqcConstants.dialogEdgeMargin
    title: qsTranslate("CommentTypesDialog", "Comment Types")
    standardButtons: Dialog.RestoreDefaults | Dialog.Cancel | Dialog.Ok

    contentItem: ColumnLayout {
        spacing: MpvqcConstants.dialogSectionSpacing

        MpvqcSectionCard {
            objectName: "commentTypesAddCard"

            title: qsTranslate("CommentTypesDialog", "Add Comment Type")

            Layout.fillWidth: true
            Layout.topMargin: MpvqcConstants.dialogContentTopMargin

            MpvqcCommentTypesDraftField {
                id: _draftField

                validationError: _viewState.validationError
                addEnabled: _viewState.isAddEnabled

                Layout.fillWidth: true

                onAddRequested: _viewState.addType()
            }
        }

        MpvqcSectionCard {
            objectName: "commentTypesListCard"

            Layout.fillWidth: true

            MpvqcCommentTypesListView {
                id: _listView

                applyMove: (from, to) => root.viewModel.move(from, to)

                Layout.fillWidth: true
                Layout.preferredHeight: 8 * MpvqcConstants.listRowHeight

                onDeleteRequested: index => _viewState.removeType(index)

                Component.onCompleted: commentTypes = root.viewModel.commentTypesModel
            }
        }

        Item {
            Layout.fillHeight: true
        }
    }

    onAboutToHide: _listView.cancelReorder()
    onAccepted: root.viewModel.save()
    onReset: {
        if (_viewState.canEdit) {
            root.viewModel.resetToDefaults();
        }
    }

    QtObject {
        id: _viewState

        readonly property string validationError: _draftField.text === "" ? "" : root.viewModel.validateNew(_draftField.text)
        readonly property bool isAddEnabled: _draftField.text !== "" && validationError === ""
        readonly property bool canEdit: !_listView.reordering

        function removeType(index: int): void {
            if (canEdit) {
                root.viewModel.remove(index);
            }
        }

        function addType(): void {
            if (!isAddEnabled || !canEdit) {
                return;
            }
            const index = root.viewModel.append(_draftField.text);
            _listView.positionViewAtIndex(index, ListView.Contain);
            _draftField.clear();
            _draftField.focusInput();
        }
    }
}
