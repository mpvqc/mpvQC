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

import shared
import settings

MpvqcMenu {
    id: root

    required property var mpvqcApplication

    property var mpvqcSettings: mpvqcApplication.mpvqcSettings

    property alias defaultFormat: _defaultFormat
    property alias currentTimeFormat: _currentTimeFormat
    property alias remainingTimeFormat: _remainingTimeFormat
    property alias hideTimeFormat: _hideTimeFormat
    property alias percentage: _percentage

    modal: true
    dim: false

    MenuItem {
        id: _defaultFormat

        text: qsTranslate("MainWindow", "Default format")
        checked: root.mpvqcSettings.timeFormat === MpvqcSettings.TimeFormat.CURRENT_TOTAL_TIME
        autoExclusive: true
        checkable: true

        onTriggered: {
            root.mpvqcSettings.timeFormat = MpvqcSettings.TimeFormat.CURRENT_TOTAL_TIME;
        }
    }

    MenuItem {
        id: _currentTimeFormat

        text: qsTranslate("MainWindow", "Current time")
        checked: root.mpvqcSettings.timeFormat === MpvqcSettings.TimeFormat.CURRENT_TIME
        autoExclusive: true
        checkable: true

        onTriggered: {
            root.mpvqcSettings.timeFormat = MpvqcSettings.TimeFormat.CURRENT_TIME;
        }
    }

    MenuItem {
        id: _remainingTimeFormat

        text: qsTranslate("MainWindow", "Remaining time")
        checked: root.mpvqcSettings.timeFormat === MpvqcSettings.TimeFormat.REMAINING_TIME
        autoExclusive: true
        checkable: true

        onTriggered: {
            root.mpvqcSettings.timeFormat = MpvqcSettings.TimeFormat.REMAINING_TIME;
        }
    }

    MenuItem {
        id: _hideTimeFormat

        text: qsTranslate("MainWindow", "Hide time")
        checked: root.mpvqcSettings.timeFormat === MpvqcSettings.TimeFormat.EMPTY
        autoExclusive: true
        checkable: true

        onTriggered: {
            root.mpvqcSettings.timeFormat = MpvqcSettings.TimeFormat.EMPTY;
        }
    }

    MenuSeparator {}

    Action {
        id: _percentage

        text: qsTranslate("MainWindow", "Progress in percent")
        checked: root.mpvqcSettings.statusbarPercentage
        checkable: true

        onTriggered: {
            root.mpvqcSettings.statusbarPercentage = checked;
        }
    }
}
