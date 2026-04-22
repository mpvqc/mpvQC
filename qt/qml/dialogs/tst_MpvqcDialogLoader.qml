// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtTest
import QtQuick

TestCase {
    id: testCase

    width: 1280
    height: 720
    visible: true
    when: windowShown
    name: "MpvqcDialogLoader"

    Component {
        id: signalSpy

        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcDialogLoader {}
    }

    function makeControl(): MpvqcDialogLoader {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);
        return control;
    }

    function makeSpy(target: MpvqcDialogLoader, signalName: string): SignalSpy {
        const spy = createTemporaryObject(signalSpy, testCase, {
            target: target,
            signalName: signalName
        });
        verify(spy);
        return spy;
    }

    function waitUntilOpened(control: Item): void {
        tryVerify(() => control.item);
        waitForRendering(control.item?.contentItem);
        tryVerify(() => control.item.opened);
    }

    function test_openAboutDialog() {
        const control = makeControl();
        control.openAboutDialog();
        waitUntilOpened(control);
    }

    function test_openAppearanceDialog() {
        const control = makeControl();
        control.openAppearanceDialog();
        waitUntilOpened(control);
    }

    function test_openBackupSettingsDialog() {
        const control = makeControl();
        control.openBackupSettingsDialog();
        waitUntilOpened(control);
    }

    function test_openCommentTypesDialog() {
        const control = makeControl();
        control.openCommentTypesDialog();
        waitUntilOpened(control);
    }

    function test_openEditInputDialog() {
        const control = makeControl();
        control.openEditInputDialog();
        waitUntilOpened(control);
    }

    function test_openEditMpvDialog() {
        const control = makeControl();
        control.openEditMpvDialog();
        waitUntilOpened(control);
    }

    function test_openExportSettingsDialog() {
        const control = makeControl();
        control.openExportSettingsDialog();
        waitUntilOpened(control);
    }

    function test_openImportSettingsDialog() {
        const control = makeControl();
        control.openImportSettingsDialog();
        waitUntilOpened(control);
    }

    function test_openImportConfirmationDialog() {
        const control = makeControl();
        const videos = JSON.stringify([
            {
                path: "/tmp/video.mp4",
                filename: "video.mp4",
                fromDocument: false,
                fromSubtitle: false
            }
        ]);
        const subtitles = JSON.stringify([
            {
                path: "/tmp/subtitle.srt",
                filename: "subtitle.srt",
                checked: true
            }
        ]);
        control.openImportConfirmationDialog(videos, subtitles);
        waitUntilOpened(control);
    }

    function test_openShortcutsDialog() {
        const control = makeControl();
        control.openShortcutsDialog();
        waitUntilOpened(control);
    }

    function test_dialogClosed() {
        const control = makeControl();
        const spy = makeSpy(control, "dialogClosed");

        control.openAboutDialog();
        waitUntilOpened(control);
        control.item.close();

        tryVerify(() => !control.item, 1000);
        compare(spy.count, 1);
    }
}
