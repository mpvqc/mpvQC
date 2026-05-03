// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import io.github.mpvqc.mpvQC.Dialogs
import io.github.mpvqc.mpvQC.FileDialogs
import io.github.mpvqc.mpvQC.MessageBoxes
import io.github.mpvqc.mpvQC.Python

Item {
    id: root

    required property MpvqcMenuBarViewModel viewModel

    signal focusWanted
    signal closeAppRequested
    signal resizeVideoRequested

    MpvqcDialogLoader {
        id: _dialogLoader

        onDialogClosed: root.focusWanted()
    }

    MpvqcFileDialogLoader {
        id: _fileDialogLoader

        onDialogClosed: root.focusWanted()
    }

    MpvqcMessageBoxLoader {
        id: _messageBoxLoader

        onMessageBoxClosed: root.focusWanted()
    }

    Connections {
        target: root.viewModel

        function onConfirmResetRequested(): void {
            _messageBoxLoader.openResetMessageBox();
        }

        function onOpenQcDocumentsRequested(): void {
            _fileDialogLoader.openImportQcDocumentsDialog();
        }

        function onExportPathRequested(): void {
            _fileDialogLoader.openDocumentSaveDialog();
        }

        function onExtendedExportRequested(template: url): void {
            _fileDialogLoader.openExtendedDocumentExportDialog(template);
        }

        function onCloseAppRequested(): void {
            root.closeAppRequested();
        }

        function onOpenVideoRequested(): void {
            _fileDialogLoader.openImportVideoDialog();
        }

        function onOpenSubtitlesRequested(): void {
            _fileDialogLoader.openImportSubtitlesDialog();
        }

        function onResizeVideoRequested(): void {
            root.resizeVideoRequested();
        }

        function onAppearanceDialogRequested(): void {
            _dialogLoader.openAppearanceDialog();
        }

        function onCommentTypesDialogRequested(): void {
            _dialogLoader.openCommentTypesDialog();
        }

        function onBackupSettingsDialogRequested(): void {
            _dialogLoader.openBackupSettingsDialog();
        }

        function onExportSettingsDialogRequested(): void {
            _dialogLoader.openExportSettingsDialog();
        }

        function onImportSettingsDialogRequested(): void {
            _dialogLoader.openImportSettingsDialog();
        }

        function onEditMpvConfigDialogRequested(): void {
            _dialogLoader.openEditMpvDialog();
        }

        function onEditInputConfigDialogRequested(): void {
            _dialogLoader.openEditInputDialog();
        }

        function onKeyboardShortcutsDialogRequested(): void {
            _dialogLoader.openShortcutsDialog();
        }

        function onAboutDialogRequested(): void {
            _dialogLoader.openAboutDialog();
        }

        function onUpdateDialogRequested(): void {
            _messageBoxLoader.openVersionCheckMessageBox();
        }

        function onExtendedExportDialogRequested(): void {
            _messageBoxLoader.openExtendedExportsMessageBox();
        }
    }
}
