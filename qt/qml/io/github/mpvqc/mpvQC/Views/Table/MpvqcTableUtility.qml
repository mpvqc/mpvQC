// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma Singleton

import QtQuick

import io.github.mpvqc.mpvQC.Python

QtObject {
    // Mutable, not readonly: the QML test harness swaps in a fresh view model per test.
    property var viewModel: MpvqcCommentTableTimeFormatViewModel {}

    readonly property bool useLongFormat: viewModel.useLongFormat
    readonly property var _reForbidden: /[\u00AD\r\n]/gi
    readonly property var _reStyledTextSpecial: /[&<>\s]/g

    readonly property var _highlightCache: ({
            query: "",
            regExp: null
        })

    function formatTime(inputMilliseconds: real): string {
        const inputSeconds = Math.floor(inputMilliseconds / 1000);
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
        if (!highlightedText) {
            return _toStyledText(comment, 0, comment.length);
        }
        if (highlightedText !== _highlightCache.query || _highlightCache.regExp === null) {
            _highlightCache.query = highlightedText;
            _highlightCache.regExp = new RegExp(_escapeRegExp(highlightedText), "gi");
        }
        let result = "";
        let end = 0;
        comment.replace(_highlightCache.regExp, (match, offset) => {
            result += _toStyledText(comment, end, offset);
            result += `<b><u>${_toStyledText(comment, offset, offset + match.length)}</u></b>`;
            end = offset + match.length;
            return match;
        });
        return result + _toStyledText(comment, end, comment.length);
    }

    /**
     * Qt's styled text parser collapses raw whitespace runs and drops raw whitespace at
     * the start and end, but keeps entities as is. A raw space survives only as the last
     * of a run inside the comment, so only that one stays raw, which spares the parser an
     * entity per word gap. Takes the whole comment because a run can cross a match boundary.
     */
    function _toStyledText(comment: string, start: int, end: int): string {
        return comment.slice(start, end).replace(_reStyledTextSpecial, (character, offset) => {
            switch (character) {
            case "&":
                return "&amp;";
            case "<":
                return "&lt;";
            case ">":
                return "&gt;";
            }
            const index = start + offset;
            const endsInnerSpaceRun = character === " " && index > 0 && index < comment.length - 1 && comment[index + 1] !== " ";
            return endsInnerSpaceRun ? " " : `&#${character.charCodeAt(0)};`;
        });
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
