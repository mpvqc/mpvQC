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
import components
import helpers
import settings
import models


MpvqcAutoWidthMenu {
    title: qsTranslate("MainWindow", "&Options")

    Action {
        text: qsTranslate("MainWindow", "&Appearance...")

        onTriggered: {
            const url = "qrc:/qml/components/dialogs/appearance/MpvqcAppearanceDialog.qml"
            const component = Qt.createComponent(url)
            const dialog = component.createObject(appWindow)
            dialog.open()
        }
    }

    Action {
        text: qsTranslate("MainWindow", "&Comment Type Settings...")

        onTriggered: {
            const url = "qrc:/qml/components/dialogs/commentType/MpvqcCommentTypeSettingsDialog.qml"
            const component = Qt.createComponent(url)
            const dialog = component.createObject(appWindow)
            dialog.open()
        }
    }

    MenuSeparator { }

    Action {
        text: qsTranslate("MainWindow", "&Export Settings...")

        onTriggered: {
            const url = "qrc:/qml/components/dialogs/export/MpvqcExportSettingsDialog.qml"
            const component = Qt.createComponent(url)
            const dialog = component.createObject(appWindow)
            dialog.open()
        }
    }

    Action {
        text: qsTranslate("MainWindow", "&Backup Settings...")

        onTriggered: {
            const url = "qrc:/qml/components/dialogs/backup/MpvqcBackupSettingsDialog.qml"
            const component = Qt.createComponent(url)
            const dialog = component.createObject(appWindow)
            dialog.open()
        }
    }

    MenuSeparator { }

    MpvqcAutoWidthMenu {
        title: qsTranslate("MainWindow", "&Language")

        Repeater {
            model: MpvqcLanguageModel {}

            MenuItem {
                text: qsTranslate("Languages", model.language)
                autoExclusive: true
                checkable: true
                checked: model.abbrev === Qt.uiLanguage

                onTriggered: {
                    MpvqcTimer.scheduleOnceAfter(125, loadLanguage)
                }

                function loadLanguage() {
                    Qt.uiLanguage = model.abbrev
                    MpvqcSettings.language=model.abbrev
                }
            }
        }
    }

}
