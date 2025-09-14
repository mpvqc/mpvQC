// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

DropArea {
    required property var supportedSubtitleFileExtensions

    readonly property string acceptedFormat: "text/uri-list"

    signal filesDropped(var documents, var videos, var subtitles)

    onEntered: event => handleEnter(event)
    onDropped: event => handleDrop(event)

    function handleEnter(event): void {
        if (_canHandle(event)) {
            event.accept(Qt.LinkAction);
        }
    }

    function handleDrop(event): void {
        if (_canHandle(event)) {
            _open(event.urls);
        }
    }

    function _canHandle(event): bool {
        const matchesFormat = event.formats.includes(acceptedFormat);
        const hasUrls = event.hasUrls;
        return matchesFormat && hasUrls;
    }

    function _open(urls): void {
        const decodedUrls = _decodeURIs(urls);
        const {
            documents,
            videos,
            subtitles
        } = _splitByFileExtension(decodedUrls);
        filesDropped(documents, videos, subtitles);
    }

    function _decodeURIs(urls): list<string> {
        return urls.map(url => decodeURI(url));
    }

    function _splitByFileExtension(urls) {
        const documents = [];
        const videos = [];
        const subtitles = [];

        for (const urlString of urls) {
            const url = Qt.resolvedUrl(urlString);
            if (urlString.endsWith(".txt")) {
                documents.push(url);
            } else if (_endsWithAny(supportedSubtitleFileExtensions, urlString)) {
                subtitles.push(url);
            } else {
                videos.push(url);
            }
        }
        return {
            documents,
            videos,
            subtitles
        };
    }

    function _endsWithAny(extensions, url): bool {
        return extensions.some(extension => url.endsWith(extension));
    }
}
