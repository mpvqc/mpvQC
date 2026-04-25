// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import pyobjects

import "dialogs"
import "filedialogs"
import "messageboxes"
import "views/header"
import "views/main"

Item {
    id: root

    readonly property MpvqcApplicationViewModel viewModel: MpvqcApplicationViewModel {}

    required property bool windowActive
    required property real windowWidth

    property bool _initialFocusDone: false

    signal closeRequested
    signal minimizeRequested
    signal toggleMaximizeRequested
    signal startSystemMoveRequested
    signal toggleFullScreenRequested
    signal disableFullScreenRequested
    signal appWindowSizeRequested(width: int, height: int)

    onWindowActiveChanged: {
        if (windowActive && !_initialFocusDone) {
            _initialFocusDone = true;
            _content.focusCommentTable();
        }
    }

    MpvqcContentView {
        id: _content

        viewModel: _contentViewModel
        windowBorder: root.viewModel.windowBorder

        focus: true
        anchors.fill: parent
        anchors.margins: windowBorder

        header: MpvqcHeaderView {
            viewModel: _headerViewModel
            menuBarViewModel: _menuBarViewModel
            width: root.windowWidth
        }
    }

    MpvqcDialogLoader {
        id: _dialogLoader

        onDialogClosed: _content.focusCommentTable()
    }

    MpvqcFileDialogLoader {
        id: _fileDialogLoader

        onDialogClosed: _content.focusCommentTable()
    }

    MpvqcMessageBoxLoader {
        id: _messageBoxLoader

        onMessageBoxClosed: _content.focusCommentTable()
    }

    MouseArea {
        anchors.fill: parent
        cursorShape: undefined
        propagateComposedEvents: true

        onPressed: event => {
            event.accepted = false;
            _content.focusCommentTable();
        }
    }

    MpvqcHeaderViewModel {
        id: _headerViewModel

        onWindowDragRequested: root.startSystemMoveRequested()
        onMinimizeAppRequested: root.minimizeRequested()
        onToggleMaximizeAppRequested: root.toggleMaximizeRequested()
        onCloseAppRequested: root.closeRequested()
    }

    MpvqcMenuBarViewModel {
        id: _menuBarViewModel

        onConfirmResetRequested: _messageBoxLoader.openResetMessageBox()
        onOpenQcDocumentsRequested: _fileDialogLoader.openImportQcDocumentsDialog()
        onExportPathRequested: _fileDialogLoader.openDocumentSaveDialog()
        onExtendedExportRequested: exportTemplate => _fileDialogLoader.openExtendedDocumentExportDialog(exportTemplate)
        onCloseAppRequested: root.closeRequested()

        onOpenVideoRequested: _fileDialogLoader.openImportVideoDialog()
        onOpenSubtitlesRequested: _fileDialogLoader.openImportSubtitlesDialog()
        onResizeVideoRequested: _content.resizeVideo()

        onAppearanceDialogRequested: _dialogLoader.openAppearanceDialog()
        onCommentTypesDialogRequested: _dialogLoader.openCommentTypesDialog()
        onBackupSettingsDialogRequested: _dialogLoader.openBackupSettingsDialog()
        onExportSettingsDialogRequested: _dialogLoader.openExportSettingsDialog()
        onImportSettingsDialogRequested: _dialogLoader.openImportSettingsDialog()
        onEditMpvConfigDialogRequested: _dialogLoader.openEditMpvDialog()
        onEditInputConfigDialogRequested: _dialogLoader.openEditInputDialog()

        onKeyboardShortcutsDialogRequested: _dialogLoader.openShortcutsDialog()
        onAboutDialogRequested: _dialogLoader.openAboutDialog()
        onUpdateDialogRequested: _messageBoxLoader.openVersionCheckMessageBox()
        onExtendedExportDialogRequested: _messageBoxLoader.openExtendedExportsMessageBox()
    }

    MpvqcContentViewModel {
        id: _contentViewModel

        onAppWindowSizeRequested: (width, height) => root.appWindowSizeRequested(width, height)
        onDisableFullScreenRequested: root.disableFullScreenRequested()
        onToggleFullScreenRequested: root.toggleFullScreenRequested()
    }
}
