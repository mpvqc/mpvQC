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


import QtQuick.Controls
import dialogs
import shared


MpvqcMenu {
    id: root

    required property var mpvqcApplication
    property alias updateAction: _updateAction
    property alias shortcutAction: _shortcutAction
    property alias aboutAction: _aboutAction

    title: qsTranslate("MainWindow", "&Help")

    Action {
        id: _updateAction

        property var dialog: MpvqcDialogUpdate {
            mpvqcApplication: root.mpvqcApplication
        }

        text: qsTranslate("MainWindow", "&Check for Updates...")

        onTriggered: {
            dialog.open()
        }
    }

    Action {
        id: _shortcutAction

        property var dialog: MpvqcDialogShortcuts {
            mpvqcApplication: root.mpvqcApplication
        }

        text: qsTranslate("MainWindow", "Keyboard Shortcuts...")

        onTriggered: {
            dialog.open()
        }
    }

    MenuSeparator { }

    Action {
        id: _aboutAction

        property var dialog: MpvqcDialogAbout {
            mpvqcApplication: root.mpvqcApplication
        }

        text: qsTranslate("MainWindow", "About &mpvQC...")

        onTriggered: {
            dialog.open()
        }
    }

}
