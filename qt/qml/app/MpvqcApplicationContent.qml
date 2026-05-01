// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import pyobjects

import "../dialogs"
import "../filedialogs"
import "../messageboxes"
import "../views/header"
import "../views/player"

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
            _layout.focusCommentTable();
        }
    }

    Keys.onEscapePressed: root.disableFullScreenRequested()
    Keys.onPressed: event => _keyHandler.handleKeyPress(event)

    MpvqcHeaderViewModel {
        id: _headerViewModel
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
        onResizeVideoRequested: _layout.recalculateSizes()

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
    }

    MpvqcHeaderView {
        id: _header

        viewModel: _headerViewModel
        menuBarViewModel: _menuBarViewModel
        width: root.windowWidth

        onWindowDragRequested: root.startSystemMoveRequested()
        onMinimizeRequested: root.minimizeRequested()
        onToggleMaximizeRequested: root.toggleMaximizeRequested()
        onCloseRequested: root.closeRequested()
    }

    MpvqcLayout {
        id: _layout

        focus: true
        anchors.fill: parent
        anchors.margins: root.viewModel.windowBorder

        header: _header
        layoutOrientation: _contentViewModel.layoutOrientation
        windowBorder: root.viewModel.windowBorder
        headerHeight: _header.height

        onAppWindowSizeRequested: (width, height) => root.appWindowSizeRequested(width, height)
        onToggleFullScreenRequested: root.toggleFullScreenRequested()
        onAddNewCommentMenuRequested: _commentMenu.popup()
    }

    MpvqcFileDropArea {
        anchors.fill: _layout
    }

    MpvqcNewCommentMenu {
        id: _commentMenu

        onCommentTypeChosen: commentType => {
            root.disableFullScreenRequested();
            _layout.addComment(commentType);
        }
    }

    MpvqcNewCommentMenuClickGuard {
        menu: _commentMenu
    }

    MouseArea {
        anchors.fill: parent
        cursorShape: undefined
        propagateComposedEvents: true

        onPressed: event => {
            event.accepted = false;
            _layout.focusCommentTable();
        }
    }

    MpvqcDialogLoader {
        id: _dialogLoader

        onDialogClosed: _layout.focusCommentTable()
    }

    MpvqcFileDialogLoader {
        id: _fileDialogLoader

        onDialogClosed: _layout.focusCommentTable()
    }

    MpvqcMessageBoxLoader {
        id: _messageBoxLoader

        onMessageBoxClosed: _layout.focusCommentTable()
    }

    MpvqcContentKeyHandler {
        id: _keyHandler

        onOpenCommentMenuRequested: _commentMenu.popup()
        onToggleFullScreenRequested: root.toggleFullScreenRequested()
        onForwardKeyToPlayerRequested: (key, modifiers) => _contentViewModel.forwardKeyToPlayer(key, modifiers)
    }
}
