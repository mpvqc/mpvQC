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


DropArea {
    required property var supportedSubtitleFileExtensions

    readonly property var acceptedFormat: 'text/uri-list'

    signal filesDropped(var documents, url video, var subtitles)

    onEntered: (event) => handleEnter(event)
    onDropped: (event) => handleDrop(event)

    function handleEnter(event) {
        if (_canHandle(event)) {
            event.accept(Qt.LinkAction)
        }
    }

    function handleDrop(event) {
        if (_canHandle(event)) {
            _open(event.urls)
        }
    }

    function _canHandle(event) {
        const matchesFormat = event.formats.includes(acceptedFormat)
        const hasUrls = event.hasUrls
        return matchesFormat && hasUrls
    }

    function _open(urls) {
        const decodedUrls = _decodeURIs(urls)
        const { documents, videos, subtitles } = _splitByFileExtension(decodedUrls)
        const video = videos.length > 0 ? videos[0] : ''
        filesDropped(documents, video, subtitles)
    }

    function _decodeURIs(urls) {
        return urls.map(url => decodeURI(url))
    }

    function _splitByFileExtension(urls) {
        const documents = []; const videos = []; const subtitles = []
        for (const url of urls) {
            const urlString = url.toString()
            if (urlString.endsWith('.txt')) {
                documents.push(url)
            } else if (_endsWithAny(supportedSubtitleFileExtensions, urlString)) {
                subtitles.push(url)
            } else {
                videos.push(url)
            }
        }
        return { documents, videos, subtitles }
    }

    function _endsWithAny(extensions, url) {
        return extensions.some(extension => url.endsWith(extension));
    }

}
