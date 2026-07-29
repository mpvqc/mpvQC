// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Python

TestCase {
    id: testCase

    width: 1280
    height: 720
    visible: true
    when: windowShown
    name: "MpvqcDialogLoader"

    readonly property MpvqcTestBridge bridge: MpvqcTestBridge {}

    function makeControl(): MpvqcDialogLoader {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);
        return control;
    }

    function waitUntilOpened(control: Item): void {
        tryVerify(() => control.item);
        waitForRendering(control.item?.contentItem);
        tryVerify(() => control.item.opened);
    }

    function test_openDialog_data(): var {
        return [
            {
                tag: "about",
                open: control => control.openDialog(MpvqcDialogKind.DialogKind.ABOUT),
                objectName: "aboutDialog"
            },
            {
                tag: "appearance",
                open: control => control.openDialog(MpvqcDialogKind.DialogKind.APPEARANCE),
                objectName: "appearanceDialog"
            },
            {
                tag: "backup-settings",
                open: control => control.openDialog(MpvqcDialogKind.DialogKind.BACKUP_SETTINGS),
                objectName: "backupDialog"
            },
            {
                tag: "comment-types",
                open: control => control.openDialog(MpvqcDialogKind.DialogKind.COMMENT_TYPES),
                objectName: "commentTypesDialog"
            },
            {
                tag: "edit-input-config",
                open: control => control.openDialog(MpvqcDialogKind.DialogKind.EDIT_INPUT_CONFIG),
                objectName: "editInputDialog"
            },
            {
                tag: "edit-mpv-config",
                open: control => control.openDialog(MpvqcDialogKind.DialogKind.EDIT_MPV_CONFIG),
                objectName: "editMpvDialog"
            },
            {
                tag: "export-settings",
                open: control => control.openDialog(MpvqcDialogKind.DialogKind.EXPORT_SETTINGS),
                objectName: "exportSettingsDialog"
            },
            {
                tag: "import-settings",
                open: control => control.openDialog(MpvqcDialogKind.DialogKind.IMPORT_SETTINGS),
                objectName: "importSettingsDialog"
            },
            {
                tag: "import-wizard",
                open: control => control.openImportWizardDialog(testCase.bridge.buildWizardViewModel("all-steps")),
                objectName: "importWizardDialog"
            },
            {
                tag: "keyboard-shortcuts",
                open: control => control.openDialog(MpvqcDialogKind.DialogKind.KEYBOARD_SHORTCUTS),
                objectName: "shortcutsDialog"
            }
        ];
    }

    function test_openDialog(data): void {
        const control = makeControl();

        data.open(control);

        waitUntilOpened(control);
        compare(control.item.objectName, data.objectName);
        testCase.bridge.waitForBackgroundJobs();
    }

    Component {
        id: objectUnderTest

        MpvqcDialogLoader {}
    }
}
