// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import io.github.mpvqc.mpvQC.Python

Loader {
    id: root
    objectName: "dialogLoader"

    readonly property MpvqcDialogLoaderViewModel viewModel: MpvqcDialogLoaderViewModel {}

    readonly property url aboutDialog: Qt.resolvedUrl("MpvqcAboutDialog.qml")
    readonly property url appearanceDialog: Qt.resolvedUrl("MpvqcAppearanceDialog.qml")
    readonly property url backupSettingsDialog: Qt.resolvedUrl("MpvqcBackupDialog.qml")
    readonly property url commentTypeDialog: Qt.resolvedUrl("MpvqcCommentTypesDialog.qml")
    readonly property url editInputDialog: Qt.resolvedUrl("MpvqcEditInputDialog.qml")
    readonly property url editMpvDialog: Qt.resolvedUrl("MpvqcEditMpvDialog.qml")
    readonly property url exportSettingsDialog: Qt.resolvedUrl("MpvqcExportSettingsDialog.qml")
    readonly property url importSettingsDialog: Qt.resolvedUrl("MpvqcImportSettingsDialog.qml")
    readonly property url importConfirmationDialog: Qt.resolvedUrl("MpvqcImportConfirmationDialog.qml")
    readonly property url shortcutsDialog: Qt.resolvedUrl("MpvqcShortcutDialog.qml")

    signal dialogClosed

    asynchronous: true
    active: false
    visible: active

    function openAboutDialog(): void {
        setSource(aboutDialog);
        active = true;
    }

    function openAppearanceDialog(): void {
        setSource(appearanceDialog);
        active = true;
    }

    function openBackupSettingsDialog(): void {
        setSource(backupSettingsDialog);
        active = true;
    }

    function openCommentTypesDialog(): void {
        setSource(commentTypeDialog);
        active = true;
    }

    function openEditInputDialog(): void {
        setSource(editInputDialog);
        active = true;
    }

    function openEditMpvDialog(): void {
        setSource(editMpvDialog);
        active = true;
    }

    function openExportSettingsDialog(): void {
        setSource(exportSettingsDialog);
        active = true;
    }

    function openImportSettingsDialog(): void {
        setSource(importSettingsDialog);
        active = true;
    }

    function openImportConfirmationDialog(videosJson: string, subtitlesJson: string): void {
        setSource(importConfirmationDialog, {
            videosJson: videosJson,
            subtitlesJson: subtitlesJson
        });
        active = true;
    }

    function openShortcutsDialog(): void {
        setSource(shortcutsDialog);
        active = true;
    }

    onLoaded: item.open() // qmllint disable

    Connections {
        target: root.item
        ignoreUnknownSignals: true

        function onClosed(): void {
            root.active = false;
            root.source = "";
            root.dialogClosed();
        }

        function onImportConfirmed(selectedVideoPath: string, selectedSubtitlePaths: list<string>): void {
            root.viewModel.confirmImport(selectedVideoPath, selectedSubtitlePaths);
        }
    }

    Connections {
        target: root.viewModel

        function onImportConfirmationDialogRequested(videosJson: string, subtitlesJson: string): void {
            root.openImportConfirmationDialog(videosJson, subtitlesJson);
        }
    }
}
