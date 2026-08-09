// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    width: 500
    height: 360
    visible: true
    when: windowShown
    name: "MpvqcWizardSessionStep"

    function makeControl(properties = {}): Item {
        const step = createTemporaryObject(objectUnderTest, testCase, properties);
        verify(step);
        waitForRendering(step);
        return step;
    }

    function test_defaultsToMerge(): void {
        const step = makeControl();
        const merge = findChild(findChild(step, "mergeRow"), "radio");
        const replace = findChild(findChild(step, "replaceRow"), "radio");
        verify(merge.selected);
        verify(!replace.selected);
    }

    function test_togglingReplaceUpdatesViewModelMode(): void {
        const step = makeControl();
        const replace = findChild(step, "replaceRow");
        mouseClick(replace);
        compare(step.viewModel.mode, MpvqcImportWizardSessionMode.SessionMode.REPLACE);
    }

    function test_togglingMergeUpdatesViewModelMode(): void {
        const step = makeControl({
            sessionMode: MpvqcImportWizardSessionMode.SessionMode.REPLACE
        });
        const merge = findChild(step, "mergeRow");
        mouseClick(merge);
        compare(step.viewModel.mode, MpvqcImportWizardSessionMode.SessionMode.MERGE);
    }

    function test_clickingPastTheLabelStillSelects(): void {
        const step = makeControl();
        const replace = findChild(step, "replaceRow");
        mouseClick(replace, replace.width - 4, replace.height / 2);
        compare(step.viewModel.mode, MpvqcImportWizardSessionMode.SessionMode.REPLACE);
    }

    function test_rowsSizeThemselvesThroughTheirImplicitHeight(): void {
        const step = makeControl();
        const merge = findChild(step, "mergeRow");
        verify(merge);
        compare(merge.implicitHeight, MpvqcConstants.listRowHeight);
        compare(merge.height, merge.implicitHeight);
    }

    function test_theSelectedRowCarriesTheSelectionTint(): void {
        const step = makeControl();
        const merge = findChild(step, "mergeRow");
        const replace = findChild(step, "replaceRow");
        verify(merge);
        verify(replace);
        compare(merge.background.color, Qt.alpha(MpvqcAppearance.palette.accent, 0.16));
        compare(replace.background.color.a, 0);
    }

    function test_headerReflectsIncomingCount(): void {
        const step = makeControl({
            incomingCount: 5
        });
        const header = findChild(step, "question");
        verify(header.text.indexOf("5") >= 0);
    }

    function test_rowsMirrorUnderRightToLeftLayouts(): void {
        const step = makeControl({
            "LayoutMirroring.enabled": true,
            "LayoutMirroring.childrenInherit": true
        });
        const row = findChild(step, "mergeRow");
        verify(row);
        const radio = findChild(row, "radio");
        const label = findChild(row, "label");
        verify(radio);
        verify(label);
        verify(radio.x > label.x);
        compare(label.effectiveHorizontalAlignment, Text.AlignRight);
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

        MpvqcWizardSessionStep {
            id: _step

            property int sessionMode: MpvqcImportWizardSessionMode.SessionMode.MERGE
            property int incomingCount: 0

            anchors.fill: parent

            viewModel: QtObject {
                readonly property int incomingCommentCount: _step.incomingCount
                property int mode: _step.sessionMode
            }
        }
    }
}
