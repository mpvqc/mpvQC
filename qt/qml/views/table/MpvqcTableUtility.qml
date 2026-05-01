// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma Singleton

import QtQuick

import pyobjects

QtObject {
    readonly property MpvqcTableUtilityViewModel viewModel: MpvqcTableUtilityViewModel {}

    readonly property bool useLongFormat: viewModel.duration >= 3600
    readonly property var _reForbidden: /[\u00AD\r\n]/gi

    function formatTime(inputSeconds: real): string {
        const hours = Math.floor(inputSeconds / 3600);
        const minutes = Math.floor((inputSeconds % 3600) / 60);
        const seconds = Math.floor(inputSeconds % 60);

        const h = hours < 10 ? '0' + hours : '' + hours;
        const m = minutes < 10 ? '0' + minutes : '' + minutes;
        const s = seconds < 10 ? '0' + seconds : '' + seconds;

        return useLongFormat ? h + ':' + m + ':' + s : m + ':' + s;
    }

    /**
     * Replace some characters:
     *  - soft hyphen (\xad); When copying from Duden they include these :|
     *  - carriage return
     *  - newline
     */
    function sanitizeText(text: string): string {
        return text.replace(_reForbidden, "");
    }

    function highlightComment(comment: string, highlightedText: string): string {
        const re = new RegExp(_escapeRegExp(highlightedText), "gi");
        return comment.replace(re, "<b><u>$&</u></b>");
    }

    /**
     * Escape regex syntax characters so the result is safe to feed into
     * `new RegExp(...)` as a literal pattern. Equivalent to the ES2025
     * `RegExp.escape`, which is not yet available in Qt's engine.
     */
    function _escapeRegExp(s: string): string {
        return s.replace(/[\\^$.*+?()[\]{}|]/g, "\\$&");
    }
}
