// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import "../../shared"

Column {
    id: root

    required property var mpvqcApplication
    property var mpvqcMpvPlayerPropertiesPyObject: mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject

    MpvqcHeader {
        text: qsTranslate("AboutDialog", "Powered by")
        width: root.width
        horizontalAlignment: Text.AlignHCenter
    }

    MpvqcMentionDependency {
        dependencyLicence: "GPL-2.0+"
        dependencyName: "libmpv"
        dependencyUrl: "https://mpv.io/"
        dependencyVersion: root.mpvqcMpvPlayerPropertiesPyObject.mpv_version.replace("mpv ", "")

        width: root.width
    }

    MpvqcMentionDependency {
        dependencyLicence: "GPL-2.0+"
        dependencyName: "ffmpeg"
        dependencyUrl: "https://ffmpeg.org/"
        dependencyVersion: root.mpvqcMpvPlayerPropertiesPyObject.ffmpeg_version.replace("ffmpeg ", "")

        width: root.width
    }

    Item {
        height: 10
        width: root.width
    }

    Repeater {
        model: MpvqcLibraryModel {}
        width: parent.width

        MpvqcMentionDependency {
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
            width: parent.width
        }
    }

    Item {
        height: 10
        width: root.width
    }

    MpvqcMentionDependency {
        dependencyLicence: "OFL"
        dependencyName: "Noto Sans"
        dependencyUrl: "https://fonts.google.com/noto/specimen/Noto+Sans"
        width: root.width
    }

    MpvqcMentionDependency {
        dependencyLicence: "Apache-2.0"
        dependencyName: "material-design-icons"
        dependencyUrl: "https://github.com/google/material-design-icons"
        width: root.width
    }
}
