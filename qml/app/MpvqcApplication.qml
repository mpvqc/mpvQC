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
import QtQuick.Controls

import pyobjects
import settings
import shared

import "MpvqcTimeFormatUtils.js" as MpvqcTimeFormatUtils


ApplicationWindow {
    id: root

    readonly property var mpvqcLabelWidthCalculator: MpvqcLabelWidthCalculator { mpvqcApplication: root }
    readonly property var mpvqcManager: MpvqcManager { mpvqcApplication: root }
    readonly property var mpvqcMpvFiles: MpvqcMpvFiles { mpvqcApplication: root }
    readonly property var mpvqcNewCommentMenu: MpvqcNewCommentMenu { mpvqcApplication: root }
    readonly property var mpvqcSettings: MpvqcSettings { mpvqcApplication: root }
    readonly property var mpvqcWindowVisibilityHandler: MpvqcWindowVisibilityHandler { mpvqcApplication: root }

    readonly property alias mpvqcCommentTable: _content.mpvqcCommentTable

    readonly property var mpvqcApplicationPathsPyObject: MpvqcApplicationPathsPyObject {}
    readonly property var mpvqcClipboardPyObject: MpvqcClipboardPyObject {}
    readonly property var mpvqcDefaultTextValidatorPyObject: MpvqcDefaultTextValidatorPyObject {}
    readonly property var mpvqcCommentTypeValidatorPyObject: MpvqcCommentTypeValidatorPyObject {}
    readonly property var mpvqcEnvironmentPyObject: MpvqcEnvironmentPyObject {}
    readonly property var mpvqcExtendedDocumentExporterPyObject: MpvqcExtendedDocumentExporterPyObject {}
    readonly property var mpvqcFileSystemHelperPyObject: MpvqcFileSystemHelperPyObject {}
    readonly property var mpvqcMouseCursorPyObject: MpvqcMouseCursorPyObject {}
    readonly property var mpvqcMpvPlayerPropertiesPyObject: MpvqcMpvPlayerPropertiesPyObject {}
    readonly property var mpvqcMpvPlayerPyObject: MpvqcMpvPlayerPyObject {}
    readonly property var mpvqcResourcePyObject: MpvqcResourcePyObject {}
    readonly property var mpvqcReverseTranslatorPyObject: MpvqcReverseTranslatorPyObject {}
    readonly property var mpvqcVersionCheckerPyObject: MpvqcVersionCheckerPyObject {}

    readonly property var mpvqcTimeFormatUtils: MpvqcTimeFormatUtils

    readonly property bool maximized: mpvqcWindowVisibilityHandler.maximized
    readonly property bool fullscreen: mpvqcWindowVisibilityHandler.fullscreen

    readonly property int windowBorder: {
        if (root.fullscreen) {
            return 0
        } else if (Qt.platform.os === 'windows') {
            return root.maximized ? 8 : 1  // work around custom window properties
        } else if (Qt.platform.os === 'linux') {
            return root.maximized ? 0 : 1
        }
    }

    readonly property var supportedSubtitleFileExtensions: [
        'aqt', 'ass', 'idx', 'js', 'jss', 'mks', 'rt', 'scc', 'smi',
        'srt', 'ssa', 'sub', 'sup', 'utf', 'utf-8', 'utf8', 'vtt'
    ]

    function toggleMaximized() {
        mpvqcWindowVisibilityHandler.toggleMaximized()
    }

    function toggleFullScreen() {
        mpvqcWindowVisibilityHandler.toggleFullScreen()
    }

    function enableFullScreen() {
        mpvqcWindowVisibilityHandler.enableFullScreen()
    }

    function disableFullScreen() {
        mpvqcWindowVisibilityHandler.disableFullScreen()
    }

    onClosing: (event) => {
        closeHandler.requestClose()
        event.accepted = closeHandler.userConfirmedClose
    }

    MpvqcContent {
        id: _content

        mpvqcApplication: root
        focus: true
        anchors.fill: parent
        anchors.margins: root.windowBorder

        onSplitViewHandleHovered: (hovered) => _catchAllMouseArea.splitViewHandleHovered(hovered)

        Keys.onEscapePressed: {
            if (root.fullscreen) {
                root.disableFullScreen()
            }
        }

        Keys.onPressed: (event) => {
            if (event.key === Qt.Key_E) {
                return _handleEPressed(event)
            }
            if (event.key === Qt.Key_F) {
                return _handleFPressed(event)
            }

            if (_preventFromEverReachingUserDefinedCommands(event)) {
                return
            }

            root.mpvqcMpvPlayerPyObject.handle_key_event(event.key, event.modifiers)
        }

        function _handleEPressed(event) {
            if (event.isAutoRepeat) {
                return
            }

            const modifiers = event.modifiers

            if (modifiers === Qt.NoModifier) {
                return root.mpvqcNewCommentMenu.popupMenu()
            }
        }

        function _handleFPressed(event) {
            if (event.isAutoRepeat) {
                return
            }

            const modifiers = event.modifiers

            if (modifiers === Qt.NoModifier) {
                return root.toggleFullScreen()
            }
        }

        function _preventFromEverReachingUserDefinedCommands(event): bool {
            const key = event.key
            const modifiers = event.modifiers
            return key === Qt.Key_Up
                || key === Qt.Key_Down
                || (key === Qt.Key_Return && modifiers === Qt.NoModifier)
                || (key === Qt.Key_Escape && modifiers === Qt.NoModifier)
                || (key === Qt.Key_Delete && modifiers === Qt.NoModifier)
                || (key === Qt.Key_Backspace && modifiers === Qt.NoModifier)
                || (key === Qt.Key_F && modifiers === Qt.ControlModifier)
                || (key === Qt.Key_C && modifiers === Qt.ControlModifier)
        }

    }

    MpvqcCatchAllMouseArea {
        id: _catchAllMouseArea

        mpvqcApplication: root
        anchors.fill: parent

        onAfterPressed: {
            mpvqcCommentTable.forceActiveFocus()
        }
    }

    MpvqcQuitHandler {
        id: closeHandler

        mpvqcApplication: root
        canClose: mpvqcManager.saved
    }

    Component.onCompleted: {
        Qt.uiLanguage = mpvqcSettings.language
        mpvqcCommentTable.forceActiveFocus()
    }

    Material.theme: mpvqcSettings.theme
    Material.accent: mpvqcSettings.primary
    Material.primary: mpvqcSettings.primary

}
