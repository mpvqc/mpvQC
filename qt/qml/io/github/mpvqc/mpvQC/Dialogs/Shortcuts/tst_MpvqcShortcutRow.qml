// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    width: 400
    height: 100
    visible: true
    when: windowShown
    name: "MpvqcShortcutRow"

    Component {
        id: objectUnderTest

        MpvqcShortcutRow {
            width: 380
            label: "label"
        }
    }

    function makeControl(properties = {}): Item {
        const control = createTemporaryObject(objectUnderTest, testCase, properties);
        verify(control);
        return control;
    }

    function collectVisible(item, objectName, result = []): list<Item> {
        for (let i = 0; i < item.children.length; i++) {
            const child = item.children[i];
            if (child.objectName === objectName && child.visible) {
                result.push(child);
            }
            collectVisible(child, objectName, result);
        }
        return result;
    }

    function test_separators_data(): var {
        return [
            {
                tag: "single-key",
                sequences: [[
                        {
                            text: "E"
                        }
                    ]],
                expectedKeycaps: 1,
                expectedKeySeparators: 0,
                expectedSequenceSeparators: 0
            },
            {
                tag: "chord-joins-keys-with-plus",
                sequences: [[
                        {
                            text: "Ctrl"
                        },
                        {
                            text: "N"
                        }
                    ]],
                expectedKeycaps: 2,
                expectedKeySeparators: 1,
                expectedSequenceSeparators: 0
            },
            {
                tag: "three-key-chord",
                sequences: [[
                        {
                            text: "Ctrl"
                        },
                        {
                            text: "Shift"
                        },
                        {
                            text: "S"
                        }
                    ]],
                expectedKeycaps: 3,
                expectedKeySeparators: 2,
                expectedSequenceSeparators: 0
            },
            {
                tag: "alternatives-join-with-slash",
                sequences: [[
                        {
                            icon: "backspace"
                        }
                    ], [
                        {
                            text: "Delete"
                        }
                    ]],
                expectedKeycaps: 2,
                expectedKeySeparators: 0,
                expectedSequenceSeparators: 1
            },
            {
                tag: "mixed-text-and-icon-chord",
                sequences: [[
                        {
                            text: "Shift"
                        },
                        {
                            icon: "arrowLeft"
                        }
                    ]],
                expectedKeycaps: 2,
                expectedKeySeparators: 1,
                expectedSequenceSeparators: 0
            },
        ];
    }

    function test_separators(data): void {
        const control = makeControl({
            sequences: data.sequences
        });

        compare(collectVisible(control, "keycap").length, data.expectedKeycaps);
        compare(collectVisible(control, "keySeparator").length, data.expectedKeySeparators);
        compare(collectVisible(control, "sequenceSeparator").length, data.expectedSequenceSeparators);
    }

    function test_singleLetterAndIconKeycapsShareSize(): void {
        const control = makeControl({
            sequences: [[
                    {
                        text: "N"
                    }
                ], [
                    {
                        icon: "arrowLeft"
                    }
                ], [
                    {
                        text: "?"
                    }
                ]]
        });
        const keycaps = collectVisible(control, "keycap");
        compare(keycaps.length, 3);

        compare(keycaps[0].width, keycaps[1].width);
        compare(keycaps[1].width, keycaps[2].width);
        compare(keycaps[0].height, keycaps[1].height);
        compare(keycaps[1].height, keycaps[2].height);
    }

    function test_noteIconShownOnlyWithNote(): void {
        const withNote = makeControl({
            sequences: [[
                    {
                        text: "N"
                    }
                ]],
            note: "a caveat"
        });
        const withNoteIcon = findChild(withNote, "noteIcon");
        verify(withNoteIcon.visible);
        compare(withNoteIcon.toolTipText, "a caveat");

        const withoutNote = makeControl({
            sequences: [[
                    {
                        text: "N"
                    }
                ]]
        });
        verify(!findChild(withoutNote, "noteIcon").visible);
    }

    function test_longLabelWrapsInsteadOfPushingKeycaps(): void {
        const control = makeControl({
            label: "A very long shortcut description that does not fit on a single line ".repeat(3),
            note: "a caveat",
            sequences: [[
                    {
                        text: "Ctrl"
                    },
                    {
                        icon: "arrowLeft"
                    }
                ]]
        });
        const keycaps = collectVisible(control, "keycap");
        compare(keycaps.length, 2);

        const last = keycaps[keycaps.length - 1];
        const rightEdge = last.mapToItem(control, last.width, 0).x;
        verify(rightEdge <= control.width);
        verify(control.height > MpvqcConstants.listRowHeight);
    }

    function test_keycapsRenderTextAndIcon(): void {
        const control = makeControl({
            sequences: [[
                    {
                        icon: "backspace"
                    }
                ], [
                    {
                        text: "Delete"
                    }
                ]]
        });
        const keycaps = collectVisible(control, "keycap");
        compare(keycaps.length, 2);

        verify(keycaps[0].contentItem.icon.source.toString() !== "");
        compare(keycaps[0].text, "");

        compare(keycaps[1].text, "Delete");
        verify(keycaps[1].contentItem.icon.source.toString() === "");
    }
}
