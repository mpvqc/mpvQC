/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

import QtQuick
import QtQuick.Controls.Material

import pyobjects

import "../settings"
import "../header2"

ApplicationWindow {
    id: root

    readonly property var mpvqcLabelWidthCalculator: MpvqcLabelWidthCalculator { mpvqcApplication: root }
    readonly property var mpvqcSettings: MpvqcSettings { mpvqcApplication: root }
    readonly property var mpvqcWindowVisibilityHandler: MpvqcWindowVisibilityHandler { mpvqcApplication: root }

    readonly property var mpvqcManager: MpvqcManager {
        mpvqcApplication: root
        commentCount: _content.commentCount
    }

    readonly property var mpvqcTheme: MpvqcTheme {
        themeIdentifier: root.mpvqcSettings.themeIdentifier
        themeColorOption: root.mpvqcSettings.themeColorOption
    }

    readonly property var mpvqcApplicationPathsPyObject: MpvqcApplicationPathsPyObject {}
    readonly property var mpvqcCommentTypeValidatorPyObject: MpvqcCommentTypeValidatorPyObject {}
    readonly property var mpvqcDefaultTextValidatorPyObject: MpvqcDefaultTextValidatorPyObject {}
    readonly property var mpvqcExtendedDocumentExporterPyObject: MpvqcExtendedDocumentExporterPyObject {}
    readonly property var mpvqcMpvPlayerPropertiesPyObject: MpvqcMpvPlayerPropertiesPyObject {}
    readonly property var mpvqcMpvPlayerPyObject: MpvqcMpvPlayerPyObject {}
    readonly property var mpvqcPlayerFilesPyObject: MpvqcPlayerFilesPyObject {}
    readonly property var mpvqcUtilityPyObject: MpvqcUtilityPyObject {}
    readonly property var mpvqcVersionCheckerPyObject: MpvqcVersionCheckerPyObject {}

    readonly property bool maximized: mpvqcWindowVisibilityHandler.maximized
    readonly property bool fullscreen: mpvqcWindowVisibilityHandler.fullscreen
    readonly property int windowBorder: root.fullscreen || root.maximized ? 0 : 1

    function toggleMaximized(): void {
        mpvqcWindowVisibilityHandler.toggleMaximized();
    }

    function toggleFullScreen(): void {
        mpvqcWindowVisibilityHandler.toggleFullScreen();
    }

    function enableFullScreen(): void {
        mpvqcWindowVisibilityHandler.enableFullScreen();
    }

    function disableFullScreen(): void {
        mpvqcWindowVisibilityHandler.disableFullScreen();
    }

    width: 1280
    height: 720

    minimumWidth: 960
    minimumHeight: 540

    font {
        pointSize: 10
        family: 'Noto Sans'
    }

    flags: Qt.FramelessWindowHint | Qt.Window
    color: Material.background
    visible: true

    Material.theme: root.mpvqcTheme.isDark ? Material.Dark : Material.Light
    Material.accent: root.mpvqcTheme.control

    Material.background: root.mpvqcTheme.background
    Material.foreground: root.mpvqcTheme.foreground

    LayoutMirroring.enabled: Application.layoutDirection === Qt.RightToLeft
    LayoutMirroring.childrenInherit: true

    onClosing: event => {
        closeHandler.requestClose();
        event.accepted = closeHandler.userConfirmedClose;
    }

    MpvqcContent {
        id: _content

        mpvqcApplication: root
        focus: true
        anchors.fill: parent
        anchors.margins: root.windowBorder

        readonly property var mpvqcAppHeaderController: MpvqcAppHeaderController {
            mpvqcTheme: root.mpvqcTheme

            isVisible: !root.fullscreen
            isMaximized: root.maximized
            isStateSaved: root.mpvqcManager.saved
            isVideoLoaded: root.mpvqcMpvPlayerPropertiesPyObject.video_loaded
            isDebugEnabled: root.mpvqcUtilityPyObject.getEnvironmentVariable("MPVQC_DEBUG")

            applicationLayout: root.mpvqcSettings.layoutOrientation
            windowTitleFormat: root.mpvqcSettings.windowTitleFormat

            playerVideoName: root.mpvqcMpvPlayerPropertiesPyObject.filename
            playerVideoPath: root.mpvqcMpvPlayerPropertiesPyObject.path

            extendedExportTemplatesModel: MpvqcExportTemplateModelPyObject {} // qmllint disable

            onResetAppStateRequested: {
                console.log("TODO: onResetAppStateRequested");
            }

            onOpenQcDocumentsRequested: {
                console.log("TODO: onOpenQcDocumentsRequested");
            }

            onSaveQcDocumentsRequested: {
                console.log("TODO: onSaveQcDocumentsRequested");
            }

            onSaveQcDocumentsAsRequested: {
                console.log("TODO: onSaveQcDocumentsAsRequested");
            }

            onExtendedExportRequested: (name, path) => {
                console.log("TODO: onExtendedExportRequested", name, path);
            }

            onOpenVideoRequested: {
                console.log("TODO: onOpenVideoRequested");
            }

            onOpenSubtitlesRequested: {
                console.log("TODO: onOpenSubtitlesRequested");
            }

            onResizeVideoRequested: {
                console.log("TODO: onResizeVideoRequested");
            }

            onAppearanceDialogRequested: {
                console.log("TODO: onAppearanceDialogRequested");
            }

            onCommentTypesDialogRequested: {
                console.log("TODO: onCommentTypesDialogRequested");
            }

            onWindowTitleFormatConfigured: updatedValue => {
                root.mpvqcSettings.windowTitleFormat = updatedValue;
            }

            onApplicationLayoutConfigured: updatedValue => {
                root.mpvqcSettings.layoutOrientation = updatedValue;
            }

            onBackupSettingsDialogRequested: {
                console.log("TODO: onBackupSettingsDialogRequested");
            }

            onExportSettingsDialogRequested: {
                console.log("TODO: onExportSettingsDialogRequested");
            }

            onImportSettingsDialogRequested: {
                console.log("TODO: onImportSettingsDialogRequested");
            }

            onEditMpvConfigDialogRequested: {
                console.log("TODO: onEditMpvConfigDialogRequested");
            }

            onEditInputConfigDialogRequested: {
                console.log("TODO: onEditInputConfigDialogRequested");
            }

            onLanguageConfigured: updatedLanguageIdentifier => {
                root.mpvqcSettings.language = updatedLanguageIdentifier;
            }

            onUpdateDialogRequested: {
                console.log("TODO: onUpdateDialogRequested");
            }

            onKeyboardShortcutsDialogRequested: {
                console.log("TODO: onKeyboardShortcutsDialogRequested");
            }

            onExtendedExportDialogRequested: {
                console.log("TODO: onExtendedExportDialogRequested");
            }

            onAboutDialogRequested: {
                console.log("TODO: onAboutDialogRequested");
            }

            onWindowDragRequested: {
                root.startSystemMove();
            }

            onMinimizeAppRequested: {
                root.showMinimized();
            }

            onToggleMaximizeAppRequested: {
                root.toggleMaximized();
            }

            onCloseAppRequested: {
                root.close();
            }
        }

        header: MpvqcAppHeaderView {
            controller: _content.mpvqcAppHeaderController
            width: root.width
        }

        onAppWindowSizeRequested: (width, height) => {
            if (width >= root.minimumWidth && height >= root.minimumHeight) {
                root.width = width;
                root.height = height;
            }
        }

        onDisableFullScreenRequested: {
            if (root.fullscreen) {
                root.disableFullScreen();
            }
        }

        onToggleFullScreenRequested: {
            root.toggleFullScreen();
        }
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

    MpvqcQuitHandler {
        id: closeHandler

        mpvqcApplication: root
        canClose: root.mpvqcManager.saved
    }

    Binding {
        target: Qt
        property: "uiLanguage"
        value: root.mpvqcSettings.language
        delayed: true
        restoreMode: Binding.RestoreNone
    }

    Component.onCompleted: {
        _content.focusCommentTable();
    }

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
