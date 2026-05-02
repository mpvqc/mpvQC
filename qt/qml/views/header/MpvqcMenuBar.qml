// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import pyobjects
import "../../utility"

MenuBar {
    id: root

    required property MpvqcMenuBarViewModel viewModel

    readonly property bool isShortcutEnabled: {
        const item = root.Window.window?.activeFocusItem;
        return !item || !(item instanceof TextField || item instanceof TextArea || item instanceof TextInput || item instanceof TextEdit);
    }

    MpvqcMenuBarMenu {
        objectName: "fileMenu"
        title: qsTranslate("MainWindow", "File")

        MpvqcMenuBarItem {
            objectName: "newQcDocumentMenuItem"
            text: qsTranslate("MainWindow", "New QC Document")
            icon.source: MpvqcIcons.draft
            onTriggered: root.viewModel.requestResetAppState()
        }

        MpvqcMenuBarItem {
            objectName: "openQcDocumentsMenuItem"
            text: qsTranslate("MainWindow", "Open QC Document(s)...")
            icon.source: MpvqcIcons.fileOpen
            onTriggered: root.viewModel.requestOpenQcDocuments()
        }

        MpvqcMenuBarItem {
            objectName: "saveQcDocumentMenuItem"
            text: qsTranslate("MainWindow", "Save QC Document")
            icon.source: MpvqcIcons.save
            onTriggered: root.viewModel.requestSaveQcDocument()
        }

        MpvqcMenuBarItem {
            objectName: "saveQcDocumentAsMenuItem"
            text: qsTranslate("MainWindow", "Save QC Document As...")
            icon.source: MpvqcIcons.saveAs
            onTriggered: root.viewModel.requestSaveQcDocumentAs()
        }

        MenuSeparator {
            Component.onCompleted: {
                if (_extendedExportModel.count === 0) {
                    visible = false;
                    height = 0;
                }
            }
        }

        MpvqcMenuBarMenu {
            objectName: "exportQcDocumentMenu"
            title: qsTranslate("MainWindow", "Export QC Document")
            icon.source: MpvqcIcons.fileExport

            Component.onCompleted: {
                if (_extendedExportModel.count === 0) {
                    // `visible` on a Menu toggles its open/closed state,
                    // so hiding the entry has to go through the parent MenuItem instead of a reactive binding
                    parent.visible = false;
                    parent.height = 0;
                }
            }

            Repeater {
                model: MpvqcExportTemplateModel {
                    id: _extendedExportModel
                }

                delegate: MpvqcMenuBarItem {
                    required property string name
                    required property url path

                    text: name
                    icon.source: MpvqcIcons.notes
                    onTriggered: root.viewModel.requestSaveQcDocumentExtendedUsing(name, path)
                }
            }
        }

        MenuSeparator {}

        MpvqcMenuBarItem {
            objectName: "exitMpvqcMenuItem"
            text: qsTranslate("MainWindow", "Exit mpvQC")
            icon.source: MpvqcIcons.exitToApp
            onTriggered: root.viewModel.requestClose()
        }
    }

    MpvqcMenuBarMenu {
        objectName: "videoMenu"
        title: qsTranslate("MainWindow", "Video")

        MpvqcMenuBarItem {
            objectName: "openVideoMenuItem"
            text: qsTranslate("MainWindow", "Open Video...")
            icon.source: MpvqcIcons.movie
            onTriggered: root.viewModel.requestOpenVideo()
        }

        MpvqcMenuBarItem {
            objectName: "openSubtitlesMenuItem"
            text: qsTranslate("MainWindow", "Open Subtitle(s)...")
            icon.source: MpvqcIcons.subtitles
            onTriggered: root.viewModel.requestOpenSubtitles()
        }

        MenuSeparator {}

        MpvqcMenuBarItem {
            objectName: "resizeVideoMenuItem"
            text: qsTranslate("MainWindow", "Resize Video to Original Resolution")
            icon.source: MpvqcIcons.aspectRatio
            onTriggered: root.viewModel.requestResizeVideo()
        }
    }

    MpvqcMenuBarMenu {
        objectName: "optionsMenu"
        title: qsTranslate("MainWindow", "Options")

        MpvqcMenuBarItem {
            objectName: "openAppearanceDialogMenuItem"
            text: qsTranslate("MainWindow", "Appearance...")
            icon.source: MpvqcIcons.palette
            onTriggered: root.viewModel.requestOpenAppearanceDialog()
        }

        MpvqcMenuBarItem {
            objectName: "openCommentTypesDialogMenuItem"
            text: qsTranslate("MainWindow", "Comment Type Settings...")
            icon.source: MpvqcIcons.comment
            onTriggered: root.viewModel.requestOpenCommentTypesDialog()
        }

        MpvqcRadioMenu {
            objectName: "applicationTitleMenu"
            title: qsTranslate("MainWindow", "Application Title")
            icon.source: MpvqcIcons.title

            currentValue: root.viewModel.windowTitleFormat
            model: [
                {
                    "identifier": "default",
                    "label": qsTranslate("MainWindow", "Default Title"),
                    "value": MpvqcWindowTitleFormat.WindowTitleFormat.DEFAULT
                },
                {
                    "identifier": "filename",
                    "label": qsTranslate("MainWindow", "Video File"),
                    "value": MpvqcWindowTitleFormat.WindowTitleFormat.FILE_NAME
                },
                {
                    "identifier": "filepath",
                    "label": qsTranslate("MainWindow", "Video Path"),
                    "value": MpvqcWindowTitleFormat.WindowTitleFormat.FILE_PATH
                },
            ]

            onOptionSelected: value => root.viewModel.configureWindowTitleFormat(value)
        }

        MpvqcRadioMenu {
            objectName: "applicationLayoutMenu"
            title: qsTranslate("MainWindow", "Application Layout")
            icon.source: MpvqcIcons.verticalSplit

            currentValue: root.viewModel.applicationLayout
            model: [
                {
                    "identifier": "vertical",
                    "label": qsTranslate("MainWindow", "Video Above Comments"),
                    "value": Qt.Vertical
                },
                {
                    "identifier": "horizontal",
                    "label": qsTranslate("MainWindow", "Video Next to Comments"),
                    "value": Qt.Horizontal
                },
            ]

            onOptionSelected: value => root.viewModel.configureApplicationLayout(value)
        }

        MenuSeparator {}

        MpvqcMenuBarItem {
            objectName: "openBackupSettingsDialogMenuItem"
            text: qsTranslate("MainWindow", "Backup Settings...")
            icon.source: MpvqcIcons.settingsBackupRestore
            onTriggered: root.viewModel.requestOpenBackupSettingsDialog()
        }

        MpvqcMenuBarItem {
            objectName: "openExportSettingsDialogMenuItem"
            text: qsTranslate("MainWindow", "Export Settings...")
            icon.source: MpvqcIcons.upload
            onTriggered: root.viewModel.requestOpenExportSettingsDialog()
        }

        MpvqcMenuBarItem {
            objectName: "openImportSettingsDialogMenuItem"
            text: qsTranslate("MainWindow", "Import Settings...")
            icon.source: MpvqcIcons.download
            onTriggered: root.viewModel.requestOpenImportSettingsDialog()
        }

        MenuSeparator {}

        MpvqcMenuBarItem {
            objectName: "openEditMpvConfigDialogMenuItem"
            text: qsTranslate("MainWindow", "Edit mpv.conf...")
            icon.source: MpvqcIcons.movieEdit
            onTriggered: root.viewModel.requestOpenEditMpvConfigDialog()
        }

        MpvqcMenuBarItem {
            objectName: "openEditInputConfigDialogMenuItem"
            text: qsTranslate("MainWindow", "Edit input.conf...")
            icon.source: MpvqcIcons.keyboard
            onTriggered: root.viewModel.requestOpenEditInputConfigDialog()
        }

        MenuSeparator {}

        MpvqcLanguageSubMenu {
            onLanguageSelected: identifier => root.viewModel.configureLanguage(identifier)
        }
    }

    MpvqcMenuBarMenu {
        objectName: "helpMenu"
        title: qsTranslate("MainWindow", "Help")

        MpvqcMenuBarItem {
            objectName: "openCheckForUpdatesMenuItem"
            text: qsTranslate("MainWindow", "Check for Updates...")
            icon.source: MpvqcIcons.update
            visible: root.viewModel.isUpdateMenuVisible
            height: visible ? implicitHeight : 0
            onTriggered: root.viewModel.requestOpenCheckForUpdatesDialog()
        }

        MpvqcMenuBarItem {
            objectName: "openKeyboardShortcutsMenuItem"
            text: qsTranslate("MainWindow", "Keyboard Shortcuts...")
            icon.source: MpvqcIcons.keyboardDoubleArrowRight
            onTriggered: root.viewModel.requestOpenKeyboardShortcutsDialog()
        }

        MenuSeparator {}

        MpvqcMenuBarItem {
            objectName: "openExtendedExportsDialogMenuItem"
            text: qsTranslate("MainWindow", "Extended Exports...")
            icon.source: MpvqcIcons.upload
            onTriggered: root.viewModel.requestOpenExtendedExportsDialog()
        }

        MpvqcMenuBarItem {
            objectName: "openAppDataFolderMenuItem"
            text: qsTranslate("MainWindow", "Open App Data Folder...")
            icon.source: MpvqcIcons.folderOpen
            onTriggered: root.viewModel.openAppDataFolder()
        }

        MenuSeparator {}

        MpvqcMenuBarItem {
            objectName: "openAboutDialogMenuItem"
            text: qsTranslate("MainWindow", "About mpvQC...")
            icon.source: MpvqcIcons.info
            onTriggered: root.viewModel.requestOpenAboutDialog()
        }
    }

    Shortcut {
        sequence: "CTRL+N"
        enabled: root.isShortcutEnabled
        onActivated: root.viewModel.requestResetAppState()
    }

    Shortcut {
        sequence: "CTRL+O"
        enabled: root.isShortcutEnabled
        onActivated: root.viewModel.requestOpenQcDocuments()
    }

    Shortcut {
        sequence: "CTRL+S"
        enabled: root.isShortcutEnabled
        onActivated: root.viewModel.requestSaveQcDocument()
    }

    Shortcut {
        sequence: "CTRL+Shift+S"
        enabled: root.isShortcutEnabled
        onActivated: root.viewModel.requestSaveQcDocumentAs()
    }

    Shortcut {
        sequence: "CTRL+Q"
        enabled: root.isShortcutEnabled
        onActivated: root.viewModel.requestClose()
    }

    Shortcut {
        sequence: "CTRL+Alt+O"
        enabled: root.isShortcutEnabled
        onActivated: root.viewModel.requestOpenVideo()
    }

    Shortcut {
        sequence: "CTRL+R"
        enabled: root.isShortcutEnabled
        onActivated: root.viewModel.requestResizeVideo()
    }

    Shortcut {
        sequence: "?"
        enabled: root.isShortcutEnabled
        onActivated: root.viewModel.requestOpenKeyboardShortcutsDialog()
    }
}
