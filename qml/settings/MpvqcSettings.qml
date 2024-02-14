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


Item {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcApplicationPathsPyObject: mpvqcApplication.mpvqcApplicationPathsPyObject
    readonly property var mpvqcEnvironmentPyObject: mpvqcApplication.mpvqcEnvironmentPyObject
    readonly property var settingsFile: mpvqcApplicationPathsPyObject.settings

    Settings {
        id: _backupSettings
        location: root.settingsFile
        category: 'Backup'
        property bool enabled: true
        property int interval: 60
    }
    property alias backupEnabled: _backupSettings.enabled
    property alias backupInterval: _backupSettings.interval


    MpvqcCommonSettings {
        id: _commonSettings
        location: root.settingsFile
    }
    property alias language: _commonSettings.language
    property alias commentTypes: _commonSettings.commentTypes


    Settings {
        id: _exportSettings
        location: root.settingsFile
        category: 'Export'
        property string nickname: root.mpvqcEnvironmentPyObject.variable('USERNAME') || root.mpvqcEnvironmentPyObject.variable('USER') || 'nickname'
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
        location: root.settingsFile
        category: 'StatusBar'
        property bool statusbarPercentage: true
        property int timeFormat: MpvqcSettings.TimeFormat.CURRENT_TOTAL_TIME
    }
    property alias statusbarPercentage: _statusBarSettings.statusbarPercentage
    property alias timeFormat: _statusBarSettings.timeFormat


    enum ImportWhenVideoLinkedInDocument { ALWAYS, ASK_EVERY_TIME, NEVER }
    Settings {
        id: _importSettings
        location: root.settingsFile
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
        location: root.settingsFile
        category: 'SplitView'
        property var dimensions: ''
        property int layoutOrientation: Qt.Vertical
    }
    property alias dimensions: _splitViewSettings.dimensions
    property alias layoutOrientation: _splitViewSettings.layoutOrientation


    Settings {
        id: _themeSettings
        location: root.settingsFile
        category: 'Theme'
        property int theme: Material.Dark
        property int primary: Material.Indigo
    }
    property alias theme: _themeSettings.theme
    property alias primary: _themeSettings.primary


    enum WindowTitleFormat { DEFAULT, FILE_NAME, FILE_PATH }
    Settings {
        id: _windowSettings
        location: root.settingsFile
        category: 'Window'
        property int titleFormat: MpvqcSettings.WindowTitleFormat.DEFAULT
    }
    property alias windowTitleFormat: _windowSettings.titleFormat


    Component.onCompleted: {
        _commonSettings.restore()
    }

    Component.onDestruction: {
        _commonSettings.save()
    }
}
