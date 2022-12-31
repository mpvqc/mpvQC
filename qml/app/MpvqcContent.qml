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

import footer
import header


FocusScope {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcManager: mpvqcApplication.mpvqcManager
    readonly property var supportedSubtitleFileExtensions: mpvqcApplication.supportedSubtitleFileExtensions

    readonly property alias mpvqcCommentTable: _contentSplitView.mpvqcCommentTable

    MpvqcResizeToOriginalResolutionHandler {
        id: _videoResizer

        mpvqcApplication: root.mpvqcApplication
        header: _page.header
        footer: _page.footer
        splitView: _contentSplitView
    }

    Page {
        id: _page

        anchors.fill: parent

        header: MpvqcHeader {
            mpvqcApplication: root.mpvqcApplication
            width: parent.width

            onResizeVideoTriggered: _videoResizer.resizeVideo()
        }

        footer: MpvqcFooter {
            mpvqcApplication: root.mpvqcApplication
            width: parent.width
        }

        MpvqcContentSplitView {
            id: _contentSplitView

            mpvqcApplication: root.mpvqcApplication
            focus: true
            anchors.fill: _page.contentItem

            MpvqcDragAndDropHandler {
                anchors.fill: parent
                supportedSubtitleFileExtensions: root.supportedSubtitleFileExtensions

                onFilesDropped: (docs, vid, subs) => {
                    root.mpvqcManager.open(docs, vid, subs)
                }
            }
        }

    }

}
