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

import "../header"
import "../manager"
import "../settings"

ApplicationWindow {
    id: root

    readonly property var mpvqcApplicationPathsPyObject: MpvqcApplicationPathsPyObject {}
    readonly property var mpvqcCommentTypeValidatorPyObject: MpvqcCommentTypeValidatorPyObject {}
    readonly property var mpvqcExtendedDocumentExporterPyObject: MpvqcExtendedDocumentExporterPyObject {}
    readonly property var mpvqcMpvPlayerPropertiesPyObject: MpvqcMpvPlayerPropertiesPyObject {}
    readonly property var mpvqcMpvPlayerPyObject: MpvqcMpvPlayerPyObject {}
    readonly property var mpvqcPlayerFilesPyObject: MpvqcPlayerFilesPyObject {}
    readonly property var mpvqcUtilityPyObject: MpvqcUtilityPyObject {}
    readonly property var mpvqcVersionCheckerPyObject: MpvqcVersionCheckerPyObject {}

    readonly property MpvqcManager mpvqcManager: MpvqcManager {}

    readonly property var mpvqcLabelWidthCalculator: MpvqcLabelWidthCalculator {
        mpvqcApplication: root
    }

    readonly property var mpvqcSettings: MpvqcSettings {
        mpvqcApplication: root
    }

    readonly property var mpvqcTheme: MpvqcTheme {
        themeIdentifier: root.mpvqcSettings.themeIdentifier
        themeColorOption: root.mpvqcSettings.themeColorOption
    }

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

    font {
        pointSize: 10
        family: 'Noto Sans'
    }

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
        headerController: _headerController

        focus: true
        anchors.fill: parent
        anchors.margins: root.windowBorder

        header: MpvqcAppHeaderView {
            controller: _headerController
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
                _windowVisibilityHandler.disableFullScreen();
            }
        }

        onToggleFullScreenRequested: {
            _windowVisibilityHandler.toggleFullScreen();
        }
    }

    MpvqcAppHeaderController {
        id: _headerController

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

        onWindowDragRequested: {
            root.startSystemMove();
        }

        onMinimizeAppRequested: {
            root.showMinimized();
        }

        onToggleMaximizeAppRequested: {
            _windowVisibilityHandler.toggleMaximized();
        }

        onCloseAppRequested: {
            root.close();
        }
    }

    MpvqcBackupper {
        backend: MpvqcBackupperBackendPyObject {} // qmllint disable
        isHaveComments: _content.commentCount
        isBackupEnabled: root.mpvqcSettings.backupEnabled
        backupInterval: root.mpvqcSettings.backupInterval
    }

    MpvqcWindowVisibilityHandler {
        id: _windowVisibilityHandler

        mpvqcApplication: root
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
