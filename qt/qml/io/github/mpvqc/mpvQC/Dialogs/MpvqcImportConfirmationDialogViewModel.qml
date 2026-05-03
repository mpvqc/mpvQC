// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

QtObject {
    id: root

    required property string videosJson
    required property string subtitlesJson

    readonly property var videos: JSON.parse(videosJson)
    readonly property var subtitles: JSON.parse(subtitlesJson)

    readonly property var videosWithSkipOption: {
        const copy = videos.slice();
        copy.push({
            path: "",
            filename: "",
            fromDocument: false,
            fromSubtitle: false,
            isNoVideo: true
        });
        return copy;
    }

    property int selectedVideoIndex: 0

    readonly property int videoCount: videos.length
    readonly property int subtitleCount: subtitles.length
    readonly property bool hasVideos: videoCount > 0
    readonly property bool hasSubtitles: subtitleCount > 0
    readonly property bool showHeaders: hasVideos && hasSubtitles
    readonly property bool showSubtitleBatchSelectionControls: subtitleCount > 1

    signal modelChanged

    function selectVideo(index: int): void {
        selectedVideoIndex = index;
    }

    function toggleSubtitle(index: int): void {
        subtitles[index].checked = !subtitles[index].checked;
        modelChanged();
    }

    function selectAllSubtitles(): void {
        for (let i = 0; i < subtitles.length; i++) {
            subtitles[i].checked = true;
        }
        modelChanged();
    }

    function deselectAllSubtitles(): void {
        for (let i = 0; i < subtitles.length; i++) {
            subtitles[i].checked = false;
        }
        modelChanged();
    }

    function getSelectedItems(): var {
        const video = videosWithSkipOption[selectedVideoIndex]?.path ?? "";
        const subs = subtitles.filter(s => s.checked).map(s => s.path);
        return {
            video,
            subtitles: subs
        };
    }
}
