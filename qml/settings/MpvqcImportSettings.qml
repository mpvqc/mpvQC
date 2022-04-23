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


import QtQuick
import Qt.labs.platform
import Qt.labs.settings


Item {
    id: current
    required property var settingsFile
    property var lastDirectoryVideo: settings.lastDirectoryVideo
    property var lastDirectoryDocuments: settings.lastDirectoryDocuments
    property var lastDirectorySubtitles: settings.lastDirectorySubtitles
    property bool loadVideoFromDocumentAutomatically: settings.loadVideoFromDocumentAutomatically

    Settings {
        id: settings
        fileName: current.settingsFile
        category: "Import"
        property var lastDirectoryVideo: StandardPaths.writableLocation(StandardPaths.MoviesLocation)
        property var lastDirectoryDocuments: StandardPaths.writableLocation(StandardPaths.DocumentsLocation)
        property var lastDirectorySubtitles: StandardPaths.writableLocation(StandardPaths.DocumentsLocation)
        property bool loadVideoFromDocumentAutomatically: false
    }

    function store() {
        settings.lastDirectoryVideo = current.lastDirectoryVideo
        settings.lastDirectoryDocuments = current.lastDirectoryDocuments
        settings.lastDirectorySubtitles = current.lastDirectorySubtitles
        settings.loadVideoFromDocumentAutomatically = current.loadVideoFromDocumentAutomatically
    }

}
