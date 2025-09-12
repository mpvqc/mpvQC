/*
 * Copyright (C) 2025 mpvQC developers
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

import QtQuick
import QtTest

import "MpvqcStateReducer.js" as StateReducer

TestCase {
    name: "MpvqcStateReducer"

    function makeChange(docs, vid) {
        return {
            documents: docs,
            video: vid
        };
    }

    // ───────────────────────────────
    // Event: SAVE
    // ───────────────────────────────

    function test_event_SAVE_data() {
        return [
            {
                tag: "fromInitial_setsDocument_savedTrue",
                start: StateReducer.initialState(null),
                event: {
                    type: "SAVE",
                    document: "/doc1"
                },
                expected: {
                    kind: "other",
                    document: "/doc1",
                    video: null,
                    saved: true
                }
            },
            {
                tag: "fromOther_replacesDocument_keepsVideo_setsSavedTrue",
                start: {
                    kind: "other",
                    document: "/doc1",
                    video: "/video1",
                    saved: false
                },
                event: {
                    type: "SAVE",
                    document: "/doc2"
                },
                expected: {
                    kind: "other",
                    document: "/doc2",
                    video: "/video1",
                    saved: true
                }
            }
        ];
    }

    function test_event_SAVE(data) {
        const s = StateReducer.reducer(data.start, data.event);
        compare(s.kind, data.expected.kind, data.tag);
        compare(s.document, data.expected.document, data.tag);
        compare(s.video, data.expected.video, data.tag);
        compare(s.saved, data.expected.saved, data.tag);
    }

    // ───────────────────────────────
    // Event: CHANGE
    // ───────────────────────────────

    function test_event_CHANGE_data() {
        return [
            {
                tag: "fromInitial_transitionsToOther_unsaved",
                start: StateReducer.initialState(null),
                event: {
                    type: "CHANGE"
                },
                expected: {
                    kind: "other",
                    document: null,
                    video: null,
                    saved: false
                }
            },
            {
                tag: "fromOtherUnsaved_keepsFields_unsaved",
                start: {
                    kind: "other",
                    document: "/doc1",
                    video: "/video1",
                    saved: false
                },
                event: {
                    type: "CHANGE"
                },
                expected: {
                    kind: "other",
                    document: "/doc1",
                    video: "/video1",
                    saved: false
                }
            },
            {
                tag: "fromOtherSaved_keepsFields_unsaved",
                start: {
                    kind: "other",
                    document: "/doc1",
                    video: "/video1",
                    saved: true
                },
                event: {
                    type: "CHANGE"
                },
                expected: {
                    kind: "other",
                    document: "/doc1",
                    video: "/video1",
                    saved: false
                }
            }
        ];
    }

    function test_event_CHANGE(data) {
        const s = StateReducer.reducer(data.start, data.event);
        compare(s.kind, data.expected.kind, data.tag);
        compare(s.document, data.expected.document, data.tag);
        compare(s.video, data.expected.video, data.tag);
        compare(s.saved, data.expected.saved, data.tag);
    }

    // ───────────────────────────────
    // Event: RESET
    // ───────────────────────────────

    function test_event_RESET_data() {
        return [
            {
                tag: "fromInitial_staysInitial_keepsNulls_savedTrue",
                start: StateReducer.initialState(null),
                event: {
                    type: "RESET"
                },
                expected: {
                    kind: "initial",
                    document: null,
                    video: null,
                    saved: true
                }
            },
            {
                tag: "fromOther_returnsToInitial_keepsVideo_clearsDocument_savedTrue",
                start: {
                    kind: "other",
                    document: "/doc1",
                    video: "/video1",
                    saved: false
                },
                event: {
                    type: "RESET"
                },
                expected: {
                    kind: "initial",
                    document: null,
                    video: "/video1",
                    saved: true
                }
            }
        ];
    }

    function test_event_RESET(data) {
        const s = StateReducer.reducer(data.start, data.event);
        compare(s.kind, data.expected.kind, data.tag);
        compare(s.document, data.expected.document, data.tag);
        compare(s.video, data.expected.video, data.tag);
        compare(s.saved, data.expected.saved, data.tag);
    }

    // ───────────────────────────────
    // Event: IMPORT (from initial)
    // ───────────────────────────────

    function test_event_IMPORT_fromInitial_data() {
        return [
            {
                tag: "onlyVideo_staysInitial_updatesVideo_savedTrue",
                start: StateReducer.initialState(null),
                change: makeChange([], "/video1"),
                expected: {
                    kind: "initial",
                    document: null,
                    video: "/video1",
                    saved: true
                }
            },
            {
                tag: "onlyVideo_replacesExistingInitialVideo",
                start: StateReducer.initialState("/video0"),
                change: makeChange([], "/video1"),
                expected: {
                    kind: "initial",
                    document: null,
                    video: "/video1",
                    saved: true
                }
            },
            {
                tag: "oneDocumentAndVideo_becomesOther_savedTrue",
                start: StateReducer.initialState("/video0"),
                change: makeChange(["/doc1"], "/video1"),
                expected: {
                    kind: "other",
                    document: "/doc1",
                    video: "/video1",
                    saved: true
                }
            },
            {
                tag: "multipleDocuments_noVideo_becomesOther_unsaved_keepsInitialVideo",
                start: StateReducer.initialState("/video0"),
                change: makeChange(["/doc1", "/doc2"], null),
                expected: {
                    kind: "other",
                    document: null,
                    video: "/video0",
                    saved: false
                }
            }
        ];
    }

    function test_event_IMPORT_fromInitial(data) {
        const s = StateReducer.reducer(data.start, {
            type: "IMPORT",
            change: data.change
        });
        compare(s.kind, data.expected.kind, data.tag);
        compare(s.document, data.expected.document, data.tag);
        compare(s.video, data.expected.video, data.tag);
        compare(s.saved, data.expected.saved, data.tag);
    }

    // ───────────────────────────────
    // Event: IMPORT (from other)
    // ───────────────────────────────

    function test_event_IMPORT_fromOther_data() {
        return [
            {
                tag: "sameVideo_onlyVideo_keepsStateWhenDocNull",
                start: {
                    kind: "other",
                    document: null,
                    video: "/video1",
                    saved: true
                },
                change: makeChange([], "/video1"),
                expected: {
                    kind: "other",
                    document: null,
                    video: "/video1",
                    saved: true
                }
            },
            {
                tag: "sameVideo_onlyVideo_keepsDocAndSaved",
                start: {
                    kind: "other",
                    document: "/doc1",
                    video: "/video1",
                    saved: true
                },
                change: makeChange([], "/video1"),
                expected: {
                    kind: "other",
                    document: "/doc1",
                    video: "/video1",
                    saved: true
                }
            },
            {
                tag: "differentVideo_onlyVideo_clearsDoc_setsUnsaved",
                start: {
                    kind: "other",
                    document: "/doc1",
                    video: "/video0",
                    saved: true
                },
                change: makeChange([], "/video1"),
                expected: {
                    kind: "other",
                    document: null,
                    video: "/video1",
                    saved: false
                }
            },
            {
                tag: "docAndVideo_clearsDoc_setsVideo_unsaved",
                start: {
                    kind: "other",
                    document: "/doc1",
                    video: "/video0",
                    saved: true
                },
                change: makeChange(["/doc2"], "/video1"),
                expected: {
                    kind: "other",
                    document: null,
                    video: "/video1",
                    saved: false
                }
            }
        ];
    }

    function test_event_IMPORT_fromOther(data) {
        const s = StateReducer.reducer(data.start, {
            type: "IMPORT",
            change: data.change
        });
        compare(s.kind, data.expected.kind, data.tag);
        compare(s.document, data.expected.document, data.tag);
        compare(s.video, data.expected.video, data.tag);
        compare(s.saved, data.expected.saved, data.tag);
    }

    // ───────────────────────────────
    // Unknowns
    // ───────────────────────────────

    function test_unknownEvent_throws_data() {
        return [
            {
                tag: "unknownEvent",
                start: StateReducer.initialState(null),
                event: {
                    type: "NOPE"
                }
            }
        ];
    }

    function test_unknownEvent_throws(data) {
        let threw = false;
        try {
            StateReducer.reducer(data.start, data.event);
        } catch (e) {
            threw = true;
        }
        verify(threw, data.tag);
    }

    function test_unknownStateKind_throws_data() {
        return [
            {
                tag: "unknownState",
                badState: {
                    kind: "???",
                    document: null,
                    video: null,
                    saved: true
                }
            }
        ];
    }

    function test_unknownStateKind_throws(data) {
        let threw = false;
        try {
            StateReducer.reducer(data.badState, {
                type: "IMPORT",
                change: makeChange([], null)
            });
        } catch (e) {
            threw = true;
        }
        verify(threw, data.tag);
    }
}
