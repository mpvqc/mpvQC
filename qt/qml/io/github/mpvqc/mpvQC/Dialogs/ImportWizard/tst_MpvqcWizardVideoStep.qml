// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtTest

TestCase {
    id: testCase

    width: 500
    height: 500
    visible: true
    when: windowShown
    name: "MpvqcWizardVideoStep"

    Component {
        id: objectUnderTest

        MpvqcWizardVideoStep {
            id: _step

            anchors.fill: parent

            property alias rowsModel: _rows
            property int selected: 0

            viewModel: QtObject {
                readonly property ListModel candidates: _rows
                property int selectedIndex: _step.selected
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

    function candidate(filename, fullPath): var {
        return {
            filename: filename,
            fullPath: fullPath,
            foundInDocument: false,
            foundInSubtitle: false,
            isNoVideo: false
        };
    }

    function findListView(step): ListView {
        const list = findChild(step, "videoList");
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

    function test_clickingRowUpdatesSelectedIndex_data(): var {
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

    function test_clickingRowUpdatesSelectedIndex(data): void {
        const step = makeControl();
        seed(step, [candidate("a.mp4", "/movies/a.mp4"), candidate("b.mkv", "/movies/b.mkv"), candidate("c.mp4", "/movies/c.mp4"),]);
        mouseClick(rowAt(step, data.rowIndex));
        compare(step.viewModel.selectedIndex, data.rowIndex);
    }
}
