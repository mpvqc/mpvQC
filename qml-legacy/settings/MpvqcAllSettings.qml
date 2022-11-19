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


pragma Singleton
import QtCore
import QtQuick
import QtQuick.Controls
import Qt.labs.settings
import pyobjects


Item {
    id: current
    readonly property var settingsFile: MpvqcFilePathsPyObject.settings

    Settings {
        id: backupSettings
        fileName: current.settingsFile
        category: 'Backup'
        property bool enabled: true
        property int interval: 90
    }
    property alias backupEnabled: backupSettings.enabled
    property alias backupInterval: backupSettings.interval

    MpvqcCommonSettings {
        id: commonSettings
        settingsFile: current.settingsFile
    }
    property alias language: commonSettings.language
    property alias commentTypes: commonSettings.commentTypes

    MpvqcFileInterfacePyObject { id: _configInput; file_path: MpvqcFilePathsPyObject.input_conf }
    property alias configInput: _configInput

    MpvqcFileInterfacePyObject { id: _configMpv; file_path: MpvqcFilePathsPyObject.mpv_conf }
    property alias configMpv: _configMpv

    Settings {
        id: exportSettings
        fileName: current.settingsFile
        category: 'Export'
        property string nickname: EnvironmentPyObject.variable('USERNAME') || EnvironmentPyObject.variable('USER') || 'nick'
        property bool writeHeaderDate: true
        property bool writeHeaderGenerator: true
        property bool writeHeaderNickname: false
        property bool writeHeaderVideoPath: true
    }
    property alias exportSettings: exportSettings
    property alias nickname: exportSettings.nickname
    property alias writeHeaderDate: exportSettings.writeHeaderDate
    property alias writeHeaderGenerator: exportSettings.writeHeaderGenerator
    property alias writeHeaderNickname: exportSettings.writeHeaderNickname
    property alias writeHeaderVideoPath: exportSettings.writeHeaderVideoPath

    Settings {
        id: formatSettings
        fileName: current.settingsFile
        category: 'Format'
        property bool statusbarPercentage: true
        property int timeFormat: MpvqcAllSettings.TimeFormat.CURRENT_TOTAL_TIME
    }
    property alias statusbarPercentage: formatSettings.statusbarPercentage
    property alias timeFormat: formatSettings.timeFormat

    Settings {
        id: importSettings
        fileName: current.settingsFile
        category: 'Import'
        property var lastDirectoryVideo: StandardPaths.writableLocation(StandardPaths.MoviesLocation)
        property var lastDirectoryDocuments: StandardPaths.writableLocation(StandardPaths.DocumentsLocation)
        property var lastDirectorySubtitles: StandardPaths.writableLocation(StandardPaths.DocumentsLocation)
    }
    property alias lastDirectoryVideo: importSettings.lastDirectoryVideo
    property alias lastDirectoryDocuments: importSettings.lastDirectoryDocuments
    property alias lastDirectorySubtitles: importSettings.lastDirectorySubtitles

    Settings {
        id: splitViewSettings
        fileName: current.settingsFile
        category: 'SplitView'
        property var dimensions: ''
    }
    property alias dimensions: splitViewSettings.dimensions

    Settings {
        id: themeSettings
        fileName: current.settingsFile
        category: 'Theme'
        property int theme: Material.Dark
        property int accent: Material.Orange
    }
    property alias theme: themeSettings.theme
    property alias accent: themeSettings.accent

    enum TimeFormat { EMPTY, CURRENT_TIME, REMAINING_TIME, CURRENT_TOTAL_TIME }

    Component.onCompleted: {
        commonSettings.restore()
    }

    Component.onDestruction: {
        commonSettings.save()
    }

}
