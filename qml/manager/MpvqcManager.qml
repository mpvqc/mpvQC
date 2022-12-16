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


Item {
    id: root

    property bool saved: true

    signal commentsImported(var comments)
    signal videoImported(url video)
    signal subtitlesImported(var subtitles)

    function reset() {

    }

    function openDocuments(documents) {
        console.log('MpvqcManager', 'openDocuments', documents)
    }

    function openVideo(video) {
        console.log('MpvqcManager', 'openVideo', video)
    }

    function openSubtitles(subtitles) {
        console.log('MpvqcManager', 'openSubtitles', subtitles)
    }

    function open(documents, video, subtitles) {
        console.log('MpvqcManager', 'open', documents, video, subtitles)
    }

    function save() {

    }

    function saveAs() {

    }
}
