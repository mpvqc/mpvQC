// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import pyobjects

import "../../components"

MenuBar {
    id: root

    required property MpvqcMenuBarViewModel viewModel

    readonly property bool isShortcutEnabled: {
        const item = root.Window.window?.activeFocusItem;
        return !item || !(item instanceof TextField || item instanceof TextArea || item instanceof TextInput || item instanceof TextEdit);
    }

    // *********************************************************
    // fixme: Workaround QTBUG-131786 to fake modal behavior on Windows
    // Once bug is resolved, we can remove ids from the menus
    readonly property bool isAnyMenuVisible: _fileMenu.visible || _videoMenu.visible || _optionsMenu.visible || _helpMenu.visible
    // *********************************************************

    MpvqcMenuBarMenu {
        id: _fileMenu

        title: qsTranslate("MainWindow", "File")

        MenuItem {
            text: qsTranslate("MainWindow", "New QC Document")
            icon.source: "qrc:/data/icons/draft_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24
            onTriggered: root.viewModel.requestResetAppState()
        }

        MenuItem {
            text: qsTranslate("MainWindow", "Open QC Document(s)...")
            icon.source: "qrc:/data/icons/file_open_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24
            onTriggered: root.viewModel.requestOpenQcDocuments()
        }

        MenuItem {
            text: qsTranslate("MainWindow", "Save QC Document")
            icon.source: "qrc:/data/icons/save_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24
            onTriggered: root.viewModel.requestSaveQcDocument()
        }

        MenuItem {
            text: qsTranslate("MainWindow", "Save QC Document As...")
            icon.source: "qrc:/data/icons/save_as_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24
            onTriggered: root.viewModel.requestSaveQcDocumentAs()
        }

        MenuSeparator {
            visible: _extendedExportModel.count > 0
            height: visible ? implicitHeight : 0
        }

        MpvqcMenuBarMenu {
            title: qsTranslate("MainWindow", "Export QC Document")
            icon.source: "qrc:/data/icons/file_export_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24

            enabled: _extendedExportModel.count > 0

            onEnabledChanged: {
                parent.enabled = enabled;
                parent.visible = enabled;
                parent.height = enabled ? parent.implicitHeight : 0;
            }

            Repeater {
                model: MpvqcExportTemplateModel {
                    id: _extendedExportModel
                }

                delegate: MenuItem {
                    required property string name
                    required property url path

                    text: name
                    icon.source: "qrc:/data/icons/notes_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                    icon.height: 24
                    icon.width: 24
                    onTriggered: root.viewModel.requestSaveQcDocumentExtendedUsing(name, path)
                }
            }
        }

        MenuSeparator {}

        MenuItem {
            text: qsTranslate("MainWindow", "Exit mpvQC")
            icon.source: "qrc:/data/icons/exit_to_app_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24
            onTriggered: root.viewModel.requestClose()
        }
    }

    MpvqcMenuBarMenu {
        id: _videoMenu

        title: qsTranslate("MainWindow", "Video")

        MenuItem {
            text: qsTranslate("MainWindow", "Open Video...")
            icon.source: "qrc:/data/icons/movie_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24
            onTriggered: root.viewModel.requestOpenVideo()
        }

        MenuItem {
            text: qsTranslate("MainWindow", "Open Subtitle(s)...")
            icon.source: "qrc:/data/icons/subtitles_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24
            onTriggered: root.viewModel.requestOpenSubtitles()
        }

        MenuSeparator {}

        MenuItem {
            text: qsTranslate("MainWindow", "Resize Video to Original Resolution")
            icon.source: "qrc:/data/icons/aspect_ratio_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24
            onTriggered: root.viewModel.requestResizeVideo()
        }
    }

    MpvqcMenuBarMenu {
        id: _optionsMenu

        title: qsTranslate("MainWindow", "Options")

        MenuItem {
            text: qsTranslate("MainWindow", "Appearance...")
            icon.source: "qrc:/data/icons/palette_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24
            onTriggered: root.viewModel.requestOpenAppearanceDialog()
        }

        MenuItem {
            text: qsTranslate("MainWindow", "Comment Type Settings...")
            icon.source: "qrc:/data/icons/comment_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24
            onTriggered: root.viewModel.requestOpenCommentTypesDialog()
        }

        MpvqcMenuBarMenu {
            title: qsTranslate("MainWindow", "Application Title")
            icon.source: "qrc:/data/icons/title_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24

            Repeater {
                model: [
                    {
                        "label": qsTranslate("MainWindow", "Default Title"),
                        "value": MpvqcMenuBarViewModel.WindowTitleFormat.DEFAULT
                    },
                    {
                        "label": qsTranslate("MainWindow", "Video File"),
                        "value": MpvqcMenuBarViewModel.WindowTitleFormat.FILE_NAME
                    },
                    {
                        "label": qsTranslate("MainWindow", "Video Path"),
                        "value": MpvqcMenuBarViewModel.WindowTitleFormat.FILE_PATH
                    },
                ]

                delegate: MenuItem {
                    required property string label
                    required property int value

                    text: label
                    autoExclusive: true
                    checkable: true
                    checked: root.viewModel.windowTitleFormat === value
                    onTriggered: root.viewModel.configureWindowTitleFormat(value)
                }
            }
        }

        MpvqcMenuBarMenu {
            title: qsTranslate("MainWindow", "Application Layout")
            icon.source: "qrc:/data/icons/vertical_split_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24

            Repeater {
                model: [
                    {
                        "label": qsTranslate("MainWindow", "Video Above Comments"),
                        "value": Qt.Vertical
                    },
                    {
                        "label": qsTranslate("MainWindow", "Video Next to Comments"),
                        "value": Qt.Horizontal
                    },
                ]

                delegate: MenuItem {
                    required property string label
                    required property int value

                    text: label
                    autoExclusive: true
                    checkable: true
                    checked: root.viewModel.applicationLayout === value
                    onTriggered: root.viewModel.configureApplicationLayout(value)
                }
            }
        }

        MenuSeparator {}

        MenuItem {
            text: qsTranslate("MainWindow", "Backup Settings...")
            icon.source: "qrc:/data/icons/settings_backup_restore_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24
            onTriggered: root.viewModel.requestOpenBackupSettingsDialog()
        }

        MenuItem {
            text: qsTranslate("MainWindow", "Export Settings...")
            icon.source: "qrc:/data/icons/upload_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24
            onTriggered: root.viewModel.requestOpenExportSettingsDialog()
        }

        MenuItem {
            text: qsTranslate("MainWindow", "Import Settings...")
            icon.source: "qrc:/data/icons/download_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24
            onTriggered: root.viewModel.requestOpenImportSettingsDialog()
        }

        MenuSeparator {}

        MenuItem {
            text: qsTranslate("MainWindow", "Edit mpv.conf...")
            icon.source: "qrc:/data/icons/movie_edit_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24
            onTriggered: root.viewModel.requestOpenEditMpvConfigDialog()
        }

        MenuItem {
            text: qsTranslate("MainWindow", "Edit input.conf...")
            icon.source: "qrc:/data/icons/keyboard_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24
            onTriggered: root.viewModel.requestOpenEditInputConfigDialog()
        }

        MenuSeparator {}

        MpvqcMenuBarMenu {
            id: _languageMenu

            title: qsTranslate("MainWindow", "Language")
            icon.source: "qrc:/data/icons/language_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24

            property var _deferToOnClose: () => {}

            onClosed: {
                _deferToOnClose(); // qmllint disable
                _deferToOnClose = () => {};
            }

            Repeater {
                model: MpvqcLanguageModel {}

                MenuItem {
                    required property string language
                    required property string identifier

                    text: qsTranslate("Languages", language)
                    autoExclusive: true
                    checkable: true
                    checked: identifier === Qt.uiLanguage
                    onTriggered: _languageMenu._deferToOnClose = () => root.viewModel.configureLanguage(identifier)
                }
            }
        }
    }

    MpvqcMenuBarMenu {
        id: _helpMenu

        title: qsTranslate("MainWindow", "Help")

        MenuItem {
            text: qsTranslate("MainWindow", "Check for Updates...")
            icon.source: "qrc:/data/icons/update_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24
            visible: root.viewModel.isUpdateMenuVisible
            height: visible ? implicitHeight : 0
            onTriggered: root.viewModel.requestOpenCheckForUpdatesDialog()
        }

        MenuItem {
            text: qsTranslate("MainWindow", "Keyboard Shortcuts...")
            icon.source: "qrc:/data/icons/keyboard_double_arrow_right_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24
            onTriggered: root.viewModel.requestOpenKeyboardShortcutsDialog()
        }

        MenuSeparator {}

        MenuItem {
            text: qsTranslate("MainWindow", "Extended Exports...")
            icon.source: "qrc:/data/icons/upload_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24
            onTriggered: root.viewModel.requestOpenExtendedExportsDialog()
        }

        MenuItem {
            text: qsTranslate("MainWindow", "About mpvQC...")
            icon.source: "qrc:/data/icons/info_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
            icon.height: 24
            icon.width: 24
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
