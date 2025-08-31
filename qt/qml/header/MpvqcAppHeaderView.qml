/*
 * Copyright (C) 2025 mpvQC developers
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import "../shared"

Item {
    id: root

    required property MpvqcAppHeaderController controller

    readonly property alias menuBarWidth: menuBar.width
    readonly property alias menuBarHeight: menuBar.height

    height: menuBarHeight
    visible: controller.isVisible

    DragHandler {
        target: null
        grabPermissions: TapHandler.CanTakeOverFromAnything

        onActiveChanged: {
            if (active) {
                root.controller.requestWindowDrag();
            }
        }
    }

    TapHandler {
        onDoubleTapped: {
            root.controller.requestToggleMaximize();
        }
    }

    Row {
        width: root.width
        spacing: 0

        MenuBar {
            id: menuBar

            MpvqcMenu {
                title: qsTranslate("MainWindow", "File")

                Action {
                    text: qsTranslate("MainWindow", "New QC Document")
                    shortcut: "CTRL+N"
                    icon.source: "qrc:/data/icons/inventory_black_24dp.svg"

                    onTriggered: {
                        root.controller.requestResetAppState();
                    }
                }

                Action {
                    text: qsTranslate("MainWindow", "Open QC Document(s)...")
                    shortcut: "CTRL+O"
                    icon.source: "qrc:/data/icons/file_open_black_24dp.svg"

                    onTriggered: {
                        root.controller.requestOpenQcDocuments();
                    }
                }

                Action {
                    text: qsTranslate("MainWindow", "Save QC Document")
                    shortcut: "CTRL+S"
                    icon.source: "qrc:/data/icons/save_black_24dp.svg"

                    onTriggered: {
                        root.controller.requestSaveQcDocument();
                    }
                }

                Action {
                    text: qsTranslate("MainWindow", "Save QC Document As...")
                    shortcut: "CTRL+Shift+S"
                    icon.source: "qrc:/data/icons/save_as_black_24dp.svg"

                    onTriggered: {
                        root.controller.requestSaveQcDocumentAs();
                    }
                }

                MenuSeparator {
                    visible: root.controller.haveExtendedExportTemplates
                    height: visible ? implicitHeight : 0
                }

                MpvqcMenu {
                    title: qsTranslate("MainWindow", "Export QC Document")
                    icon.source: "qrc:/data/icons/save_alt_black_24dp.svg"
                    icon.height: 24
                    icon.width: 24

                    enabled: root.controller.haveExtendedExportTemplates

                    onEnabledChanged: {
                        parent.enabled = enabled;
                        parent.visible = enabled;
                        parent.height = enabled ? parent.implicitHeight : 0;
                    }

                    Repeater {
                        id: _repeater
                        model: root.controller.extendedExportTemplatesModel

                        delegate: MenuItem {
                            required property string name
                            required property url path

                            text: name
                            icon.source: "qrc:/data/icons/notes_black_24dp.svg"
                            icon.height: 24
                            icon.width: 24

                            onTriggered: {
                                root.controller.requestSaveQcDocumentExtendedUsing(name, path);
                            }
                        }
                    }
                }

                MenuSeparator {}

                Action {
                    text: qsTranslate("MainWindow", "Exit mpvQC")
                    shortcut: "CTRL+Q"
                    icon.source: "qrc:/data/icons/exit_to_app_black_24dp.svg"

                    onTriggered: {
                        root.controller.requestClose();
                    }
                }
            }

            MpvqcMenu {
                title: qsTranslate("MainWindow", "Video")

                Action {
                    text: qsTranslate("MainWindow", "Open Video...")
                    shortcut: "CTRL+Alt+O"
                    icon.source: "qrc:/data/icons/movie_black_24dp.svg"

                    onTriggered: {
                        root.controller.requestOpenVideo();
                    }
                }

                Action {
                    text: qsTranslate("MainWindow", "Open Subtitle(s)...")
                    icon.source: "qrc:/data/icons/subtitles_black_24dp.svg"

                    onTriggered: {
                        root.controller.requestOpenSubtitles();
                    }
                }

                MenuSeparator {}

                Action {
                    text: qsTranslate("MainWindow", "Resize Video to Original Resolution")
                    shortcut: "CTRL+R"
                    icon.source: "qrc:/data/icons/aspect_ratio_black_24dp.svg"

                    onTriggered: {
                        root.controller.requestResizeVideo();
                    }
                }
            }

            MpvqcMenu {
                title: qsTranslate("MainWindow", "Options")

                Action {
                    text: qsTranslate("MainWindow", "Appearance...")
                    icon.source: "qrc:/data/icons/palette_black_24dp.svg"

                    onTriggered: {
                        root.controller.requestOpenAppearanceDialog();
                    }
                }

                Action {
                    text: qsTranslate("MainWindow", "Comment Type Settings...")
                    icon.source: "qrc:/data/icons/comment_black_24dp.svg"

                    onTriggered: {
                        root.controller.requestOpenCommentTypesDialog();
                    }
                }

                MpvqcMenu {
                    title: qsTranslate("MainWindow", "Application Title")
                    icon.source: "qrc:/data/icons/title_black_24dp.svg"
                    icon.height: 24
                    icon.width: 24

                    Repeater {
                        model: root.controller.windowTitleFormatModel

                        delegate: MenuItem {
                            required property string label
                            required property int value

                            text: label
                            autoExclusive: true
                            checkable: true
                            checked: root.controller.windowTitleFormat === value

                            onTriggered: {
                                root.controller.configureWindowTitleFormat(value);
                            }
                        }
                    }
                }

                MpvqcMenu {
                    title: qsTranslate("MainWindow", "Application Layout")
                    icon.source: "qrc:/data/icons/vertical_split_black_24dp.svg"
                    icon.height: 24
                    icon.width: 24

                    Repeater {
                        model: root.controller.applicationLayoutModel

                        delegate: MenuItem {
                            required property string label
                            required property int value

                            text: label
                            autoExclusive: true
                            checkable: true
                            checked: root.controller.applicationLayout === value

                            onTriggered: {
                                root.controller.configureApplicationLayout(value);
                            }
                        }
                    }
                }

                MenuSeparator {}

                Action {
                    text: qsTranslate("MainWindow", "Backup Settings...")
                    icon.source: "qrc:/data/icons/settings_backup_restore_black_24dp.svg"

                    onTriggered: {
                        root.controller.requestOpenBackupSettingsDialog();
                    }
                }

                Action {
                    text: qsTranslate("MainWindow", "Export Settings...")
                    icon.source: "qrc:/data/icons/upload_black_24dp.svg"

                    onTriggered: {
                        root.controller.requestOpenExportSettingsDialog();
                    }
                }

                Action {
                    text: qsTranslate("MainWindow", "Import Settings...")
                    icon.source: "qrc:/data/icons/download_black_24dp.svg"

                    onTriggered: {
                        root.controller.requestOpenImportSettingsDialog();
                    }
                }

                MenuSeparator {}

                Action {
                    text: qsTranslate("MainWindow", "Edit mpv.conf...")
                    icon.source: "qrc:/data/icons/movie_edit_black_24dp.svg"

                    onTriggered: {
                        root.controller.requestOpenEditMpvConfigDialog();
                    }
                }

                Action {
                    text: qsTranslate("MainWindow", "Edit input.conf...")
                    icon.source: "qrc:/data/icons/keyboard_black_24dp.svg"

                    onTriggered: {
                        root.controller.requestOpenEditInputConfigDialog();
                    }
                }

                MenuSeparator {}

                MpvqcMenu {
                    id: _languageMenu

                    title: qsTranslate("MainWindow", "Language")
                    icon.source: "qrc:/data/icons/language_black_24dp.svg"
                    icon.height: 24
                    icon.width: 24

                    property var _deferToOnClose: () => {}

                    onClosed: {
                        _deferToOnClose(); // qmllint disable
                        _deferToOnClose = () => {};
                    }

                    Repeater {
                        model: root.controller.languageModel

                        MenuItem {
                            required property string language
                            required property string identifier

                            text: qsTranslate("Languages", language)
                            autoExclusive: true
                            checkable: true
                            checked: identifier === Qt.uiLanguage

                            onTriggered: {
                                _languageMenu._deferToOnClose = () => root.controller.configureLanguage(identifier);
                            }
                        }
                    }
                }
            }

            MpvqcMenu {
                title: qsTranslate("MainWindow", "Help")

                MenuItem {

                    text: qsTranslate("MainWindow", "Check for Updates...")
                    icon.source: "qrc:/data/icons/update_black_24dp.svg"
                    visible: root.controller.isUpdateMenuVisible
                    height: visible ? implicitHeight : 0

                    onTriggered: {
                        root.controller.requestOpenCheckForUpdatesDialog();
                    }
                }

                Action {
                    text: qsTranslate("MainWindow", "Keyboard Shortcuts...")
                    icon.source: "qrc:/data/icons/shortcut_black_24dp.svg"
                    shortcut: "?"

                    onTriggered: {
                        root.controller.requestOpenKeyboardShortcutsDialog();
                    }
                }

                MenuSeparator {}

                Action {
                    text: qsTranslate("MainWindow", "Extended Exports...")
                    icon.source: "qrc:/data/icons/upload_black_24dp.svg"

                    onTriggered: {
                        root.controller.requestOpenExtendedExportsDialog();
                    }
                }

                Action {
                    text: qsTranslate("MainWindow", "About mpvQC...")
                    icon.source: "qrc:/data/icons/info_black_24dp.svg"

                    onTriggered: {
                        root.controller.requestOpenAboutDialog();
                    }
                }
            }
        }

        Label {
            width: root.width - root.menuBarWidth * 2
            height: root.menuBarHeight
            text: root.controller.windowTitle
            elide: LayoutMirroring.enabled ? Text.ElideRight : Text.ElideLeft
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            leftPadding: 25
            rightPadding: 25
        }

        Item {
            width: root.menuBarWidth
            height: root.menuBarHeight

            ToolButton {
                id: _minimizeButton

                height: root.height
                focusPolicy: Qt.NoFocus
                anchors.right: _maximizeButton.left
                icon.width: 18
                icon.height: 18
                icon.source: "qrc:/data/icons/minimize_black_24dp.svg"

                onClicked: {
                    root.controller.requestMinimize();
                }
            }

            ToolButton {
                id: _maximizeButton

                readonly property url iconMaximize: "qrc:/data/icons/open_in_full_black_24dp.svg"
                readonly property url iconNormalize: "qrc:/data/icons/close_fullscreen_black_24dp.svg"

                height: root.height
                focusPolicy: Qt.NoFocus
                anchors.right: _closeButton.left
                icon.width: 18
                icon.height: 18
                icon.source: root.controller.isMaximized ? iconNormalize : iconMaximize

                onClicked: {
                    root.controller.requestToggleMaximize();
                }
            }

            ToolButton {
                id: _closeButton

                height: root.height
                focusPolicy: Qt.NoFocus
                anchors.right: parent.right

                icon {
                    width: 18
                    height: 18
                    source: "qrc:/data/icons/close_black_24dp.svg"
                    color: {
                        if (root.controller.isWindows && _closeButton.hovered) {
                            return "#FFFFFD";
                        } else if (_closeButton.hovered) {
                            return root.controller.mpvqcTheme.background;
                        } else {
                            return root.controller.mpvqcTheme.foreground;
                        }
                    }
                }

                onClicked: {
                    root.controller.requestClose();
                }

                Binding {
                    when: true
                    target: _closeButton.background
                    property: "color"
                    value: root.controller.isWindows ? "#C42C1E" : root.controller.mpvqcTheme.control
                    restoreMode: Binding.RestoreNone
                }
            }
        }
    }
}
