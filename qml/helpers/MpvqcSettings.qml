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
import QtQuick.Controls
import Qt.labs.platform
import Qt.labs.settings
import pyobjects
import "mpvqc-settings-default-language.js" as MpvqcLanguage


Item {
    id: current
    readonly property var settingsFile: SettingsPyObject.backing_object_file_name

    Settings {
        id: settingsTheme
        fileName: current.settingsFile
        category: "Theme"

        property int theme: Material.Dark
        property int accent: Material.Orange
    }

    property int theme: settingsTheme.theme
    property int accent: settingsTheme.accent

    Settings {
        id: settingsCommon
        fileName: current.settingsFile
        category: "Common"

        property string language: MpvqcLanguage.getDefault(current)
    }

    property string language: settingsCommon.language

    Settings {
        id: importSettings
        fileName: current.settingsFile
        category: "Import"
        property var lastDirectoryVideo: StandardPaths.writableLocation(StandardPaths.MoviesLocation)
        property var lastDirectoryDocuments: StandardPaths.writableLocation(StandardPaths.DocumentsLocation)
        property var lastDirectorySubtitles: StandardPaths.writableLocation(StandardPaths.DocumentsLocation)
    }

    property var lastDirectoryVideo: importSettings.lastDirectoryVideo
    property var lastDirectoryDocuments: importSettings.lastDirectoryDocuments
    property var lastDirectorySubtitles: importSettings.lastDirectorySubtitles

    Component.onDestruction: {
        settingsTheme.theme = current.theme
        settingsTheme.accent = current.accent

        settingsCommon.language = current.language

        importSettings.lastDirectoryVideo = current.lastDirectoryVideo
        importSettings.lastDirectoryDocuments = current.lastDirectoryDocuments
        importSettings.lastDirectorySubtitles = current.lastDirectorySubtitles
    }

}
