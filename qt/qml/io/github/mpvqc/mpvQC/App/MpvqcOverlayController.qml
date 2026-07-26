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

        onClosed: root.focusWanted()
    }

    MpvqcMessageBoxLoader {
        id: _messageBoxLoader

        onClosed: root.focusWanted()
    }

    MpvqcMessageBoxRequestRelayViewModel {
        onExportErrorOccurred: (message, line) => _messageBoxLoader.openExportErrorMessageBox(message, line)

        onConfirmQuit: _messageBoxLoader.openMessageBox(MpvqcMessageBoxKind.MessageBoxKind.QUIT)
    }

    Connections {
        target: root.viewModel

        function onConfirmResetRequested(): void {
            _messageBoxLoader.openMessageBox(MpvqcMessageBoxKind.MessageBoxKind.RESET);
        }

        function onFileDialogRequested(kind: int): void {
            _fileDialogLoader.openFileDialog(kind);
        }

        function onCustomExportRequested(template: url): void {
            _fileDialogLoader.openCustomExportFileDialog(template);
        }

        function onCloseAppRequested(): void {
            root.closeAppRequested();
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

        function onMessageBoxRequested(kind: int): void {
            _messageBoxLoader.openMessageBox(kind);
        }
    }
}
