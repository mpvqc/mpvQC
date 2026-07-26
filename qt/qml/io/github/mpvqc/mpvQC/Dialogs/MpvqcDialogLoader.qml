// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Python

MpvqcOverlayLoader {
    id: root
    objectName: "dialogLoader"

    readonly property var _urlsByKind: ({
            [MpvqcDialogKind.DialogKind.ABOUT]: Qt.resolvedUrl("About/MpvqcAboutDialog.qml"),
            [MpvqcDialogKind.DialogKind.APPEARANCE]: Qt.resolvedUrl("MpvqcAppearanceDialog.qml"),
            [MpvqcDialogKind.DialogKind.BACKUP_SETTINGS]: Qt.resolvedUrl("MpvqcBackupDialog.qml"),
            [MpvqcDialogKind.DialogKind.COMMENT_TYPES]: Qt.resolvedUrl("CommentTypes/MpvqcCommentTypesDialog.qml"),
            [MpvqcDialogKind.DialogKind.EDIT_INPUT_CONFIG]: Qt.resolvedUrl("MpvqcEditInputDialog.qml"),
            [MpvqcDialogKind.DialogKind.EDIT_MPV_CONFIG]: Qt.resolvedUrl("MpvqcEditMpvDialog.qml"),
            [MpvqcDialogKind.DialogKind.EXPORT_SETTINGS]: Qt.resolvedUrl("MpvqcExportSettingsDialog.qml"),
            [MpvqcDialogKind.DialogKind.IMPORT_SETTINGS]: Qt.resolvedUrl("MpvqcImportSettingsDialog.qml"),
            [MpvqcDialogKind.DialogKind.IMPORT_WIZARD]: Qt.resolvedUrl("ImportWizard/MpvqcImportWizardDialog.qml"),
            [MpvqcDialogKind.DialogKind.KEYBOARD_SHORTCUTS]: Qt.resolvedUrl("Shortcuts/MpvqcShortcutDialog.qml")
        })

    function openDialog(kind: int): void {
        root.open(root._urlsByKind[kind]);
    }

    function openImportWizardDialog(viewModel: MpvqcImportWizardViewModel): void {
        root.open(root._urlsByKind[MpvqcDialogKind.DialogKind.IMPORT_WIZARD], {
            viewModel: viewModel
        });
    }
}
