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

    title: qsTranslate("MainWindow", "&Options")

    Action {
        id: _appearanceAction

        property var dialog: MpvqcDialogAppearance {
            mpvqcApplication: root.mpvqcApplication
        }

        text: qsTranslate("MainWindow", "&Appearance...")

        onTriggered: {
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

        onTriggered: {
            const dialog = factory.createObject(parent)
            dialog.closed.connect(dialog.destroy)
            dialog.open()
        }
    }

    MenuSeparator { }

    Action {
        id: _backupAction

        property var dialog: MpvqcDialogBackup {
            mpvqcApplication: root.mpvqcApplication
        }

        text: qsTranslate("MainWindow", "&Backup Settings...")

        onTriggered: {
            dialog.open()
        }
    }

    Action {
        id: _exportAction

        property var dialog: MpvqcDialogExport {
            mpvqcApplication: root.mpvqcApplication
        }

        text: qsTranslate("MainWindow", "&Export Settings...")

        onTriggered: {
            dialog.open()
        }
    }

    Action {
        id: _importAction

        property var dialog: MpvqcDialogImport {
            mpvqcApplication: root.mpvqcApplication
        }

        text: qsTranslate("MainWindow", "&Import Settings...")

        onTriggered: {
            dialog.open()
        }
    }

    MenuSeparator { }

    MpvqcSubMenuLanguage {
        mpvqcApplication: root.mpvqcApplication
    }

}
