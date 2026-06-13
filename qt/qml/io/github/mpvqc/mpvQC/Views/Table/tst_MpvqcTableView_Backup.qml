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

    readonly property MpvqcTestBridge bridge: MpvqcTestBridge {}

    readonly property Component control: Component {
        MpvqcTableView {
            backupEnabled: true

            height: testCase.height
            width: testCase.width
        }
    }

    width: 600
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcTableView::Backup"

    function initTestCase(): void {
        MpvqcLabelWidthCalculator.timeLabelWidth = 50;
        MpvqcLabelWidthCalculator.commentTypesLabelWidth = 150;
    }

    function init(): void {
        bridge.resetState();
    }

    function cleanup(): void {
        bridge.waitForBackgroundJobs();
    }

    function makeControl(): var {
        const view = createTemporaryObject(control, testCase);
        verify(view);
        waitForRendering(view);
        return view;
    }

    function test_timerWritesSeededCommentToBackupZip(): void {
        const view = makeControl();

        bridge.importComments([
            {
                "time": 1,
                "commentType": "Comment Type 1",
                "comment": "BackupIntegrationMarker"
            }
        ]);

        tryVerify(() => {
            bridge.waitForBackgroundJobs();
            return bridge.backupWriteCount() === 1;
        }, 5000, "backup never reached disk");
        verify(bridge.backupArchiveAnyEntryContains("BackupIntegrationMarker"), "archive missing the seeded marker");
    }
}
