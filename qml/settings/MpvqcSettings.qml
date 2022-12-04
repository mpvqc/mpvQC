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

//    readonly property var settingsFile: MpvqcFilePathsPyObject.settings

//    Settings {
//        id: _backupSettings
//        // fileName: '/home/elias/PycharmProjects/mpvQC-dev/appdata/settings.ini' // todo change'/home/elias/PycharmProjects/mpvQC-dev/appdata/settings.ini' // todo change
//        category: 'Backup'
//        property bool enabled: true
//        property int interval: 90
//    }
//    property alias backupEnabled: _backupSettings.enabled
//    property alias backupInterval: _backupSettings.interval

    MpvqcCommonSettings {
        id: _commonSettings
        // fileName: '/home/elias/PycharmProjects/mpvQC-dev/appdata/settings.ini' // todo change'/home/elias/PycharmProjects/mpvQC-dev/appdata/settings.ini' // todo change
    }
    property alias language: _commonSettings.language
    property alias commentTypes: _commonSettings.commentTypes

//    MpvqcFileInterfacePyObject { id: _configInput; file_path: MpvqcFilePathsPyObject.input_conf }
//    property alias configInput: _configInput
//
//    MpvqcFileInterfacePyObject { id: _configMpv; file_path: MpvqcFilePathsPyObject.mpv_conf }
//    property alias configMpv: _configMpv

    Settings {
        id: _exportSettings
        // fileName: '/home/elias/PycharmProjects/mpvQC-dev/appdata/settings.ini' // todo change'/home/elias/PycharmProjects/mpvQC-dev/appdata/settings.ini' // todo change
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

//    Settings {
//        id: _formatSettings
//        // fileName: '/home/elias/PycharmProjects/mpvQC-dev/appdata/settings.ini' // todo change'/home/elias/PycharmProjects/mpvQC-dev/appdata/settings.ini' // todo change
//        category: 'Format'
//        property bool statusbarPercentage: true
//        property int timeFormat: MpvqcAllSettings.TimeFormat.CURRENT_TOTAL_TIME
//    }
//    property alias statusbarPercentage: _formatSettings.statusbarPercentage
//    property alias timeFormat: _formatSettings.timeFormat

    Settings {
        id: _importSettings
        // fileName: '/home/elias/PycharmProjects/mpvQC-dev/appdata/settings.ini' // todo change'/home/elias/PycharmProjects/mpvQC-dev/appdata/settings.ini' // todo change
        category: 'Import'
        property var lastDirectoryVideo: StandardPaths.writableLocation(StandardPaths.MoviesLocation)
        property var lastDirectoryDocuments: StandardPaths.writableLocation(StandardPaths.DocumentsLocation)
        property var lastDirectorySubtitles: StandardPaths.writableLocation(StandardPaths.DocumentsLocation)
    }
    property alias lastDirectoryVideo: _importSettings.lastDirectoryVideo
    property alias lastDirectoryDocuments: _importSettings.lastDirectoryDocuments
    property alias lastDirectorySubtitles: _importSettings.lastDirectorySubtitles

//    Settings {
//        id: _splitViewSettings
//        // fileName: '/home/elias/PycharmProjects/mpvQC-dev/appdata/settings.ini' // todo change'/home/elias/PycharmProjects/mpvQC-dev/appdata/settings.ini' // todo change
//        category: 'SplitView'
//        property var dimensions: ''
//    }
//    property alias dimensions: _splitViewSettings.dimensions

    Settings {
        id: _themeSettings
        // fileName: '/home/elias/PycharmProjects/mpvQC-dev/appdata/settings.ini' // todo change'/home/elias/PycharmProjects/mpvQC-dev/appdata/settings.ini' // todo change
        category: 'Theme'
        property int theme: Material.Dark
        property int accent: Material.Orange
    }
    property alias theme: _themeSettings.theme
    property alias accent: _themeSettings.accent

//    enum TimeFormat { EMPTY, CURRENT_TIME, REMAINING_TIME, CURRENT_TOTAL_TIME }


    Component.onCompleted: {
        _commonSettings.restore()
    }

    Component.onDestruction: {
        _commonSettings.save()
    }
}
