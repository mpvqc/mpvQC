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

import QtQuick
import QtQuick.Controls

import dialogs
import shared


MpvqcMenu {
    id: root

    required property var mpvqcApplication

    property alias appearanceAction: _appearanceAction
    property alias commentTypesAction: _commentTypesAction
    property alias exportAction: _exportAction
    property alias importAction: _importAction
    property alias backupAction: _backupAction
    property alias editMpvAction: _editMpvAction
    property alias editInputAction: _editInputAction

    title: qsTranslate("MainWindow", "&Options")

    Action {
        id: _appearanceAction

        property var factory: Component {
            MpvqcDialogAppearance {
                mpvqcApplication: root.mpvqcApplication
            }
        }

        text: qsTranslate("MainWindow", "&Appearance...")
        icon.source: "qrc:/data/icons/palette_black_24dp.svg"

        onTriggered: {
            const dialog = factory.createObject(root)
            dialog.closed.connect(dialog.destroy)
            dialog.open()
        }
    }

    Action {
        id: _commentTypesAction

        property var factory: Component {
            MpvqcDialogCommentTypes {
                mpvqcApplication: root.mpvqcApplication
            }
        }

        text: qsTranslate("MainWindow", "&Comment Type Settings...")
        icon.source: "qrc:/data/icons/comment_black_24dp.svg"

        onTriggered: {
            const dialog = factory.createObject(root)
            dialog.closed.connect(dialog.destroy)
            dialog.open()
        }
    }

    MpvqcSubMenuWindowTitle {
        mpvqcApplication: root.mpvqcApplication
    }

    MenuSeparator { }

    Action {
        id: _backupAction

        property var factory: Component {
            MpvqcDialogBackup {
                mpvqcApplication: root.mpvqcApplication
            }
        }

        text: qsTranslate("MainWindow", "&Backup Settings...")
        icon.source: "qrc:/data/icons/settings_backup_restore_black_24dp.svg"

        onTriggered: {
            const dialog = factory.createObject(root)
            dialog.closed.connect(dialog.destroy)
            dialog.open()
        }
    }

    Action {
        id: _exportAction

        property var factory: Component {
            MpvqcDialogExport {
                mpvqcApplication: root.mpvqcApplication
            }
        }

        text: qsTranslate("MainWindow", "&Export Settings...")
        icon.source: "qrc:/data/icons/upload_black_24dp.svg"

        onTriggered: {
            const dialog = factory.createObject(root)
            dialog.closed.connect(dialog.destroy)
            dialog.open()
        }
    }

    Action {
        id: _importAction

        property var factory: Component {
            MpvqcDialogImport {
                mpvqcApplication: root.mpvqcApplication
            }
        }

        text: qsTranslate("MainWindow", "&Import Settings...")
        icon.source: "qrc:/data/icons/download_black_24dp.svg"

        onTriggered: {
            const dialog = factory.createObject(root)
            dialog.closed.connect(dialog.destroy)
            dialog.open()
        }
    }

    MenuSeparator { }

    Action {
        id: _editMpvAction

        property var factory: Component {
            MpvqcDialogEditMpv {
                mpvqcApplication: root.mpvqcApplication
            }
        }

        text: qsTranslate("MainWindow", "&Edit mpv.conf...")
        icon.source: "qrc:/data/icons/movie_edit_black_24dp.svg"

        onTriggered: {
            const dialog = factory.createObject(root)
            dialog.closed.connect(dialog.destroy)
            dialog.open()
        }
    }

    Action {
        id: _editInputAction

        property var factory: Component {
            MpvqcDialogEditInput {
                mpvqcApplication: root.mpvqcApplication
            }
        }

        text: qsTranslate("MainWindow", "&Edit input.conf...")
        icon.source: "qrc:/data/icons/keyboard_black_24dp.svg"

        onTriggered: {
            const dialog = factory.createObject(root)
            dialog.closed.connect(dialog.destroy)
            dialog.open()
        }
    }

    MenuSeparator { }

    MpvqcSubMenuLanguage {
        mpvqcApplication: root.mpvqcApplication
    }

}
