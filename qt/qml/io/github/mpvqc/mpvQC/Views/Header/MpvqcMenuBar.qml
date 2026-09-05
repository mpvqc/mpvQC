// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls

import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

MenuBar {
    id: root

    required property MpvqcShellMenuBarViewModel viewModel

    signal dialogRequested(kind: int)
    signal fileDialogRequested(kind: int)
    signal customExportRequested(template: url)
    signal messageBoxRequested(kind: int)
    signal closeRequested
    signal resizeVideoRequested

    background: null

    delegate: MenuBarItem {
        id: _menuBarItem

        background: Rectangle {
            color: _menuBarItem.highlighted ? MpvqcAppearance.hoverHighlight : "transparent"
            topLeftRadius: !MpvqcWindowUtility.isMirrored && _menuBarItem.x <= 0 ? MpvqcWindowUtility.windowRadius : 0
            topRightRadius: MpvqcWindowUtility.isMirrored && _menuBarItem.x + _menuBarItem.width >= root.width ? MpvqcWindowUtility.windowRadius : 0
        }
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
            onTriggered: root.fileDialogRequested(MpvqcFileDialogKind.FileDialogKind.IMPORT_DOCUMENTS)
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
            onTriggered: root.fileDialogRequested(MpvqcFileDialogKind.FileDialogKind.SAVE_DOCUMENT)
        }

        MenuSeparator {}

        MpvqcExportQcDocumentMenu {
            onClassicExportTriggered: root.fileDialogRequested(MpvqcFileDialogKind.FileDialogKind.EXPORT_CLASSIC_DOCUMENT)
            onCustomExportTriggered: template => root.customExportRequested(template)
        }

        MenuSeparator {}

        MpvqcMenuBarItem {
            objectName: "exitMpvqcMenuItem"
            text: qsTranslate("MainWindow", "Exit mpvQC")
            icon.source: MpvqcIcons.exitToApp
            onTriggered: root.closeRequested()
        }
    }

    MpvqcMenuBarMenu {
        objectName: "videoMenu"
        title: qsTranslate("MainWindow", "Video")

        MpvqcMenuBarItem {
            objectName: "openVideoMenuItem"
            text: qsTranslate("MainWindow", "Open Video...")
            icon.source: MpvqcIcons.movie
            onTriggered: root.fileDialogRequested(MpvqcFileDialogKind.FileDialogKind.IMPORT_VIDEO)
        }

        MpvqcMenuBarItem {
            objectName: "openSubtitlesMenuItem"
            text: qsTranslate("MainWindow", "Open Subtitle(s)...")
            icon.source: MpvqcIcons.subtitles
            onTriggered: root.fileDialogRequested(MpvqcFileDialogKind.FileDialogKind.IMPORT_SUBTITLES)
        }

        MenuSeparator {}

        MpvqcMenuBarItem {
            objectName: "resizeVideoMenuItem"
            text: qsTranslate("MainWindow", "Resize Video to Original Resolution")
            icon.source: MpvqcIcons.aspectRatio
            onTriggered: root.resizeVideoRequested()
        }
    }

    MpvqcMenuBarMenu {
        objectName: "optionsMenu"
        title: qsTranslate("MainWindow", "Options")

        MpvqcMenuBarItem {
            objectName: "openAppearanceDialogMenuItem"
            text: qsTranslate("MainWindow", "Appearance...")
            icon.source: MpvqcIcons.palette
            onTriggered: root.dialogRequested(MpvqcDialogKind.DialogKind.APPEARANCE)
        }

        MpvqcMenuBarItem {
            objectName: "openCommentTypesDialogMenuItem"
            text: qsTranslate("MainWindow", "Comment Type Settings...")
            icon.source: MpvqcIcons.comment
            onTriggered: root.dialogRequested(MpvqcDialogKind.DialogKind.COMMENT_TYPES)
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
            objectName: "layoutOrientationMenu"
            title: qsTranslate("MainWindow", "Application Layout")
            icon.source: MpvqcIcons.verticalSplit

            currentValue: root.viewModel.layoutOrientation
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

            onOptionSelected: value => root.viewModel.configureLayoutOrientation(value)
        }

        MenuSeparator {}

        MpvqcMenuBarItem {
            objectName: "openBackupSettingsDialogMenuItem"
            text: qsTranslate("MainWindow", "Backup Settings...")
            icon.source: MpvqcIcons.settingsBackupRestore
            onTriggered: root.dialogRequested(MpvqcDialogKind.DialogKind.BACKUP_SETTINGS)
        }

        MpvqcMenuBarItem {
            objectName: "openExportSettingsDialogMenuItem"
            text: qsTranslate("MainWindow", "Export Settings...")
            icon.source: MpvqcIcons.upload
            onTriggered: root.dialogRequested(MpvqcDialogKind.DialogKind.EXPORT_SETTINGS)
        }

        MpvqcMenuBarItem {
            objectName: "openImportSettingsDialogMenuItem"
            text: qsTranslate("MainWindow", "Import Settings...")
            icon.source: MpvqcIcons.download
            onTriggered: root.dialogRequested(MpvqcDialogKind.DialogKind.IMPORT_SETTINGS)
        }

        MenuSeparator {}

        MpvqcMenuBarItem {
            objectName: "openEditMpvConfigDialogMenuItem"
            text: qsTranslate("MainWindow", "Edit mpv.conf...")
            icon.source: MpvqcIcons.movieEdit
            onTriggered: root.dialogRequested(MpvqcDialogKind.DialogKind.EDIT_MPV_CONFIG)
        }

        MpvqcMenuBarItem {
            objectName: "openEditInputConfigDialogMenuItem"
            text: qsTranslate("MainWindow", "Edit input.conf...")
            icon.source: MpvqcIcons.keyboard
            onTriggered: root.dialogRequested(MpvqcDialogKind.DialogKind.EDIT_INPUT_CONFIG)
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
            // Collapse when hidden via a sibling's natural height; reading own
            // implicitHeight here triggers a height -> implicitHeight binding loop.
            height: visible ? _keyboardShortcutsMenuItem.implicitHeight : 0
            onTriggered: root.messageBoxRequested(MpvqcMessageBoxKind.MessageBoxKind.VERSION_CHECK)
        }

        MpvqcMenuBarItem {
            id: _keyboardShortcutsMenuItem

            objectName: "openKeyboardShortcutsMenuItem"
            text: qsTranslate("MainWindow", "Keyboard Shortcuts...")
            icon.source: MpvqcIcons.keyboardDoubleArrowRight
            onTriggered: root.dialogRequested(MpvqcDialogKind.DialogKind.KEYBOARD_SHORTCUTS)
        }

        MenuSeparator {}

        MpvqcMenuBarItem {
            objectName: "openCustomExportsDialogMenuItem"
            text: qsTranslate("MainWindow", "Extended Exports...")
            icon.source: MpvqcIcons.upload
            onTriggered: root.messageBoxRequested(MpvqcMessageBoxKind.MessageBoxKind.CUSTOM_EXPORT)
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
            onTriggered: root.dialogRequested(MpvqcDialogKind.DialogKind.ABOUT)
        }
    }

    Shortcut {
        sequence: "CTRL+N"
        enabled: MpvqcWindowUtility.isMainWindowFocused
        onActivated: root.viewModel.requestResetAppState()
    }

    Shortcut {
        sequence: "CTRL+O"
        enabled: MpvqcWindowUtility.isMainWindowFocused
        onActivated: root.fileDialogRequested(MpvqcFileDialogKind.FileDialogKind.IMPORT_DOCUMENTS)
    }

    Shortcut {
        sequence: "CTRL+S"
        enabled: MpvqcWindowUtility.isMainWindowFocused
        onActivated: root.viewModel.requestSaveQcDocument()
    }

    Shortcut {
        sequence: "CTRL+Shift+S"
        enabled: MpvqcWindowUtility.isMainWindowFocused
        onActivated: root.fileDialogRequested(MpvqcFileDialogKind.FileDialogKind.SAVE_DOCUMENT)
    }

    Shortcut {
        sequence: "CTRL+Q"
        enabled: MpvqcWindowUtility.isMainWindowFocused
        onActivated: root.closeRequested()
    }

    Shortcut {
        sequence: "CTRL+Alt+O"
        enabled: MpvqcWindowUtility.isMainWindowFocused
        onActivated: root.fileDialogRequested(MpvqcFileDialogKind.FileDialogKind.IMPORT_VIDEO)
    }

    Shortcut {
        sequence: "CTRL+R"
        enabled: MpvqcWindowUtility.isMainWindowFocused
        onActivated: root.resizeVideoRequested()
    }

    Shortcut {
        sequence: "?"
        enabled: MpvqcWindowUtility.isMainWindowFocused
        onActivated: root.dialogRequested(MpvqcDialogKind.DialogKind.KEYBOARD_SHORTCUTS)
    }
}
