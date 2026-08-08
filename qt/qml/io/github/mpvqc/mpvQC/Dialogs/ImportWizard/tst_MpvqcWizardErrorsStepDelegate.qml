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
