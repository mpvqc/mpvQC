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
import QtQuick.Controls.Material

import manager
import pyobjects
import settings

import "MpvqcKeyCommandGenerator.js" as MpvqcKeyCommandGenerator
import "MpvqcTimeFormatUtils.js" as MpvqcTimeFormatUtils
import "MpvqcWidthCalculatorLabel.js" as MpvqcWidthCalculatorLabel


ApplicationWindow {
    id: root

    readonly property var mpvqcManager: MpvqcManager { mpvqcApplication: root }
    readonly property var mpvqcSettings: MpvqcSettings { mpvqcApplication: root }
    readonly property var mpvqcWidthCalculatorCommentTypes: MpvqcWidthCalculatorCommentTypes { mpvqcApplication: root }
    readonly property alias mpvqcCommentTable: _content.mpvqcCommentTable
    readonly property var mvqcMpvFiles: MpvqcMpvFiles { mpvqcApplication: root }
    readonly property var mpvqcWindowVisibilityHandler: MpvqcWindowVisibilityHandler { mpvqcApplication: root }

    readonly property var mpvqcApplicationPathsPyObject: MpvqcApplicationPathsPyObject {}
    readonly property var mpvqcBackupPyObject: MpvqcBackupPyObject {}
    readonly property var mpvqcClipboardPyObject: MpvqcClipboardPyObject {}
    readonly property var mpvqcSpecialCharacterValidatorPyObject: MpvqcSpecialCharacterValidatorPyObject {}
    readonly property var mpvqcMpvPlayerPyObject: MpvqcMpvPlayerPyObject {}
    readonly property var mpvqcMpvPlayerPropertiesPyObject: MpvqcMpvPlayerPropertiesPyObject {}
    readonly property var mpvqcFileSystemHelperPyObject: MpvqcFileSystemHelperPyObject {}
    readonly property var mpvqcEnvironmentPyObject: MpvqcEnvironmentPyObject {}
    readonly property var mpvqcReverseTranslatorPyObject: MpvqcReverseTranslatorPyObject {}
    readonly property var mpvqcResourcePyObject: MpvqcResourcePyObject {}

    readonly property var mpvqcKeyCommandGenerator: MpvqcKeyCommandGenerator
    readonly property var mpvqcTimeFormatUtils: MpvqcTimeFormatUtils
    readonly property var mpvqcWidthCalculatorLabel: MpvqcWidthCalculatorLabel

    readonly property bool maximized: mpvqcWindowVisibilityHandler.maximized
    readonly property bool fullscreen: mpvqcWindowVisibilityHandler.fullscreen

    readonly property int windowBorder: root.maximized || root.fullscreen ? 0 : 6
    readonly property int windowRadius: 12

    readonly property var supportedSubtitleFileExtensions: [
        'aqt', 'ass', 'idx', 'js', 'jss', 'mks', 'rt', 'scc', 'smi',
        'srt', 'ssa', 'sub', 'sup', 'utf', 'utf-8', 'utf8', 'vtt'
    ]

    background: Rectangle {
        radius: root.windowRadius
        color: Material.background

        MpvqcWindowMouseCurserHandler {
            borderWidth: root.windowBorder
            anchors.fill: parent
        }

        MpvqcWindowResizeHandler {
            mpvqcApplication: root
            borderWidth: root.windowBorder
        }

        MpvqcContent {
            id: _content

            mpvqcApplication: root
            focus: true
            anchors.fill: parent
            anchors.margins: root.windowBorder
        }
    }

    function toggleMaximized() { mpvqcWindowVisibilityHandler.toggleMaximized() }
    function toggleFullScreen() { mpvqcWindowVisibilityHandler.toggleFullScreen() }
    function enableFullScreen() { mpvqcWindowVisibilityHandler.enableFullScreen() }
    function disableFullScreen() { mpvqcWindowVisibilityHandler.disableFullScreen() }

    onClosing: (event) => {
        closeHandler.requestClose()
        event.accepted = closeHandler.userConfirmedClose
    }

    onActiveFocusItemChanged: {
        if (!activeFocusItem) {
            return
        }
        if (activeFocusItem === contentItem) {
            mpvqcCommentTable.forceActiveFocus()
            return
        }
        const asString = activeFocusItem.toString()
        if (asString.includes('QQuickRootItem')) {
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
    }

    Material.theme: mpvqcSettings.theme
    Material.accent: mpvqcSettings.accent

}
