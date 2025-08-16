/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import "../dialogs"
import "../shared"

MpvqcMenu {
    id: root

    required property var mpvqcApplication

    readonly property alias appearanceAction: _appearanceAction
    readonly property alias commentTypesAction: _commentTypesAction
    readonly property alias backupAction: _backupAction
    readonly property alias exportAction: _exportAction
    readonly property alias importAction: _importAction
    readonly property alias editMpvAction: _editMpvAction
    readonly property alias editInputAction: _editInputAction

    readonly property var factoryDialogAppearance: Component {
        MpvqcDialogAppearance {
            mpvqcApplication: root.mpvqcApplication
        }
    }

    readonly property var factoryDialogCommentTypes: Component {
        MpvqcDialogCommentTypes {
            mpvqcApplication: root.mpvqcApplication
        }
    }

    readonly property var factoryDialogBackupSettings: Component {
        MpvqcDialogBackup {
            mpvqcApplication: root.mpvqcApplication
        }
    }

    readonly property var factoryDialogExportSettings: Component {
        MpvqcDialogExport {
            mpvqcApplication: root.mpvqcApplication
        }
    }

    readonly property var factoryDialogImportSettings: Component {
        MpvqcDialogImport {
            mpvqcApplication: root.mpvqcApplication
        }
    }

    readonly property var factoryDialogEditMpvSettings: Component {
        MpvqcDialogEditMpv {
            mpvqcApplication: root.mpvqcApplication
        }
    }

    readonly property var factoryDialogEditInputSettings: Component {
        MpvqcDialogEditInput {
            mpvqcApplication: root.mpvqcApplication
        }
    }

    title: qsTranslate("MainWindow", "Options")

    Action {
        id: _appearanceAction

        text: qsTranslate("MainWindow", "Appearance...")
        icon.source: "qrc:/data/icons/palette_black_24dp.svg"

        onTriggered: {
            const dialog = root.factoryDialogAppearance.createObject(root);
            dialog.closed.connect(dialog.destroy);
            dialog.open();
        }
    }

    Action {
        id: _commentTypesAction

        text: qsTranslate("MainWindow", "Comment Type Settings...")
        icon.source: "qrc:/data/icons/comment_black_24dp.svg"

        onTriggered: {
            const dialog = root.factoryDialogCommentTypes.createObject(root);
            dialog.closed.connect(dialog.destroy);
            dialog.open();
        }
    }

    MpvqcSubMenuWindowTitle {
        mpvqcApplication: root.mpvqcApplication
    }

    MpvqcSubMenuSplitViewOrientation {
        mpvqcApplication: root.mpvqcApplication
    }

    MenuSeparator {}

    Action {
        id: _backupAction

        text: qsTranslate("MainWindow", "Backup Settings...")
        icon.source: "qrc:/data/icons/settings_backup_restore_black_24dp.svg"

        onTriggered: {
            const dialog = root.factoryDialogBackupSettings.createObject(root);
            dialog.closed.connect(dialog.destroy);
            dialog.open();
        }
    }

    Action {
        id: _exportAction

        text: qsTranslate("MainWindow", "Export Settings...")
        icon.source: "qrc:/data/icons/upload_black_24dp.svg"

        onTriggered: {
            const dialog = root.factoryDialogExportSettings.createObject(root);
            dialog.closed.connect(dialog.destroy);
            dialog.open();
        }
    }

    Action {
        id: _importAction

        text: qsTranslate("MainWindow", "Import Settings...")
        icon.source: "qrc:/data/icons/download_black_24dp.svg"

        onTriggered: {
            const dialog = root.factoryDialogImportSettings.createObject(root);
            dialog.closed.connect(dialog.destroy);
            dialog.open();
        }
    }

    MenuSeparator {}

    Action {
        id: _editMpvAction

        text: qsTranslate("MainWindow", "Edit mpv.conf...")
        icon.source: "qrc:/data/icons/movie_edit_black_24dp.svg"

        onTriggered: {
            const dialog = root.factoryDialogEditMpvSettings.createObject(root);
            dialog.closed.connect(dialog.destroy);
            dialog.open();
        }
    }

    Action {
        id: _editInputAction

        text: qsTranslate("MainWindow", "Edit input.conf...")
        icon.source: "qrc:/data/icons/keyboard_black_24dp.svg"

        onTriggered: {
            const dialog = root.factoryDialogEditInputSettings.createObject(root);
            dialog.closed.connect(dialog.destroy);
            dialog.open();
        }
    }

    MenuSeparator {}

    MpvqcSubMenuLanguage {
        mpvqcApplication: root.mpvqcApplication
    }
}
