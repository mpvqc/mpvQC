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

ApplicationWindow {
    id: root

    readonly property var mpvqcLabelWidthCalculator: MpvqcLabelWidthCalculator { mpvqcApplication: root }
    readonly property var mpvqcSettings: MpvqcSettings { mpvqcApplication: root }
    readonly property var mpvqcTheme: MpvqcTheme { mpvqcApplication: root }
    readonly property var mpvqcWindowVisibilityHandler: MpvqcWindowVisibilityHandler { mpvqcApplication: root }
    
    readonly property var mpvqcManager: MpvqcManager {
        mpvqcApplication: root
        commentCount: _content.commentCount
    }

    readonly property var mpvqcApplicationPathsPyObject: MpvqcApplicationPathsPyObject {}
    readonly property var mpvqcCommentTypeValidatorPyObject: MpvqcCommentTypeValidatorPyObject {}
    readonly property var mpvqcDefaultTextValidatorPyObject: MpvqcDefaultTextValidatorPyObject {}
    readonly property var mpvqcExtendedDocumentExporterPyObject: MpvqcExtendedDocumentExporterPyObject {}
    readonly property var mpvqcMpvPlayerPropertiesPyObject: MpvqcMpvPlayerPropertiesPyObject {}
    readonly property var mpvqcMpvPlayerPyObject: MpvqcMpvPlayerPyObject {}
    readonly property var mpvqcPlayerFilesPyObject: MpvqcPlayerFilesPyObject {}
    readonly property var mpvqcThemesPyObject: MpvqcThemesPyObject {}
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

    flags: Qt.FramelessWindowHint | Qt.Window
    color: Material.background
    visible: true

    font {
        pointSize: 10
        family: 'Noto Sans'
    }

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

    Component.onCompleted: {
        Qt.uiLanguage = mpvqcSettings.language;
        _content.focusCommentTable();
    }

    Material.theme: root.mpvqcTheme.isDark ? Material.Dark : Material.Light
    Material.accent: root.mpvqcTheme.control

    Material.background: root.mpvqcTheme.background
    Material.foreground: root.mpvqcTheme.foreground

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
