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
    height: 360
    visible: true
    when: windowShown
    name: "MpvqcWizardErrorsStep"

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

    function findRows(step): Item {
        const rows = findChild(step, "errorRows");
        verify(rows);
        return rows;
    }

    function findHeader(step): Item {
        const header = findChild(step, "errorsHeader");
        verify(header);
        return header;
    }

    function rejectedDocument(name): var {
        return {
            filename: name,
            fullPath: `/documents/${name}`,
            reason: `${name} is broken`
        };
    }

    function test_listsOneRowPerRejectedDocument(): void {
        const step = makeControl();
        seed(step, [rejectedDocument("broken.qc"), rejectedDocument("future.json")]);
        const rows = findRows(step);
        tryCompare(rows, "count", 2);
        waitForRendering(step);
        compare(rows.itemAt(0).filename, "broken.qc");
        compare(rows.itemAt(1).filename, "future.json");
        compare(rows.itemAt(0).reason, "broken.qc is broken");
        compare(rows.itemAt(0).fullPath, "/documents/broken.qc");
    }

    function test_headerCountsRejectedDocuments(): void {
        const step = makeControl();

        seed(step, [rejectedDocument("broken.qc")]);
        tryCompare(findRows(step), "count", 1);
        const single = findHeader(step).text;
        verify(single.includes("1"), `header should name the count, was '${single}'`);

        seed(step, [rejectedDocument("broken.qc"), rejectedDocument("future.json")]);
        tryCompare(findRows(step), "count", 2);
        const plural = findHeader(step).text;
        verify(plural.includes("2"), `header should name the count, was '${plural}'`);
    }

    function test_questionMirrorsUnderRightToLeftLayouts(): void {
        const step = makeControl({
            "LayoutMirroring.enabled": true,
            "LayoutMirroring.childrenInherit": true
        });
        const question = findChild(step, "question");
        verify(question);
        compare(question.effectiveHorizontalAlignment, Text.AlignRight);
    }

    Component {
        id: objectUnderTest

        MpvqcWizardErrorsStep {
            id: step

            property alias documentsModel: _documents

            anchors.fill: parent

            viewModel: QtObject {
                readonly property ListModel documents: _documents
            }

            ListModel {
                id: _documents
            }
        }
    }
}
