// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    width: 500
    height: 500
    visible: true
    when: windowShown
    name: "MpvqcWizardSubtitlesStep"

    Component {
        id: objectUnderTest

        MpvqcWizardSubtitlesStep {
            id: _step

            anchors.fill: parent

            property alias rowsModel: _rows
            property int triState: Qt.Unchecked

            viewModel: QtObject {
                readonly property ListModel subtitles: _rows
                property int selectAllTriState: _step.triState

                property int lastToggleIndex: -1
                property int toggleCount: 0
                property int toggleSelectAllCount: 0

                function toggle(index) {
                    lastToggleIndex = index;
                    toggleCount += 1;
                }

                function toggleSelectAll() {
                    toggleSelectAllCount += 1;
                }
            }

            ListModel {
                id: _rows
            }
        }
    }

    function makeControl(properties = {}): Item {
        const step = createTemporaryObject(objectUnderTest, testCase, properties);
        verify(step);
        return step;
    }

    function seed(step, rows): void {
        step.rowsModel.clear();
        for (const row of rows) {
            step.rowsModel.append(row);
        }
    }

    function entry(filename, isChecked): var {
        return {
            filename: filename,
            isChecked: isChecked
        };
    }

    function findListView(step): ListView {
        const list = findChild(step, "subtitleList");
        verify(list);
        return list;
    }

    function rowAt(step, index): Item {
        const list = findListView(step);
        tryCompare(list, "count", step.rowsModel.count);
        waitForRendering(list);
        const item = list.itemAtIndex(index);
        verify(item);
        return item;
    }

    function test_clickingRowCallsToggle_data(): var {
        return [
            {
                tag: "first",
                rowIndex: 0
            },
            {
                tag: "second",
                rowIndex: 1
            },
            {
                tag: "third",
                rowIndex: 2
            },
        ];
    }

    function test_clickingRowCallsToggle(data): void {
        const step = makeControl();
        seed(step, [entry("a.srt", true), entry("b.srt", false), entry("c.ass", true)]);
        mouseClick(rowAt(step, data.rowIndex));
        compare(step.viewModel.toggleCount, 1);
        compare(step.viewModel.lastToggleIndex, data.rowIndex);
    }

    function test_clickingRowCheckboxCallsToggle_data(): var {
        return [
            {
                tag: "first",
                rowIndex: 0
            },
            {
                tag: "second",
                rowIndex: 1
            },
            {
                tag: "third",
                rowIndex: 2
            },
        ];
    }

    function test_clickingRowCheckboxCallsToggle(data): void {
        const step = makeControl();
        seed(step, [entry("a.srt", true), entry("b.srt", false), entry("c.ass", true)]);
        const row = rowAt(step, data.rowIndex);
        const checkbox = findChild(row, "checkbox");
        verify(checkbox);
        mouseClick(checkbox);
        compare(step.viewModel.toggleCount, 1);
        compare(step.viewModel.lastToggleIndex, data.rowIndex);
    }

    function test_clickingSelectAllCallsToggleSelectAll(): void {
        const step = makeControl();
        seed(step, [entry("a.srt", true), entry("b.srt", true)]);
        const selectAll = findChild(step, "selectAll");
        tryVerify(() => selectAll.visible);
        mouseClick(selectAll);
        compare(step.viewModel.toggleSelectAllCount, 1);
    }

    function test_selectAllReflectsTriState_data(): var {
        return [
            {
                tag: "unchecked",
                value: Qt.Unchecked
            },
            {
                tag: "partial",
                value: Qt.PartiallyChecked
            },
            {
                tag: "checked",
                value: Qt.Checked
            },
        ];
    }

    function test_selectAllReflectsTriState(data): void {
        const step = makeControl({
            triState: data.value
        });
        const selectAll = findChild(step, "selectAll");
        compare(selectAll.checkState, data.value);
    }

    function test_rowCheckboxReflectsIsChecked_data(): var {
        return [
            {
                tag: "checked",
                isChecked: true
            },
            {
                tag: "unchecked",
                isChecked: false
            },
        ];
    }

    function test_rowCheckboxReflectsIsChecked(data): void {
        const step = makeControl();
        seed(step, [entry("a.srt", data.isChecked)]);
        const row = rowAt(step, 0);
        const checkbox = findChild(row, "checkbox");
        verify(checkbox);
        compare(checkbox.checked, data.isChecked);
    }

    function test_selectAllHiddenWhenSingleSubtitle_data(): var {
        return [
            {
                tag: "single",
                rows: [entry("only.srt", true)],
                expectVisible: false
            },
            {
                tag: "multiple",
                rows: [entry("a.srt", true), entry("b.srt", true)],
                expectVisible: true
            },
        ];
    }

    function test_selectAllHiddenWhenSingleSubtitle(data): void {
        const step = makeControl();
        seed(step, data.rows);
        const selectAll = findChild(step, "selectAll");
        verify(selectAll);
        tryCompare(selectAll, "visible", data.expectVisible);
    }
}
