// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtTest

TestCase {
    id: testCase

    name: "MpvqcTableUtility"
    width: 100
    height: 100
    visible: true
    when: windowShown

    property Component utilityComponent: Qt.createComponent("MpvqcTableUtility.qml")

    function makeUtility(properties: var): var {
        const utility = createTemporaryObject(utilityComponent, testCase, properties ?? {});
        verify(utility);
        return utility;
    }

    function test_formatTime_data(): var {
        return [
            {
                tag: "short-format--zero",
                useLongFormat: false,
                milliseconds: 0 * 1000,
                expected: "00:00"
            },
            {
                tag: "short-format--single-second",
                useLongFormat: false,
                milliseconds: 7 * 1000,
                expected: "00:07"
            },
            {
                tag: "short-format--single-minute",
                useLongFormat: false,
                milliseconds: 65 * 1000,
                expected: "01:05"
            },
            {
                tag: "short-format--ten-minutes",
                useLongFormat: false,
                milliseconds: 605 * 1000,
                expected: "10:05"
            },
            {
                tag: "short-format--just-below-one-hour",
                useLongFormat: false,
                milliseconds: 3599 * 1000,
                expected: "59:59"
            },
            {
                tag: "short-format--sub-second-truncates",
                useLongFormat: false,
                milliseconds: 12 * 1000 + 900,
                expected: "00:12"
            },
            {
                tag: "long-format--zero",
                useLongFormat: true,
                milliseconds: 0 * 1000,
                expected: "00:00:00"
            },
            {
                tag: "long-format--single-second",
                useLongFormat: true,
                milliseconds: 7 * 1000,
                expected: "00:00:07"
            },
            {
                tag: "long-format--single-minute",
                useLongFormat: true,
                milliseconds: 65 * 1000,
                expected: "00:01:05"
            },
            {
                tag: "long-format--exactly-one-hour",
                useLongFormat: true,
                milliseconds: 3600 * 1000,
                expected: "01:00:00"
            },
            {
                tag: "long-format--mixed-h-m-s",
                useLongFormat: true,
                milliseconds: 3661 * 1000,
                expected: "01:01:01"
            },
            {
                tag: "long-format--double-digit-hours",
                useLongFormat: true,
                milliseconds: 36000 * 1000,
                expected: "10:00:00"
            }
        ];
    }

    function test_formatTime(data): void {
        const utility = makeUtility({
            useLongFormat: data.useLongFormat
        });
        compare(utility.formatTime(data.milliseconds), data.expected);
    }

    function test_sanitizeText_data(): var {
        return [
            {
                tag: "plain-text-unchanged",
                input: "Hello, World!",
                expected: "Hello, World!"
            },
            {
                tag: "empty-unchanged",
                input: "",
                expected: ""
            },
            {
                tag: "strips-soft-hyphen",
                input: "soft\u00adhyphen",
                expected: "softhyphen"
            },
            {
                tag: "strips-multiple-soft-hyphens",
                input: "\u00adsoft\u00adhyphen\u00ad",
                expected: "softhyphen"
            },
            {
                tag: "strips-carriage-return",
                input: "line1\rline2",
                expected: "line1line2"
            },
            {
                tag: "strips-newline",
                input: "line1\nline2",
                expected: "line1line2"
            },
            {
                tag: "strips-crlf",
                input: "line1\r\nline2",
                expected: "line1line2"
            },
            {
                tag: "strips-mixed-forbidden-characters",
                input: "a\u00adb\nc\rd",
                expected: "abcd"
            },
            {
                tag: "preserves-tabs-and-spaces",
                input: "a\tb c",
                expected: "a\tb c"
            },
            {
                tag: "preserves-unicode-content",
                input: "コメント — café",
                expected: "コメント — café"
            }
        ];
    }

    function test_sanitizeText(data): void {
        const utility = makeUtility({});

        // Call twice with the same fresh input to guard against accidental
        // statefulness in the shared `_reForbidden` regex (e.g. lastIndex
        // leaking between calls).
        compare(utility.sanitizeText(data.input), data.expected);
        compare(utility.sanitizeText(data.input), data.expected);
    }

    function test_highlightComment_data(): var {
        return [
            {
                tag: "single-match-wrapped-in-bold-underline",
                comment: "Hello world",
                highlight: "world",
                expected: "Hello <b><u>world</u></b>"
            },
            {
                tag: "is-case-insensitive",
                comment: "Hello WORLD",
                highlight: "world",
                expected: "Hello <b><u>WORLD</u></b>"
            },
            {
                tag: "preserves-original-casing-in-replacement",
                comment: "Hello World and world",
                highlight: "WORLD",
                expected: "Hello <b><u>World</u></b> and <b><u>world</u></b>"
            },
            {
                tag: "highlights-all-occurrences",
                comment: "ababab",
                highlight: "b",
                expected: "a<b><u>b</u></b>a<b><u>b</u></b>a<b><u>b</u></b>"
            },
            {
                tag: "no-match-returns-comment-unchanged",
                comment: "Hello world",
                highlight: "missing",
                expected: "Hello world"
            },
            {
                tag: "regex-special-chars-treated-literally",
                comment: "price is $5.00 (cheap)",
                highlight: "$5.00",
                expected: "price is <b><u>$5.00</u></b> (cheap)"
            },
            {
                tag: "regex-metacharacter-dot-not-wildcard",
                comment: "abc a.c axc",
                highlight: "a.c",
                expected: "abc <b><u>a.c</u></b> axc"
            },
            {
                tag: "regex-brackets-treated-literally",
                comment: "see [note] here",
                highlight: "[note]",
                expected: "see <b><u>[note]</u></b> here"
            }
        ];
    }

    function test_highlightComment(data): void {
        const utility = makeUtility({});
        compare(utility.highlightComment(data.comment, data.highlight), data.expected);
    }

    function test_highlightComment_isStableAcrossRepeatedQueries(): void {
        const utility = makeUtility({});
        compare(utility.highlightComment("Hello world", "world"), "Hello <b><u>world</u></b>");
        compare(utility.highlightComment("another world here", "world"), "another <b><u>world</u></b> here");
        compare(utility.highlightComment("no match here", "world"), "no match here");
    }

    function test_highlightComment_recompilesWhenQueryChanges(): void {
        const utility = makeUtility({});
        compare(utility.highlightComment("foo bar", "foo"), "<b><u>foo</u></b> bar");
        compare(utility.highlightComment("foo bar", "bar"), "foo <b><u>bar</u></b>");
        compare(utility.highlightComment("foo bar", "foo"), "<b><u>foo</u></b> bar");
    }

    function test_highlightComment_returnsCommentUnchangedForEmptyQuery(): void {
        const utility = makeUtility({});
        compare(utility.highlightComment("Hello world", ""), "Hello world");
    }

    function test_highlightComment_emptyQueryBetweenSameQueryStillHighlights(): void {
        const utility = makeUtility({});
        compare(utility.highlightComment("Hello world", "world"), "Hello <b><u>world</u></b>");
        compare(utility.highlightComment("Hello world", ""), "Hello world");
        compare(utility.highlightComment("Hello world", "world"), "Hello <b><u>world</u></b>");
    }

    function test_highlightComment_emptyQueryBetweenDifferentQueriesStillHighlights(): void {
        const utility = makeUtility({});
        compare(utility.highlightComment("foo bar", "foo"), "<b><u>foo</u></b> bar");
        compare(utility.highlightComment("foo bar", ""), "foo bar");
        compare(utility.highlightComment("foo bar", "bar"), "foo <b><u>bar</u></b>");
    }
}
