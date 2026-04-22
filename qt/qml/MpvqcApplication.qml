// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

import pyobjects

import "dialogs"
import "filedialogs"
import "messageboxes"
import "utility"
import "views/header"
import "views/main"

ApplicationWindow {
    id: root

    readonly property MpvqcApplicationViewModel viewModel: MpvqcApplicationViewModel {}

    readonly property bool isWindows: Qt.platform.os === "windows"
    readonly property int windowsFlags: Qt.CustomizeWindowHint | Qt.Window
    readonly property int linuxFlags: Qt.FramelessWindowHint | Qt.Window

    property bool _initialFocusDone: false

    objectName: "MpvqcMainWindow"
    flags: isWindows ? windowsFlags : linuxFlags

    width: 1280
    height: 720

    minimumWidth: 960
    minimumHeight: 540

    visible: false
    color: Material.background

    font {
        pointSize: 10
        family: 'Noto Sans'
    }

    Material.theme: MpvqcTheme.isDark ? Material.Dark : Material.Light
    Material.accent: MpvqcTheme.control
    Material.background: MpvqcTheme.background
    Material.foreground: MpvqcTheme.foreground

    LayoutMirroring.enabled: Application.layoutDirection === Qt.RightToLeft
    LayoutMirroring.childrenInherit: true

    Component.onCompleted: root.requestActivate()

    onActiveChanged: {
        if (active && !_initialFocusDone) {
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
            width: root.width
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

        onWindowDragRequested: root.startSystemMove()

        onMinimizeAppRequested: root.showMinimized()

        onToggleMaximizeAppRequested: _windowVisibilityHandler.toggleMaximized()

        onCloseAppRequested: root.close()
    }

    MpvqcMenuBarViewModel {
        id: _menuBarViewModel

        onConfirmResetRequested: _messageBoxLoader.openResetMessageBox()

        onOpenQcDocumentsRequested: _fileDialogLoader.openImportQcDocumentsDialog()

        onExportPathRequested: _fileDialogLoader.openDocumentSaveDialog()

        onExtendedExportRequested: exportTemplate => _fileDialogLoader.openExtendedDocumentExportDialog(exportTemplate)

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

        onCloseAppRequested: root.close()
    }

    MpvqcContentViewModel {
        id: _contentViewModel

        onAppWindowSizeRequested: (width, height) => {
            if (width >= root.minimumWidth && height >= root.minimumHeight) {
                root.width = width;
                root.height = height;
            }
        }

        onDisableFullScreenRequested: _windowVisibilityHandler.disableFullScreen()

        onToggleFullScreenRequested: _windowVisibilityHandler.toggleFullScreen()
    }

    MpvqcWindowVisibilityHandler {
        id: _windowVisibilityHandler
    }
}
