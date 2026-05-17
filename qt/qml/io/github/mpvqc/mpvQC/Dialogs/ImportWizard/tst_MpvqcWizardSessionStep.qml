// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Python

TestCase {
    id: testCase

    width: 500
    height: 360
    visible: true
    when: windowShown
    name: "MpvqcWizardSessionStep"

    Component {
        id: objectUnderTest

        MpvqcWizardSessionStep {
            id: _step

            anchors.fill: parent

            property int sessionMode: MpvqcImportWizardSessionMode.MERGE
            property int incomingCount: 0

            viewModel: QtObject {
                readonly property int incomingCommentCount: _step.incomingCount
                property int mode: _step.sessionMode
            }
        }
    }

    function makeControl(properties = {}): Item {
        const step = createTemporaryObject(objectUnderTest, testCase, properties);
        verify(step);
        waitForRendering(step);
        return step;
    }

    function test_defaultsToMerge(): void {
        const step = makeControl();
        const merge = findChild(step, "mergeRadio");
        const replace = findChild(step, "replaceRadio");
        verify(merge.selected);
        verify(!replace.selected);
    }

    function test_togglingReplaceUpdatesViewModelMode(): void {
        const step = makeControl();
        const replace = findChild(step, "replaceRadio");
        mouseClick(replace);
        compare(step.viewModel.mode, MpvqcImportWizardSessionMode.REPLACE);
    }

    function test_togglingMergeUpdatesViewModelMode(): void {
        const step = makeControl({
            sessionMode: MpvqcImportWizardSessionMode.REPLACE
        });
        const merge = findChild(step, "mergeRadio");
        mouseClick(merge);
        compare(step.viewModel.mode, MpvqcImportWizardSessionMode.MERGE);
    }

    function test_headerReflectsIncomingCount(): void {
        const step = makeControl({
            incomingCount: 5
        });
        const header = findChild(step, "question");
        verify(header.text.indexOf("5") >= 0);
    }
}
