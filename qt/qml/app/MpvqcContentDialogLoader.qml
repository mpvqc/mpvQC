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
    readonly property url backupSettingsDialog: Qt.resolvedUrl("../dialogs/backup/MpvqcDialogBackup.qml")
    readonly property url commentTypeDialog: Qt.resolvedUrl("../dialogs/commenttypes/MpvqcDialogCommentTypes.qml")
    readonly property url editInputDialog: Qt.resolvedUrl("../dialogs/editinput/MpvqcDialogEditInput.qml")
    readonly property url editMpvDialog: Qt.resolvedUrl("../dialogs/editmpv/MpvqcDialogEditMpv.qml")
    readonly property url exportSettingsDialog: Qt.resolvedUrl("../dialogs/export/MpvqcDialogExport.qml")
    readonly property url importSettingsDialog: Qt.resolvedUrl("../dialogs/import/MpvqcDialogImport.qml")
    readonly property url shortcutsDialog: Qt.resolvedUrl("../dialogs/shortcuts/MpvqcDialogShortcuts.qml")

    readonly property bool isNewDialogBase: root.item === aboutDialog //
    || root.item === appearanceDialog

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
            mpvqcSettings: root.mpvqcApplication.mpvqcSettings,
            mpvqcTheme: root.mpvqcApplication.mpvqcTheme,
            parent: root.parent
        });
        active = true;
    }

    function openBackupSettingsDialog(): void {
        setSource(backupSettingsDialog, {
            mpvqcApplication: root.mpvqcApplication
        });
        active = true;
    }

    function openCommentTypesDialog(): void {
        setSource(commentTypeDialog, {
            mpvqcApplication: root.mpvqcApplication
        });
        active = true;
    }

    function openEditInputDialog(): void {
        setSource(editInputDialog, {
            mpvqcApplication: root.mpvqcApplication
        });
        active = true;
    }

    function openEditMpvDialog(): void {
        setSource(editMpvDialog, {
            mpvqcApplication: root.mpvqcApplication
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
        enabled: root.item
        target: root.item

        function onClosed(): void {
            root.active = false;
            root.source = "";
            root.dialogClosed();
        }
    }

    Binding {
        when: root.source === root.aboutDialog
        target: root.item
        property: "contentHeight"
        value: Math.min(1080, root.mpvqcApplication.height * 0.65)
        restoreMode: Binding.RestoreNone
    }

    Binding {
        when: root.isNewDialogBase
        target: root.item
        property: "isMirrored"
        value: root.mpvqcApplication.LayoutMirroring.enabled
        restoreMode: Binding.RestoreNone
    }
}
