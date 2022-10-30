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
import components
import models


ScrollView {

    id: creditsTab
    width: parent.width

    contentWidth: parent.width

    Column {
        width: parent.width

        MpvqcDemiBoldLabel {
            text: 'mpv'
            anchors.horizontalCenter: parent.horizontalCenter
        }

        MpvqcDependency {
            dependency: 'libmpv'
            version: playerProperties.mpv_version.replace('mpv ', '')
            url: "https://mpv.io/"
            licence: "GPL-2.0+"
        }

        MpvqcDependency {
            dependency: 'ffmpeg'
            version: playerProperties.ffmpeg_version.replace('ffmpeg ', '')
            url: "https://ffmpeg.org/"
            licence: "GPL-2.0+"
        }

        MpvqcDemiBoldLabel {
            text: qsTranslate("AboutDialog", "Libraries")
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Repeater {
            model: MpvqcLibraryModel {}
            width: parent.width

            MpvqcDependency {
                anchors.horizontalCenter: parent.horizontalCenter
                dependency: model.name
                version: model.version
                licence: model.licence
                url: model.url
            }
        }

        MpvqcDemiBoldLabel {
            text: 'Other'
            anchors.horizontalCenter: parent.horizontalCenter
        }

        MpvqcDependency {
            dependency: 'material-design-icons'
            url: "https://github.com/google/material-design-icons"
            licence: "Apache-2.0"
        }
    }

}
