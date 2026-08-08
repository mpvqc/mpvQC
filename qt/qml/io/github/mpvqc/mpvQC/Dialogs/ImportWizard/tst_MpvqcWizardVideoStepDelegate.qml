// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls // qmllint disable unused-imports
import QtTest

import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    width: 500
    height: 300
    visible: true
    when: windowShown
    name: "MpvqcWizardVideoStepDelegate"

    function makeControl(properties = {}): Item {
        const delegate = createTemporaryObject(objectUnderTest, testCase, properties);
        verify(delegate);
        waitForRendering(delegate);
        return delegate;
    }

    function test_labelTextReflectsRowKind_data(): var {
        return [
            {
                tag: "candidate-shows-filename",
                isNoVideo: false,
                expectedText: "foobar.mp4"
            },
            {
                tag: "sentinel-shows-skip-label",
                isNoVideo: true,
                expectedText: qsTranslate("ImportWizardDialog", "Skip video")
            },
        ];
    }

    function test_labelTextReflectsRowKind(data): void {
        const delegate = makeControl({
            isNoVideo: data.isNoVideo
        });
        const label = findChild(delegate, "label");
        verify(label);
        compare(label.text, data.expectedText);
    }

    function test_originPillsReflectFlags_data(): var {
        return [
            {
                tag: "from-document-only",
                foundInDocument: true,
                foundInSubtitle: false,
                expectDoc: true,
                expectSub: false
            },
            {
                tag: "from-subtitle-only",
                foundInDocument: false,
                foundInSubtitle: true,
                expectDoc: false,
                expectSub: true
            },
            {
                tag: "both",
                foundInDocument: true,
                foundInSubtitle: true,
                expectDoc: true,
                expectSub: true
            },
        ];
    }

    function test_originPillsReflectFlags(data): void {
        const delegate = makeControl({
            foundInDocument: data.foundInDocument,
            foundInSubtitle: data.foundInSubtitle
        });
        const docPill = findChild(delegate, "fromDocumentPill");
        const subPill = findChild(delegate, "fromSubtitlePill");
        verify(docPill);
        verify(subPill);
        compare(docPill.visible, data.expectDoc);
        compare(subPill.visible, data.expectSub);
    }

    function test_originPillsFollowRowSelection(): void {
        const delegate = makeControl({
            foundInDocument: true
        });
        const docPill = findChild(delegate, "fromDocumentPill");
        verify(docPill);
        compare(docPill.selected, false);

        delegate.selected = true;

        compare(docPill.selected, true);
    }

    function test_radioReflectsSelected_data(): var {
        return [
            {
                tag: "selected",
                selected: true,
                expectSelected: true
            },
            {
                tag: "unselected",
                selected: false,
                expectSelected: false
            },
        ];
    }

    function test_radioReflectsSelected(data): void {
        const delegate = makeControl({
            selected: data.selected
        });
        const radio = findChild(delegate, "radioIndicator");
        verify(radio);
        compare(radio.selected, data.expectSelected);
    }

    function test_rowTooltipShowsFullPath(): void {
        const delegate = makeControl();
        compare(delegate.ToolTip.text, "/movies/foobar.mp4");
    }

    function test_theRowSizesItselfThroughItsImplicitHeight(): void {
        const delegate = makeControl();
        compare(delegate.implicitHeight, MpvqcConstants.listRowHeight);
        compare(delegate.height, delegate.implicitHeight);
    }

    function test_longFilenameWrapsPastTwoLines(): void {
        const delegate = makeControl({
            filename: "[Group] A Very Long Release Name With Plenty Of Words And A Second Batch Of Words That Keeps Going (BD 1080p HEVC FLAC 10bit Dual Audio) [DEADBEEF].mkv"
        });
        const label = findChild(delegate, "label");
        verify(label);
        verify(label.lineCount > 2);
    }

    Component {
        id: objectUnderTest

        MpvqcWizardVideoStepDelegate {
            width: testCase.width

            index: 0
            filename: "foobar.mp4"
            fullPath: "/movies/foobar.mp4"
            foundInDocument: false
            foundInSubtitle: false
            isNoVideo: false
            selected: false
        }
    }
}
