// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma Singleton

import QtQuick

import pyobjects

QtObject {
    readonly property MpvqcTableUtilityBackend backend: MpvqcTableUtilityBackend {}

    readonly property bool useLongFormat: backend.duration >= 3600

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
        const reForbidden = /[\u00AD\r\n]/gi;
        if (text.search(reForbidden) === -1) {
            return text;
        }
        return text.replace(reForbidden, "");
    }

    /**
     * @param comment {string}
     * @param highlightedText {string}
     * @returns {string}
     */
    function highlightComment(comment: string, highlightedText: string): string {
        const re = new RegExp(_escapeRegExp(highlightedText), "gi");
        return comment.replace(re, "<b><u>$&</u></b>");
    }

    /**
     * https://github.com/tc39/proposal-regex-escaping
     * This is a direct translation to code of the spec
     */
    function _escapeRegExp(S: string): string {
        // 1. let str be ToString(S).
        // 2. ReturnIfAbrupt(str).
        const str = String(S);
        // 3. Let cpList be a List containing in order the code
        // points as defined in 6.1.4 of str, starting at the first element of str.
        const cpList = Array.from(str[Symbol.iterator]());
        // 4. let cuList be a new List
        const cuList = [];
        // 5. For each code point c in cpList in List order, do:
        for (const c of cpList) {
            // i. If c is a SyntaxCharacter then do:
            if ("^$\\.*+?()[]{}|".indexOf(c) !== -1) {
                // a. Append "\" to cuList.
                cuList.push("\\");
            }
            // Append c to cpList.
            cuList.push(c);
        }
        // 7. Return a String whose elements are, in order, the elements of cuList.
        return cuList.join("");
    }
}
