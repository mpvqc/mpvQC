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


import QtQuick
import QtQuick.Controls
import models
import pyobjects


MenuAutoWidth {

    title: qsTranslate("MainWindow", "&Options")

    MenuAutoWidth {
        title: qsTranslate("MainWindow", "&Language")

        Repeater {
            model: LanguageModel {}
            MenuItem {
                text: qsTranslate("Languages", model.language)
                autoExclusive: true
                checkable: true
                checked: model.abbrev === SettingsPyObject.language
                onTriggered: changeLanguageTimer.start()
                Timer {
                    // Delay it so possible animations have time
                    id: changeLanguageTimer
                    interval: 125
                    onTriggered: TranslationPyObject.load_translation(model.abbrev)
                }
            }
        }
    }

    Action {
        text: qsTranslate("MainWindow", "&Appearance...")
        onTriggered: {
            const component = Qt.createComponent("qrc:/qml/components/DialogAppearance.qml")
            const dialog = component.createObject(appWindow)
            dialog.open()
        }
    }

}
