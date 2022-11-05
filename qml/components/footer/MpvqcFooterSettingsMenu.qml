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
import components
import settings


MpvqcAutoWidthMenu {
    modal: true
    dim: false
    y: -height
    transformOrigin: mirrored ? Popup.BottomLeft : Popup.BottomRight

    MenuItem {
        text: qsTranslate("MainWindow", "Default format")
        checked: MpvqcSettings.timeFormat === MpvqcSettings.TimeFormat.CURRENT_TOTAL_TIME
        autoExclusive: true
        checkable: true


        onTriggered: {
            MpvqcSettings.timeFormat = MpvqcSettings.TimeFormat.CURRENT_TOTAL_TIME
        }
    }

    MenuItem {
        text: qsTranslate("MainWindow", "Current time")
        checked: MpvqcSettings.timeFormat === MpvqcSettings.TimeFormat.CURRENT_TIME
        autoExclusive: true
        checkable: true

        onTriggered: {
            MpvqcSettings.timeFormat = MpvqcSettings.TimeFormat.CURRENT_TIME
        }
    }

    MenuItem {
        text: qsTranslate("MainWindow", "Remaining time")
        checked: MpvqcSettings.timeFormat === MpvqcSettings.TimeFormat.REMAINING_TIME
        autoExclusive: true
        checkable: true

        onTriggered: {
            MpvqcSettings.timeFormat = MpvqcSettings.TimeFormat.REMAINING_TIME
        }
    }

    MenuItem {
        text: qsTranslate("MainWindow", "Hide time")
        checked: MpvqcSettings.timeFormat === MpvqcSettings.TimeFormat.EMPTY
        autoExclusive: true
        checkable: true

        onTriggered: {
            MpvqcSettings.timeFormat = MpvqcSettings.TimeFormat.EMPTY
        }
    }

    MenuSeparator { }

    Action {
        text: qsTranslate("MainWindow", "Progress in percent")
        checked: MpvqcSettings.statusbarPercentage
        checkable: true

        onTriggered: {
            MpvqcSettings.statusbarPercentage = checked
        }
    }

}
