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

    // Three loaders, never one: an export error opens a message box while the
    // file dialog tears down, and an UnfinishedPlan opens the wizard while
    // that teardown is pending. Sharing would drop the second overlay.
    MpvqcDialogLoader {
        id: _dialogLoader

        onClosed: {
            root.focusWanted();
            _importWizardRelay.releaseWizardViewModel();
        }
    }

    MpvqcFileDialogLoader {
        id: _fileDialogLoader

        onClosed: root.focusWanted()
    }

    MpvqcMessageBoxLoader {
        id: _messageBoxLoader

        onClosed: root.focusWanted()
    }

    MpvqcImportWizardRequestRelayViewModel {
        id: _importWizardRelay

        onImportWizardRequested: viewModel => _dialogLoader.openImportWizardDialog(viewModel)
    }

    MpvqcMessageBoxRequestRelayViewModel {
        onExportErrorOccurred: (message, line) => _messageBoxLoader.openExportErrorMessageBox(message, line)

        onQuitConfirmationNeeded: _messageBoxLoader.openMessageBox(MpvqcMessageBoxKind.MessageBoxKind.QUIT)
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

        function onDialogRequested(kind: int): void {
            _dialogLoader.openDialog(kind);
        }

        function onMessageBoxRequested(kind: int): void {
            _messageBoxLoader.openMessageBox(kind);
        }
    }
}
