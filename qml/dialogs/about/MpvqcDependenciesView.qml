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
            version: mpvqcMpvPlayerPropertiesPyObject.mpv_version.replace('mpv ', '')
            url: "https://mpv.io/"
            licence: "GPL-2.0+"
        }

        MpvqcDependency {
            dependency: 'ffmpeg'
            version: mpvqcMpvPlayerPropertiesPyObject.ffmpeg_version.replace('ffmpeg ', '')
            url: "https://ffmpeg.org/"
            licence: "GPL-2.0+"
        }

        MpvqcHeader {
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
            text: 'Other'
            anchors.horizontalCenter: parent.horizontalCenter
        }

        MpvqcDependency {
            dependency: 'Noto Sans'
            url: "https://fonts.google.com/noto/specimen/Noto+Sans"
            licence: "OFL"
        }

        MpvqcDependency {
            dependency: 'Noto Sans Hebrew'
            url: "https://fonts.google.com/noto/specimen/Noto+Sans+Hebrew"
            licence: "OFL"
        }

        MpvqcDependency {
            dependency: 'Noto Sans Mono'
            url: "https://fonts.google.com/noto/specimen/Noto+Sans+Mono"
            licence: "OFL"
        }

        MpvqcDependency {
            dependency: 'material-design-icons'
            url: "https://github.com/google/material-design-icons"
            licence: "Apache-2.0"
        }
    }

}
