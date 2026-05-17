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
    height: 360
    visible: true
    when: windowShown
    name: "MpvqcWizardErrorsStep"

    Component {
        id: objectUnderTest

        MpvqcWizardErrorsStep {
            id: step

            anchors.fill: parent

            property alias documentsModel: _documents

            viewModel: QtObject {
                readonly property ListModel documents: _documents
            }

            ListModel {
                id: _documents
            }
        }
    }

    function makeControl(properties = {}): Item {
        const step = createTemporaryObject(objectUnderTest, testCase, properties);
        verify(step);
        return step;
    }

    function seed(step, rows): void {
        step.documentsModel.clear();
        for (const row of rows) {
            step.documentsModel.append(row);
        }
    }

    function findListView(step): ListView {
        const list = findChild(step, "errorList");
        verify(list);
        return list;
    }

    function test_delegateShowsFilenameOnly(): void {
        const step = makeControl();
        seed(step, [
            {
                filename: "broken.qc",
                fullPath: "/full/path/to/broken.qc"
            }
        ]);
        const list = findListView(step);
        tryCompare(list, "count", 1);
        waitForRendering(list);
        const item = list.itemAtIndex(0);
        verify(item);
        compare(item.text, "broken.qc");
    }

    function test_delegateExposesFullPathAsTooltip(): void {
        const step = makeControl();
        seed(step, [
            {
                filename: "broken.qc",
                fullPath: "/full/path/to/broken.qc"
            }
        ]);
        const list = findListView(step);
        tryCompare(list, "count", 1);
        waitForRendering(list);
        const item = list.itemAtIndex(0);
        verify(item);
        compare(item.ToolTip.text, "/full/path/to/broken.qc");
    }
}
