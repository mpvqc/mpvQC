// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest
import pyobjects

TestCase {
    id: testCase

    name: "Integration::HelpMenu"
    width: 1280
    height: 720
    visible: true
    when: windowShown

    TestHelpers {
        id: it

        testCase: testCase
    }

    function init(): void {
        it.resetState();
    }

    function test_checkForUpdates_opensMessageBox(): void {
        const control = it.makeControl();

        it.triggerMenuItem(control, "helpMenu", "openCheckForUpdatesMenuItem");

        it.findOpenedDialog(control, "versionCheckMessageBox");
        it.bridge.waitForBackgroundJobs();
    }

    function test_keyboardShortcuts_opensDialog(): void {
        const control = it.makeControl();

        it.triggerMenuItem(control, "helpMenu", "openKeyboardShortcutsMenuItem");

        it.findOpenedDialog(control, "shortcutsDialog");
    }

    function test_extendedExports_opensMessageBox(): void {
        const control = it.makeControl();

        it.triggerMenuItem(control, "helpMenu", "openExtendedExportsDialogMenuItem");

        it.findOpenedDialog(control, "extendedExportMessageBox");
    }

    function test_appDataFolder_opensExternalUrl(): void {
        const control = it.makeControl();

        it.triggerMenuItem(control, "helpMenu", "openAppDataFolderMenuItem");

        tryVerify(() => it.bridge.openedDesktopUrls().includes("mpvqc-test://app-data-folder"));
    }

    function test_about_opensDialog(): void {
        const control = it.makeControl();

        it.triggerMenuItem(control, "helpMenu", "openAboutDialogMenuItem");

        it.findOpenedDialog(control, "aboutDialog");
    }
}
