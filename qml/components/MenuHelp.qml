/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick.Controls


MenuAutoWidth {

    title: qsTranslate("MainWindow", "&Help")

    Action {
        text: qsTranslate("MainWindow", "&Check for Updates...")
        onTriggered: {
            console.log("&Check for Updates...")
        }
    }

    Action {
        text: qsTranslate("MainWindow", "About &Qt")
        onTriggered: {
            console.log("About Qt")
        }
    }

    MenuSeparator { }

    Action {
        text: qsTranslate("MainWindow", "About &mpvQC")
        onTriggered: {
            const component = Qt.createComponent("qrc:/qml/components/DialogAbout.qml")
            const dialog = component.createObject(appWindow)
            dialog.open()
        }
    }

}
