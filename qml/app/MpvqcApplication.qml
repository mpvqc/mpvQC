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


ApplicationWindow {
    id: root

    readonly property MpvqcManager mpvqcManager: MpvqcManager {}
    readonly property MpvqcSettings mpvqcSettings: MpvqcSettings {}
    readonly property MpvqcReverseTranslator mpvqcReverseTranslator: MpvqcReverseTranslator {}

    readonly property MpvqcFilePathsPyObject mpvqcFilePathsPyObject: MpvqcFilePathsPyObject {}
    readonly property MpvqcFileSystemHelperPyObject mpvqcFileSystemHelperPyObject: MpvqcFileSystemHelperPyObject {}

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
            root.enableFullScreen()
        } else {
            root.disableFullScreen()
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

    Material.theme: mpvqcSettings.theme
    Material.accent: mpvqcSettings.accent

    Component.onCompleted: {
        Qt.uiLanguage = mpvqcSettings.language
    }

    MpvqcQuitHandler {
        id: closeHandler
        mpvqcApplication: root
        canClose: true
    }

    onClosing: (event) => {
        closeHandler.requestClose()
        event.accepted = closeHandler.userConfirmedClose
    }

}
