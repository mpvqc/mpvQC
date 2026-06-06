// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import io.github.mpvqc.mpvQC.Utility

QtObject {
    required property string mpvVersion
    required property string ffmpegVersion

    //: Section title in the licenses view above the media playback libraries
    readonly property string playbackTitle: qsTranslate("AboutDialog", "Playback")
    //: Section title in the licenses view above the code dependencies
    readonly property string librariesTitle: qsTranslate("AboutDialog", "Libraries")
    //: Section title in the licenses view above the bundled font and icon sets
    readonly property string fontsAndIconsTitle: qsTranslate("AboutDialog", "Fonts and icons")

    readonly property var playbackEntries: [
        {
            name: "libmpv",
            version: mpvVersion,
            licence: "GPL-2.0+",
            url: "https://mpv.io/",
            icon: MpvqcIcons.deployedCode
        },
        {
            name: "ffmpeg",
            version: ffmpegVersion,
            licence: "GPL-2.0+",
            url: "https://ffmpeg.org/",
            icon: MpvqcIcons.deployedCode
        },
    ]

    readonly property var fontsAndIconsEntries: [
        {
            name: "Noto Sans",
            version: "",
            licence: "OFL",
            url: "https://fonts.google.com/noto/specimen/Noto+Sans",
            icon: MpvqcIcons.title
        },
        {
            name: "material-design-icons",
            version: "",
            licence: "Apache-2.0",
            url: "https://github.com/google/material-design-icons",
            icon: MpvqcIcons.palette
        },
    ]
}
