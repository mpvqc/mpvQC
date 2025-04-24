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
import QtQuick.Controls.Material

import models
import shared

ScrollView {
    id: root

    required property var mpvqcApplication

    property var mpvqcMpvPlayerPropertiesPyObject: mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject

    width: parent.width
    contentWidth: parent.width

    Column {
        id: _container

        width: parent.width

        MpvqcHeader {
            text: "mpv"
            width: _container.width
        }

        MpvqcDependency {
            dependencyLicence: "GPL-2.0+"
            dependencyName: "libmpv"
            dependencyUrl: "https://mpv.io/"
            dependencyVersion: root.mpvqcMpvPlayerPropertiesPyObject.mpv_version.replace("mpv ", "")
        }

        MpvqcDependency {
            dependencyLicence: "GPL-2.0+"
            dependencyName: "ffmpeg"
            dependencyUrl: "https://ffmpeg.org/"
            dependencyVersion: root.mpvqcMpvPlayerPropertiesPyObject.ffmpeg_version.replace("ffmpeg ", "")
        }

        MpvqcHeader {
            //: Header for the section about code dependencies of the project
            text: qsTranslate("AboutDialog", "Libraries")
            width: _container.width
        }

        Repeater {
            model: MpvqcLibraryModel {}
            width: parent.width

            MpvqcDependency {
                required property string licence
                required property string name
                required property string os
                required property string url
                required property string version

                dependencyLicence: licence
                dependencyName: name
                dependencyUrl: url
                dependencyVersion: version

                anchors.horizontalCenter: parent.horizontalCenter
                visible: os.indexOf(Qt.platform.os) >= 0
            }
        }

        MpvqcHeader {
            //: Header for the section about other dependencies like fonts and icons
            text: qsTranslate("AboutDialog", "Other")
            width: _container.width
        }

        MpvqcDependency {
            dependencyLicence: "OFL"
            dependencyName: "Noto Sans"
            dependencyUrl: "https://fonts.google.com/noto/specimen/Noto+Sans"
        }

        MpvqcDependency {
            dependencyLicence: "Apache-2.0"
            dependencyName: "material-design-icons"
            dependencyUrl: "https://github.com/google/material-design-icons"
        }
    }
}
