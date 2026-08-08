// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls // qmllint disable unused-imports
import QtTest

TestCase {
    id: testCase

    width: 500
    height: 500
    visible: true
    when: windowShown
    name: "MpvqcWizardSubtitlesStep"

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
            fullPath: `/subtitles/${filename}`,
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
        ];
    }

    function test_clickingRowCallsToggle(data): void {
        const step = makeControl();
        seed(step, [entry("a.srt", true), entry("b.srt", false), entry("c.ass", true)]);
        mouseClick(rowAt(step, data.rowIndex));
        compare(step.viewModel.toggleCount, 1);
        compare(step.viewModel.lastToggleIndex, data.rowIndex);
    }

    function test_clickingRowIndicatorCallsToggle_data(): var {
        return [
            {
                tag: "first",
                rowIndex: 0
            },
            {
                tag: "second",
                rowIndex: 1
            },
        ];
    }

    function test_clickingRowIndicatorCallsToggle(data): void {
        const step = makeControl();
        seed(step, [entry("a.srt", true), entry("b.srt", false), entry("c.ass", true)]);
        const row = rowAt(step, data.rowIndex);
        const indicator = findChild(row, "checkIndicator");
        verify(indicator);
        mouseClick(indicator);
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

    function test_rowsRenderTheModelRoles(): void {
        const step = makeControl();
        seed(step, [entry("a.srt", true), entry("b.srt", false)]);
        const row = rowAt(step, 1);
        const label = findChild(row, "label");
        const indicator = findChild(row, "checkIndicator");
        verify(label);
        verify(indicator);
        compare(label.text, "b.srt");
        compare(row.ToolTip.text, "/subtitles/b.srt");
        compare(indicator.checked, false);
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

    function test_selectAllIndicatorReflectsTriState_data(): var {
        return [
            {
                tag: "all-checked",
                triState: Qt.Checked,
                expectChecked: true,
                expectPartial: false
            },
            {
                tag: "some-checked",
                triState: Qt.PartiallyChecked,
                expectChecked: false,
                expectPartial: true
            },
            {
                tag: "none-checked",
                triState: Qt.Unchecked,
                expectChecked: false,
                expectPartial: false
            },
        ];
    }

    function test_selectAllSitsOnTheMirroredSideUnderRightToLeftLayouts(): void {
        const step = makeControl({
            "LayoutMirroring.enabled": true,
            "LayoutMirroring.childrenInherit": true
        });
        seed(step, [entry("a.srt", true), entry("b.srt", true)]);
        const selectAll = findChild(step, "selectAll");
        const question = findChild(step, "question");
        verify(selectAll);
        verify(question);
        waitForRendering(step);
        verify(selectAll.mapToItem(step, 0, 0).x < question.mapToItem(step, 0, 0).x);
        compare(question.effectiveHorizontalAlignment, Text.AlignRight);
    }

    function test_selectAllIndicatorReflectsTriState(data): void {
        const step = makeControl();
        seed(step, [entry("a.srt", true), entry("b.srt", true)]);
        step.viewModel.selectAllTriState = data.triState;
        const indicator = findChild(step, "selectAllIndicator");
        verify(indicator);
        tryCompare(indicator, "checked", data.expectChecked);
        tryCompare(indicator, "partial", data.expectPartial);
    }

    Component {
        id: objectUnderTest

        MpvqcWizardSubtitlesStep {
            property alias rowsModel: _rows

            anchors.fill: parent

            viewModel: QtObject {
                readonly property ListModel subtitles: _rows

                property int selectAllTriState: Qt.Unchecked
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
}
