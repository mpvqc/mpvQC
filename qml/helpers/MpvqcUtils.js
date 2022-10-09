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


function toggleMaximized() {
    if (isMaximized()) {
        showNormal()
    } else {
        showMaximized()
    }
}


function isMaximized() {
    return appWindow.visibility === Window.Maximized
}


function showNormal() {
    appWindow.showNormal()
}


function showMaximized() {
    appWindow.showMaximized()
}


function toggleFullScreen() {
    if (isFullScreen()) {
        exitFullScreen()
    } else {
        showFullScreen()
    }
}


function isFullScreen() {
    return appWindow.visibility === Window.FullScreen
}


function exitFullScreen() {
    if (isFullScreen()) {
        appWindow.displayVideoFullScreen = false
        showNormal()
    }
}


function showFullScreen() {
    if (!isFullScreen()) {
        appWindow.showFullScreen()
        appWindow.displayVideoFullScreen = true
    }
}


function clearActiveFocus() {
    const currentFocusItem = appWindow.activeFocusItem
    if (currentFocusItem) {
        currentFocusItem.focus = false
    }
}


function getSupportedSubtitleFileEndings() {
    return ['aqt', 'ass', 'idx', 'js', 'jss', 'mks', 'rt', 'scc', 'smi', 'srt', 'ssa', 'sub', 'sup', 'utf', 'utf-8', 'utf8', 'vtt']
}

/**
 * @param urls {Array<QUrl>}
 * @returns {{subtitles: Array<QUrl>, documents: Array<QUrl>, videos: Array<QUrl>}}
 */
function splitByFileExtension(urls) {
    const subtitleExtensions = _getSubtitleExtensions()
    const documents = []; const videos = []; const subtitles = []
    for (const url of urls) {
        const urlString = url.toString()
        if (urlString.endsWith('.txt')) {
            documents.push(url)
        } else if (_endsWithAny(subtitleExtensions, urlString)) {
            subtitles.push(url)
        } else {
            videos.push(url)
        }
    }
    return { documents, videos, subtitles }
}


function _getSubtitleExtensions() {
    return getSupportedSubtitleFileEndings().map(ending => `.${ending}`)
}


function _endsWithAny(extensions, url) {
    return extensions.some(extension => url.endsWith(extension));
}
