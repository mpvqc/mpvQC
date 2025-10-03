// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

Loader {
    id: root

    required property bool isLayoutMirroringEnabled

    readonly property url aboutDialog: Qt.resolvedUrl("../dialogs/MpvqcAboutDialog.qml")
    readonly property url appearanceDialog: Qt.resolvedUrl("../dialogs/MpvqcAppearanceDialog.qml")
    readonly property url backupSettingsDialog: Qt.resolvedUrl("../dialogs/MpvqcBackupDialog.qml")
    readonly property url commentTypeDialog: Qt.resolvedUrl("../dialogs/MpvqcCommentTypesDialog.qml")
    readonly property url editInputDialog: Qt.resolvedUrl("../dialogs/MpvqcEditInputDialog.qml")
    readonly property url editMpvDialog: Qt.resolvedUrl("../dialogs/MpvqcEditMpvDialog.qml")
    readonly property url exportSettingsDialog: Qt.resolvedUrl("../dialogs/MpvqcExportSettingsDialog.qml")
    readonly property url importSettingsDialog: Qt.resolvedUrl("../dialogs/MpvqcImportSettingsDialog.qml")
    readonly property url shortcutsDialog: Qt.resolvedUrl("../dialogs/MpvqcShortcutDialog.qml")

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
            parent: root.parent
        });
        active = true;
    }

    function openImportSettingsDialog(): void {
        setSource(importSettingsDialog, {
            parent: root.parent
        });
        active = true;
    }

    function openShortcutsDialog(): void {
        setSource(shortcutsDialog, {
            parent: root.parent
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
        target: root.item
        property: "isMirrored"
        value: root.isLayoutMirroringEnabled
        restoreMode: Binding.RestoreNone
    }
}
