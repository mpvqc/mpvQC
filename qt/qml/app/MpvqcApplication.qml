// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

import pyobjects

import "../views"
import "../manager"
import "../themes"

ApplicationWindow {
    id: root

    readonly property var mpvqcMpvPlayerPropertiesPyObject: MpvqcMpvPlayerPropertiesPyObject {}
    readonly property var mpvqcMpvPlayerPyObject: MpvqcMpvPlayerPyObject {}
    readonly property var mpvqcUtilityPyObject: MpvqcUtilityPyObject {}

    readonly property var mpvqcLabelWidthCalculator: MpvqcLabelWidthCalculator
    readonly property var mpvqcSettings: MpvqcSettings
    readonly property var mpvqcTheme: MpvqcTheme

    readonly property var mpvqcManager: MpvqcManager {}

    readonly property bool maximized: _windowVisibilityHandler.maximized
    readonly property bool fullscreen: _windowVisibilityHandler.fullscreen
    readonly property int windowBorder: root.fullscreen || root.maximized ? 0 : 1

    readonly property int windowsFlags: Qt.CustomizeWindowHint | Qt.Window
    readonly property int linuxFlags: Qt.FramelessWindowHint | Qt.Window

    flags: Qt.platform.os === "windows" ? windowsFlags : linuxFlags

    width: 1280
    height: 720

    minimumWidth: 960
    minimumHeight: 540

    visible: true
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

    onClosing: event => {
        _quitHandler.requestClose();
        event.accepted = _quitHandler.userConfirmedClose;
    }

    MpvqcContent {
        id: _content

        mpvqcApplication: root
        headerController: _headerController
        contentController: _contentController

        focus: true
        anchors.fill: parent
        anchors.margins: root.windowBorder

        header: MpvqcAppHeaderView {
            controller: _headerController
            width: root.width
        }
    }

    MpvqcContentDialogLoader {
        id: _dialogLoader

        isLayoutMirroringEnabled: Application.layoutDirection === Qt.RightToLeft

        onDialogClosed: _content.focusCommentTable()
    }

    MpvqcContentFileDialogLoader {
        id: _fileDialogLoader

        onDialogClosed: _content.focusCommentTable()
    }

    MpvqcContentMessageBoxLoader {
        id: _messageBoxLoader

        onMessageBoxClosed: _content.focusCommentTable()
    }

    MouseArea {
        anchors.fill: parent
        cursorShape: undefined
        propagateComposedEvents: true

        onPressed: event => {
            // *********************************************************
            // fixme: Workaround QTBUG-131786 to fake modal behavior on Windows
            event.accepted = !!root.nativePopupOpen;
            // *********************************************************

            // event.accepted = false;
            _content.focusCommentTable();
        }
    }

    MpvqcAppHeaderViewController {
        id: _headerController

        mpvqcTheme: root.mpvqcTheme
        mpvqcSettings: root.mpvqcSettings

        isVisible: !root.fullscreen
        isMaximized: root.maximized
        isStateSaved: root.mpvqcManager.saved
        isVideoLoaded: root.mpvqcMpvPlayerPropertiesPyObject.video_loaded
        isDebugEnabled: root.mpvqcUtilityPyObject.getEnvironmentVariable("MPVQC_DEBUG")

        applicationLayout: root.mpvqcSettings.layoutOrientation
        windowTitleFormat: root.mpvqcSettings.windowTitleFormat

        playerVideoName: root.mpvqcMpvPlayerPropertiesPyObject.filename
        playerVideoPath: root.mpvqcMpvPlayerPropertiesPyObject.path

        extendedExportTemplatesModel: MpvqcExportTemplateModel {}

        onConfirmResetRequested: _messageBoxLoader.openResetMessageBox()

        onOpenQcDocumentsRequested: _fileDialogLoader.openImportQcDocumentsDialog()

        onSaveQcDocumentsRequested: root.mpvqcManager.save()

        onSaveQcDocumentsAsRequested: root.mpvqcManager.saveAs()

        onExtendedExportRequested: exportTemplate => _fileDialogLoader.openExtendedDocumentExportDialog(exportTemplate)

        onOpenVideoRequested: _fileDialogLoader.openImportVideoDialog()

        onOpenSubtitlesRequested: _fileDialogLoader.openImportSubtitlesDialog()

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

        onWindowDragRequested: root.startSystemMove()

        onMinimizeAppRequested: root.showMinimized()

        onToggleMaximizeAppRequested: _windowVisibilityHandler.toggleMaximized()

        onCloseAppRequested: root.close()
    }

    MpvqcContentController {
        id: _contentController

        mpvqcMpvPlayerPyObject: root.mpvqcMpvPlayerPyObject
        mpvqcManager: root.mpvqcManager
        mpvqcSettings: root.mpvqcSettings

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

        mpvqcApplication: root
    }

    MpvqcQuitHandler {
        id: _quitHandler

        mpvqcApplication: root
        canClose: root.mpvqcManager.saved
    }

    Component.onCompleted: _content.focusCommentTable()

    // *********************************************************
    // fixme: Workaround QTBUG-131786 to fake modal behavior on Windows
    property bool nativePopupOpen: false
    property Timer modalFaker: Timer {
        interval: 100
        onTriggered: {
            root.nativePopupOpen = false;
        }
    }

    function enableFakeModal(): void {
        if (Qt.platform.os === "windows") {
            modalFaker.stop();
            root.nativePopupOpen = true;
        }
    }

    function disableFakeModal(): void {
        if (Qt.platform.os === "windows") {
            modalFaker.restart();
        }
    }

    // *********************************************************
}
