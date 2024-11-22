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
import QtQuick.Controls

import dialogs
import shared

MpvqcMenu {
    id: root

    required property var mpvqcApplication

    readonly property alias updateAction: _updateAction
    readonly property alias shortcutAction: _shortcutAction
    readonly property alias extendedExportsAction: _extendedExportsAction
    readonly property alias aboutAction: _aboutAction

    readonly property var factoryMessageBoxVersionCheck: Component {
        MpvqcMessageBoxVersionCheck {
            mpvqcApplication: root.mpvqcApplication
        }
    }

    readonly property var factoryDialogShortcuts: Component {
        MpvqcDialogShortcuts {
            mpvqcApplication: root.mpvqcApplication
        }
    }

    readonly property var factoryMessageBoxExtendedExports: Component {
        MpvqcMessageBoxExtendedExport {
            mpvqcApplication: root.mpvqcApplication
        }
    }

    readonly property var factoryDialogAbout: Component {
        MpvqcDialogAbout {
            mpvqcApplication: root.mpvqcApplication
        }
    }

    title: qsTranslate("MainWindow", "Help")

    Action {
        id: _updateAction

        text: qsTranslate("MainWindow", "Check for Updates...")
        icon.source: "qrc:/data/icons/update_black_24dp.svg"

        onTriggered: {
            const dialog = root.factoryMessageBoxVersionCheck.createObject(root);
            dialog.closed.connect(dialog.destroy);
            dialog.open();
        }
    }

    Action {
        id: _shortcutAction

        text: qsTranslate("MainWindow", "Keyboard Shortcuts...")
        icon.source: "qrc:/data/icons/shortcut_black_24dp.svg"
        shortcut: "?"

        onTriggered: {
            const dialog = root.factoryDialogShortcuts.createObject(root);
            dialog.closed.connect(dialog.destroy);
            dialog.open();
        }
    }

    MenuSeparator {}

    Action {
        id: _extendedExportsAction

        text: qsTranslate("MainWindow", "Extended Exports...")
        icon.source: "qrc:/data/icons/upload_black_24dp.svg"

        onTriggered: {
            const messageBox = root.factoryMessageBoxExtendedExports.createObject(root);
            messageBox.closed.connect(messageBox.destroy);
            messageBox.open();
        }
    }

    Action {
        id: _aboutAction

        text: qsTranslate("MainWindow", "About mpvQC...")
        icon.source: "qrc:/data/icons/info_black_24dp.svg"

        onTriggered: {
            const dialog = root.factoryDialogAbout.createObject(root);
            dialog.closed.connect(dialog.destroy);
            dialog.open();
        }
    }
}
