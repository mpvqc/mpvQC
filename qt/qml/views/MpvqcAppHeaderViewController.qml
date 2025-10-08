// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import pyobjects

MpvqcAppHeaderViewModel {
    id: root

    required property var mpvqcTheme
    required property var mpvqcSettings

    required property bool isVisible
    required property bool isMaximized
    required property bool isStateSaved
    required property bool isVideoLoaded
    required property bool isDebugEnabled

    required property int applicationLayout
    required property int windowTitleFormat

    required property string playerVideoName
    required property string playerVideoPath

    required property var extendedExportTemplatesModel

    readonly property bool isWindows: Qt.platform.os === "windows"
    readonly property bool haveExtendedExportTemplates: extendedExportTemplatesModel.count > 0
    readonly property bool isUpdateMenuVisible: isDebugEnabled || isWindows

    readonly property var windowTitleFormatModel: [
        {
            "label": qsTranslate("MainWindow", "Default Title"),
            "value": MpvqcSettings.WindowTitleFormat.DEFAULT
        },
        {
            "label": qsTranslate("MainWindow", "Video File"),
            "value": MpvqcSettings.WindowTitleFormat.FILE_NAME
        },
        {
            "label": qsTranslate("MainWindow", "Video Path"),
            "value": MpvqcSettings.WindowTitleFormat.FILE_PATH
        },
    ]

    readonly property var applicationLayoutModel: [
        {
            "label": qsTranslate("MainWindow", "Video Above Comments"),
            "value": Qt.Vertical
        },
        {
            "label": qsTranslate("MainWindow", "Video Next to Comments"),
            "value": Qt.Horizontal
        },
    ]

    readonly property MpvqcLanguageModel languageModel: MpvqcLanguageModel {}

    readonly property string windowTitle: _determineWindowTitle()

    signal openQcDocumentsRequested
    signal saveQcDocumentsRequested
    signal saveQcDocumentsAsRequested
    signal extendedExportRequested(exportTemplate: url)

    signal openVideoRequested
    signal openSubtitlesRequested
    signal resizeVideoRequested

    signal appearanceDialogRequested
    signal commentTypesDialogRequested
    signal backupSettingsDialogRequested
    signal exportSettingsDialogRequested
    signal importSettingsDialogRequested
    signal editMpvConfigDialogRequested
    signal editInputConfigDialogRequested

    signal updateDialogRequested
    signal keyboardShortcutsDialogRequested
    signal extendedExportDialogRequested
    signal aboutDialogRequested

    signal windowDragRequested
    signal minimizeAppRequested
    signal toggleMaximizeAppRequested
    signal closeAppRequested

    function requestOpenQcDocuments(): void {
        root.openQcDocumentsRequested();
    }

    function requestSaveQcDocument(): void {
        root.saveQcDocumentsRequested();
    }

    function requestSaveQcDocumentAs(): void {
        root.saveQcDocumentsAsRequested();
    }

    function requestSaveQcDocumentExtendedUsing(name: string, exportTemplate: url): void {
        root.extendedExportRequested(exportTemplate);
    }

    function requestOpenVideo(): void {
        root.openVideoRequested();
    }

    function requestOpenSubtitles(): void {
        root.openSubtitlesRequested();
    }

    function requestResizeVideo(): void {
        root.resizeVideoRequested();
    }

    function requestOpenAppearanceDialog(): void {
        root.appearanceDialogRequested();
    }

    function requestOpenCommentTypesDialog(): void {
        root.commentTypesDialogRequested();
    }

    function configureWindowTitleFormat(updatedValue: int): void {
        mpvqcSettings.windowTitleFormat = updatedValue;
    }

    function configureApplicationLayout(updatedValue: int): void {
        mpvqcSettings.layoutOrientation = updatedValue;
    }

    function configureLanguage(updatedLanguageIdentifier: string): void {
        mpvqcSettings.language = updatedLanguageIdentifier;
    }

    function requestOpenBackupSettingsDialog(): void {
        root.backupSettingsDialogRequested();
    }

    function requestOpenExportSettingsDialog(): void {
        root.exportSettingsDialogRequested();
    }

    function requestOpenImportSettingsDialog(): void {
        root.importSettingsDialogRequested();
    }

    function requestOpenEditMpvConfigDialog(): void {
        root.editMpvConfigDialogRequested();
    }

    function requestOpenEditInputConfigDialog(): void {
        root.editInputConfigDialogRequested();
    }

    function requestOpenCheckForUpdatesDialog(): void {
        root.updateDialogRequested();
    }

    function requestOpenKeyboardShortcutsDialog(): void {
        root.keyboardShortcutsDialogRequested();
    }

    function requestOpenExtendedExportsDialog(): void {
        root.extendedExportDialogRequested();
    }

    function requestOpenAboutDialog(): void {
        root.aboutDialogRequested();
    }

    function _determineWindowTitle(): string {
        let title;
        if (!isVideoLoaded || windowTitleFormat === MpvqcSettings.WindowTitleFormat.DEFAULT) {
            title = Application.name;
        } else if (windowTitleFormat === MpvqcSettings.WindowTitleFormat.FILE_NAME) {
            title = playerVideoName;
        } else if (windowTitleFormat === MpvqcSettings.WindowTitleFormat.FILE_PATH) {
            title = playerVideoPath;
        } else {
            throw "Cannot determine window title: configuration not known";
        }

        if (isStateSaved) {
            return title;
        }

        //: %1 will be the title of the application (one of: mpvQC, file name, file path)
        return qsTranslate("MainWindow", "%1 (unsaved)").arg(title);
    }

    function requestWindowDrag(): void {
        root.windowDragRequested();
    }

    function requestMinimize(): void {
        root.minimizeAppRequested();
    }

    function requestToggleMaximize(): void {
        root.toggleMaximizeAppRequested();
    }

    function requestClose(): void {
        root.closeAppRequested();
    }
}
