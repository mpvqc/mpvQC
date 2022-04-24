/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


pragma Singleton
import QtQuick
import Qt.labs.settings
import pyobjects


Item {
    id: current
    readonly property var settingsFile: SettingsPyObject.backing_object_file_name

    MpvqcBackupSettings {
        id: backupSettings
        settingsFile: current.settingsFile
    }
    property alias backupEnabled: backupSettings.enabled
    property alias backupInterval: backupSettings.interval

    MpvqcCommonSettings {
        id: commonSettings
        settingsFile: current.settingsFile
    }
    property alias language: commonSettings.language
    property alias commentTypes: commonSettings.commentTypes

    MpvqcConfigFileSettings {
        id: configFileSettings
    }
    property alias configInput: configFileSettings.configInput
    property alias configMpv: configFileSettings.configMpv

    MpvqcExportSettings {
        id: exportSettings
        settingsFile: current.settingsFile
    }
    property alias nickname: exportSettings.nickname
    property alias appendNickname: exportSettings.appendNickname
    property alias writeHeader: exportSettings.writeHeader
    property alias writeHeaderDate: exportSettings.writeHeaderDate
    property alias writeHeaderGenerator: exportSettings.writeHeaderGenerator
    property alias writeHeaderNickname: exportSettings.writeHeaderNickname
    property alias writeHeaderVideoPath: exportSettings.writeHeaderVideoPath

    MpvqcFormatSettings {
        id: formatSettings
        settingsFile: current.settingsFile
    }
    property alias statusbarPercentage: formatSettings.statusbarPercentage
    property alias timeFormat: formatSettings.timeFormat
    property alias titleFormat: formatSettings.titleFormat

    MpvqcImportSettings {
        id: importSettings
        settingsFile: current.settingsFile
    }
    property alias lastDirectoryVideo: importSettings.lastDirectoryVideo
    property alias lastDirectoryDocuments: importSettings.lastDirectoryDocuments
    property alias lastDirectorySubtitles: importSettings.lastDirectorySubtitles
    property alias loadVideoFromDocumentAutomatically: importSettings.loadVideoFromDocumentAutomatically

    MpvqcThemeSettings {
        id: themeSettings
        settingsFile: current.settingsFile
    }
    property alias theme: themeSettings.theme
    property alias accent: themeSettings.accent

    Component.onCompleted: {
        commonSettings.restore()
    }

    Component.onDestruction: {
        backupSettings.store()
        commonSettings.store()
        exportSettings.store()
        formatSettings.store()
        importSettings.store()
        themeSettings.store()
    }

}
