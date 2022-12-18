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

import QtCore
import QtQuick
import QtQuick.Controls.Material
import Qt.labs.settings

Item {
    id: root

    required property var mpvqcApplication
    readonly property var mpvqcApplicationPathsPyObject: mpvqcApplication.mpvqcApplicationPathsPyObject
    readonly property var settingsFile: mpvqcApplicationPathsPyObject.settings

    Settings {
        id: _backupSettings
        fileName: root.settingsFile
        category: 'Backup'
        property bool enabled: true
        property int interval: 90
    }
    property alias backupEnabled: _backupSettings.enabled
    property alias backupInterval: _backupSettings.interval

    MpvqcCommonSettings {
        id: _commonSettings
        fileName: root.settingsFile
    }
    property alias language: _commonSettings.language
    property alias commentTypes: _commonSettings.commentTypes

//    MpvqcFileInterfacePyObject { id: _configInput; file_path: MpvqcApplicationPathsPyObject.input_conf }
//    property alias configInput: _configInput
//
//    MpvqcFileInterfacePyObject { id: _configMpv; file_path: MpvqcApplicationPathsPyObject.mpv_conf }
//    property alias configMpv: _configMpv

    Settings {
        id: _exportSettings
        fileName: root.settingsFile
        category: 'Export'
        property string nickname: 'nickname' // EnvironmentPyObject.variable('USERNAME') || EnvironmentPyObject.variable('USER') || 'nick'
        property bool writeHeaderDate: true
        property bool writeHeaderGenerator: true
        property bool writeHeaderNickname: false
        property bool writeHeaderVideoPath: true
    }
    property alias nickname: _exportSettings.nickname
    property alias writeHeaderDate: _exportSettings.writeHeaderDate
    property alias writeHeaderGenerator: _exportSettings.writeHeaderGenerator
    property alias writeHeaderNickname: _exportSettings.writeHeaderNickname
    property alias writeHeaderVideoPath: _exportSettings.writeHeaderVideoPath

    enum TimeFormat { EMPTY, CURRENT_TIME, REMAINING_TIME, CURRENT_TOTAL_TIME }
    Settings {
        id: _statusBarSettings
        fileName: root.settingsFile
        category: 'StatusBar'
        property bool statusbarPercentage: true
        property int timeFormat: MpvqcSettings.TimeFormat.CURRENT_TOTAL_TIME
    }
    property alias statusbarPercentage: _statusBarSettings.statusbarPercentage
    property alias timeFormat: _statusBarSettings.timeFormat

    enum ImportWhenVideoLinkedInDocument { ASK_EVERY_TIME, NEVER, ALWAYS }
    Settings {
        id: _importSettings
        fileName: root.settingsFile
        category: 'Import'
        property var lastDirectoryVideo: StandardPaths.writableLocation(StandardPaths.MoviesLocation)
        property var lastDirectoryDocuments: StandardPaths.writableLocation(StandardPaths.DocumentsLocation)
        property var lastDirectorySubtitles: StandardPaths.writableLocation(StandardPaths.DocumentsLocation)
        property var importWhenVideoLinkedInDocument: MpvqcSettings.ImportWhenVideoLinkedInDocument.ASK_EVERY_TIME
    }
    property alias importWhenVideoLinkedInDocument: _importSettings.importWhenVideoLinkedInDocument
    property alias lastDirectoryVideo: _importSettings.lastDirectoryVideo
    property alias lastDirectoryDocuments: _importSettings.lastDirectoryDocuments
    property alias lastDirectorySubtitles: _importSettings.lastDirectorySubtitles

    Settings {
        id: _splitViewSettings
        fileName: root.settingsFile
        category: 'SplitView'
        property var dimensions: ''
    }
    property alias dimensions: _splitViewSettings.dimensions

    Settings {
        id: _themeSettings
        fileName: root.settingsFile
        category: 'Theme'
        property int theme: Material.Dark
        property int accent: Material.Orange
    }
    property alias theme: _themeSettings.theme
    property alias accent: _themeSettings.accent

    Component.onCompleted: {
        _commonSettings.restore()
    }

    Component.onDestruction: {
        _commonSettings.save()
    }
}
