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

import models
import shared


ScrollView {
    id: root

    required property var mpvqcApplication

    property var mpvqcMpvPlayerPropertiesPyObject: mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject

    width: parent.width
    contentWidth: parent.width

    Column {
        width: parent.width

        MpvqcHeader {
            text: 'mpv'
            anchors.horizontalCenter: parent.horizontalCenter
        }

        MpvqcDependency {
            dependency: 'libmpv'
            version: root.mpvqcMpvPlayerPropertiesPyObject.mpv_version.replace('mpv ', '')
            url: "https://mpv.io/"
            licence: "GPL-2.0+"
        }

        MpvqcDependency {
            dependency: 'ffmpeg'
            version: root.mpvqcMpvPlayerPropertiesPyObject.ffmpeg_version.replace('ffmpeg ', '')
            url: "https://ffmpeg.org/"
            licence: "GPL-2.0+"
        }

        MpvqcHeader {
            //: Header for the section about code dependencies of the project
            text: qsTranslate("AboutDialog", "Libraries")
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Repeater {
            model: MpvqcLibraryModel {}
            width: parent.width

            MpvqcDependency {
                anchors.horizontalCenter: parent.horizontalCenter
                dependency: model.name
                visible: model.os.indexOf(Qt.platform.os) >= 0
                version: model.version
                licence: model.licence
                url: model.url
            }
        }

        MpvqcHeader {
            //: Header for the section about other dependencies like fonts and icons
            text: qsTranslate("AboutDialog", "Other")
            anchors.horizontalCenter: parent.horizontalCenter
        }

        MpvqcDependency {
            dependency: 'Noto Sans'
            url: "https://fonts.google.com/noto/specimen/Noto+Sans"
            licence: "OFL"
        }

        MpvqcDependency {
            dependency: 'material-design-icons'
            url: "https://github.com/google/material-design-icons"
            licence: "Apache-2.0"
        }
    }

}
