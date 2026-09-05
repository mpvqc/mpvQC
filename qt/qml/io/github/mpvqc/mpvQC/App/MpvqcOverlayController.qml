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

    required property MpvqcShellMenuBarViewModel viewModel

    signal focusWanted

    function openDialog(kind: int): void {
        _dialogLoader.openDialog(kind);
    }

    function openFileDialog(kind: int): void {
        _fileDialogLoader.openFileDialog(kind);
    }

    function openCustomExportFileDialog(template: url): void {
        _fileDialogLoader.openCustomExportFileDialog(template);
    }

    function openMessageBox(kind: int): void {
        _messageBoxLoader.openMessageBox(kind);
    }

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

    Connections {
        target: root.viewModel

        function onFileDialogRequested(kind: int): void {
            root.openFileDialog(kind);
        }

        function onMessageBoxRequested(kind: int): void {
            root.openMessageBox(kind);
        }

        function onExportErrorMessageBoxRequested(message: string, line: int): void {
            _messageBoxLoader.openExportErrorMessageBox(message, line);
        }
    }
}
