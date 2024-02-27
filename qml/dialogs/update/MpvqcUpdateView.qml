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

import QtQml
import QtQuick
import QtQuick.Controls


Label {
    id: root

    readonly property var openUrlExternally: Qt.openUrlExternally
    readonly property url mpvqcHomeUrl: "https://mpvqc.github.io"
    readonly property url mpvqcUpdateUrl: "https://mpvqc.github.io/api/v1/public/version"

    readonly property var trigger: Timer
    {
        interval: 0
        running: true

        onTriggered: {
            checkForUpdate()
        }
    }

    property string title: qsTranslate("VersionCheckDialog", "Checking for Updates...")
    property var request: new XMLHttpRequest()

    text: qsTranslate("VersionCheckDialog", "Loading...")
    horizontalAlignment: Text.AlignLeft
    wrapMode: Label.WordWrap
    elide: Text.ElideLeft

    onLinkActivated: root.openUrlExternally(root.mpvqcHomeUrl)

    function checkForUpdate() {
        const asynchronous = true
        request.open("GET", mpvqcUpdateUrl, asynchronous)
        request.onreadystatechange = () => {
            if (request.readyState !== XMLHttpRequest.DONE) {
                return
            }
            onRequestDone()
        }
        request.onerror = () => _handleUnknownError()
        request.send()
    }

    function onRequestDone() {
        if (request.status === 200) {
            _handle200()
        } else {
            _handleError()
        }
    }

    function _handle200() {
        const version = JSON.parse(request.responseText).latest
        if (version === Qt.application.version) {
            _handleUp2Date()
        } else {
            _handleNewVersionAvailable(version)
        }
    }

    function _handleUp2Date() {
        root.title = "👌"
        root.text = qsTranslate("VersionCheckDialog", "You are already using the most recent version of mpvQC!")
    }

    function _handleNewVersionAvailable(version: string) {
        root.title = qsTranslate("VersionCheckDialog", "New Version Available")
        const message = qsTranslate("VersionCheckDialog", "There is a new version of mpvQC available (%1). Visit %2 to download it.")
            .arg(`<i>${version}</i>`)
            .arg(`<a href="${mpvqcHomeUrl}">${mpvqcHomeUrl}</a>`)
        root.text = `<html>${message}</html>`
    }

    function _handleError() {
        root.title = qsTranslate("VersionCheckDialog", "Server Error")
        root.text = qsTranslate("VersionCheckDialog", "The server returned error code %1.").arg(request.status)
    }

    function _handleUnknownError() {
        root.title = qsTranslate("VersionCheckDialog", "Server Not Reachable")
        root.text = qsTranslate("VersionCheckDialog", "A connection to the server could not be established.")
    }

    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.NoButton
        cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
        hoverEnabled: true
    }
}
