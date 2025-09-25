// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

Loader {
    id: root

    required property var mpvqcApplication

    readonly property url aboutDialog: Qt.resolvedUrl("../dialogs/about/MpvqcAboutDialogView.qml")
    readonly property url appearanceDialog: Qt.resolvedUrl("../dialogs/appearance/MpvqcAppearanceDialogView.qml")
    readonly property url backupSettingsDialog: Qt.resolvedUrl("../dialogs/backup/MpvqcBackupDialogView.qml")
    readonly property url commentTypeDialog: Qt.resolvedUrl("../dialogs/commenttypes/MpvqcCommentTypesDialogView.qml")
    readonly property url editInputDialog: Qt.resolvedUrl("../dialogs/editinput/MpvqcEditInputDialogView.qml")
    readonly property url editMpvDialog: Qt.resolvedUrl("../dialogs/editmpv/MpvqcEditMpvDialogView.qml")
    readonly property url exportSettingsDialog: Qt.resolvedUrl("../dialogs/export/MpvqcDialogExport.qml")
    readonly property url importSettingsDialog: Qt.resolvedUrl("../dialogs/import/MpvqcDialogImport.qml")
    readonly property url shortcutsDialog: Qt.resolvedUrl("../dialogs/shortcuts/MpvqcDialogShortcuts.qml")

    readonly property bool isNewDialogBase: root.item === aboutDialog //
    || root.item === appearanceDialog //
    || root.item === backupSettingsDialog //
    || root.item === commentTypeDialog //
    || root.item === editInputDialog //
    || root.item === editMpvDialog //

    signal dialogClosed

    asynchronous: true
    active: false
    visible: active

    function openAboutDialog(): void {
        setSource(aboutDialog, {
            parent: root.parent
        });
        active = true;
    }

    function openAppearanceDialog(): void {
        setSource(appearanceDialog, {
            parent: root.parent
        });
        active = true;
    }

    function openBackupSettingsDialog(): void {
        setSource(backupSettingsDialog, {
            parent: root.parent
        });
        active = true;
    }

    function openCommentTypesDialog(): void {
        setSource(commentTypeDialog, {
            parent: root.parent
        });
        active = true;
    }

    function openEditInputDialog(): void {
        setSource(editInputDialog, {
            parent: root.parent
        });
        active = true;
    }

    function openEditMpvDialog(): void {
        setSource(editMpvDialog, {
            parent: root.parent
        });
        active = true;
    }

    function openExportSettingsDialog(): void {
        setSource(exportSettingsDialog, {
            mpvqcApplication: root.mpvqcApplication
        });
        active = true;
    }

    function openImportSettingsDialog(): void {
        setSource(importSettingsDialog, {
            mpvqcApplication: root.mpvqcApplication
        });
        active = true;
    }

    function openShortcutsDialog(): void {
        setSource(shortcutsDialog, {
            mpvqcApplication: root.mpvqcApplication
        });
        active = true;
    }

    onLoaded: item.open() // qmllint disable

    Connections {
        target: root.item

        function onClosed(): void {
            root.active = false;
            root.source = "";
            root.dialogClosed();
        }
    }

    Binding {
        when: root.isNewDialogBase
        target: root.item
        property: "isMirrored"
        value: root.mpvqcApplication.LayoutMirroring.enabled
        restoreMode: Binding.RestoreNone
    }
}
