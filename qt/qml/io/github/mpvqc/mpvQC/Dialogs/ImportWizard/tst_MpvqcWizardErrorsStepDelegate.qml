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
    height: 120
    visible: true
    when: windowShown
    name: "MpvqcWizardErrorsStepDelegate"

    function makeControl(properties = {}): Item {
        const delegate = createTemporaryObject(objectUnderTest, testCase, properties);
        verify(delegate);
        return delegate;
    }

    function test_rowListsFilenameAndReason(): void {
        const delegate = makeControl();
        const filename = findChild(delegate, "filenameLabel");
        const reason = findChild(delegate, "reasonLabel");
        verify(filename);
        verify(reason);
        compare(filename.text, "broken.qc");
        compare(reason.text, "mock reason");
    }

    function test_hoveringAnywhereOnTheRowShowsTheFullPath(): void {
        const delegate = makeControl();
        waitForRendering(delegate);
        compare(delegate.ToolTip.text, "/documents/broken.qc");
        verify(!delegate.ToolTip.visible);

        mouseMove(delegate, delegate.width - 4, delegate.height / 2);
        tryVerify(() => delegate.ToolTip.visible);

        mouseMove(delegate, delegate.width - 4, delegate.height + 20);
        tryVerify(() => !delegate.ToolTip.visible);
    }

    function test_iconStartsAtTheSharedRowPadding(): void {
        const delegate = makeControl();
        waitForRendering(delegate);
        const icon = findChild(delegate, "errorIcon");
        verify(icon);
        compare(icon.mapToItem(delegate, 0, 0).x, MpvqcConstants.listRowHorizontalPadding);
    }

    function test_rowNeitherClicksNorTakesFocus(): void {
        const delegate = makeControl();
        waitForRendering(delegate);
        verify(delegate.pressed === undefined, "a row that decides nothing must not be a button");
        verify(delegate.focusPolicy === Qt.NoFocus, `row must refuse focus, policy was ${delegate.focusPolicy}`);

        mouseClick(delegate);
        verify(!delegate.activeFocus);
    }

    function test_longTextWrapsAndKeepsTheIconOnTheFirstLine(): void {
        const delegate = makeControl();
        delegate.filename = "an-extremely-long-document-name-nobody-would-ever-type-by-hand-but-here-it-is.qc";
        delegate.reason = "the importer rejected this document because it names a format that no version of mpvQC has ever written";
        waitForRendering(delegate);
        const icon = findChild(delegate, "errorIcon");
        const filename = findChild(delegate, "filenameLabel");
        verify(icon);
        verify(filename);

        verify(delegate.height > MpvqcConstants.listRowHeight, `row should grow with its text, was ${delegate.height}`);
        compare(filename.elide, Text.ElideNone);
        verify(filename.lineCount > 1, "filename should wrap rather than run off the row");
        const iconBottom = icon.mapToItem(delegate, 0, icon.height).y;
        verify(iconBottom < delegate.height / 2, `icon should stay on the first line, ended at ${iconBottom}`);
    }

    function test_rowMirrorsUnderRightToLeftLayouts(): void {
        const delegate = makeControl({
            "LayoutMirroring.enabled": true,
            "LayoutMirroring.childrenInherit": true
        });
        waitForRendering(delegate);
        const icon = findChild(delegate, "errorIcon");
        const filename = findChild(delegate, "filenameLabel");
        const reason = findChild(delegate, "reasonLabel");
        verify(icon);
        verify(filename);
        verify(reason);
        verify(icon.mapToItem(delegate, 0, 0).x > filename.mapToItem(delegate, 0, 0).x);
        compare(filename.effectiveHorizontalAlignment, Text.AlignRight);
        compare(reason.effectiveHorizontalAlignment, Text.AlignRight);
    }

    Component {
        id: objectUnderTest

        MpvqcWizardErrorsStepDelegate {
            width: testCase.width

            filename: "broken.qc"
            fullPath: "/documents/broken.qc"
            reason: "mock reason"
        }
    }
}
