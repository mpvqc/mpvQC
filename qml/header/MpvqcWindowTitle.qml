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

import settings

Label {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcManager: mpvqcApplication.mpvqcManager
    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    readonly property var mpvqcMpvPlayerPropertiesPyObject: mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject

    readonly property bool saved: mpvqcManager.saved
    readonly property bool videoLoaded: mpvqcMpvPlayerPropertiesPyObject.video_loaded
    readonly property string videoPath: mpvqcMpvPlayerPropertiesPyObject.path
    readonly property string videoName: mpvqcMpvPlayerPropertiesPyObject.filename

    elide: LayoutMirroring.enabled ? Text.ElideRight : Text.ElideLeft
    horizontalAlignment: Text.AlignHCenter
    verticalAlignment: Text.AlignVCenter
    leftPadding: 25
    rightPadding: 25

    text: {
        const title = getTitle();
        if (root.saved) {
            return title;
        } else {
            //: %1 will be the title of the application (one of: mpvQC, file name, file path)
            return qsTranslate("MainWindow", "%1 (unsaved)").arg(title);
        }
    }

    function getTitle() {
        const selection = root.mpvqcSettings.windowTitleFormat;

        if (!videoLoaded || selection === MpvqcSettings.WindowTitleFormat.DEFAULT) {
            return Application.name;
        }

        if (selection === MpvqcSettings.WindowTitleFormat.FILE_NAME) {
            return videoName;
        } else {
            return videoPath;
        }
    }
}
