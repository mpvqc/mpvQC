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

import "MpvqcTimeFormatUtils.js" as MpvqcTimeFormatUtils
import "MpvqcLabelWidthCalculator.js" as MpvqcLabelWidthCalculator


ApplicationWindow {
    id: root

    readonly property MpvqcManager mpvqcManager: MpvqcManager {}
    readonly property MpvqcSettings mpvqcSettings: MpvqcSettings {
        mpvqcApplication: root
    }
    readonly property MpvqcReverseTranslator mpvqcReverseTranslator: MpvqcReverseTranslator {}

    readonly property MpvqcApplicationPathsPyObject mpvqcApplicationPathsPyObject: MpvqcApplicationPathsPyObject {}
    readonly property MpvqcMpvPlayerPyObject mpvqcMpvPlayerPyObject: MpvqcMpvPlayerPyObject {}
    readonly property MpvqcMpvPlayerPropertiesPyObject mpvqcMpvPlayerPropertiesPyObject: MpvqcMpvPlayerPropertiesPyObject {}
    readonly property MpvqcFileSystemHelperPyObject mpvqcFileSystemHelperPyObject: MpvqcFileSystemHelperPyObject {}

    readonly property var mpvqcTimeFormatUtils: MpvqcTimeFormatUtils
    readonly property var mpvqcLabelWidthCalculator: MpvqcLabelWidthCalculator

    readonly property bool maximized: root.visibility === Window.Maximized
    readonly property bool fullscreen: root.visibility === Window.FullScreen

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
            mpvqcApplication: root
            focus: true
            anchors.fill: parent
            anchors.margins: root.windowBorder
        }
    }

    function toggleMaximized() {
        if (root.maximized) {
            root.showNormal()
        } else {
            root.showMaximized()
        }
     }

    function toggleFullScreen() {
        if (root.fullscreen) {
            root.disableFullScreen()
        } else {
            root.enableFullScreen()
        }
    }

    function enableFullScreen() {
        if (!root.fullscreen) {
            root.showFullScreen()
        }
    }

    function disableFullScreen() {
        if (root.fullscreen) {
            root.showNormal()
        }
    }

    onClosing: (event) => {
        closeHandler.requestClose()
        event.accepted = closeHandler.userConfirmedClose
    }

    MpvqcQuitHandler {
        id: closeHandler
        mpvqcApplication: root
        canClose: true
    }

    Component.onCompleted: {
        Qt.uiLanguage = mpvqcSettings.language
    }

    Material.theme: mpvqcSettings.theme
    Material.accent: mpvqcSettings.accent

}
