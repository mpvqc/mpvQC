// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import "../components"

MpvqcDialog {
    id: root

    required property string videosJson
    required property string subtitlesJson

    readonly property var videos: JSON.parse(videosJson)
    readonly property var subtitles: JSON.parse(subtitlesJson)

    readonly property bool hasVideos: videos.length > 0
    readonly property bool hasSubtitles: subtitles.length > 0

    signal importConfirmed(selectedVideoPath: string, selectedSubtitlePaths: list<string>)

    title: qsTranslate("MessageBoxes", "Import Confirmation")
    standardButtons: Dialog.Ok | Dialog.Cancel
    contentWidth: 500

    Component.onCompleted: {
        console.log("DIALOG CREATED");
        console.log("hasVideos", hasVideos);
        console.log("videos", videos);
        console.log("hasSubtitles", hasSubtitles);
        console.log("subtitles", subtitles);
    }
}
