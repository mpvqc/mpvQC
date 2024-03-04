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

import shared


MpvqcDialog {
    id: root

    readonly property int singleColumn: mpvqcApplication.width < 1080

    contentWidth: singleColumn ? 490 : 950
    contentHeight: Math.min(1080, mpvqcApplication.height * 0.75)

    /*
     * For some reason property binding didn't do the job,
     * so we force the engine to recreate the component when the window becomes small enough.
     */

    readonly property var largeLayoutView: Component
    {
        MpvqcShortcutView {
            singleColumn: false
        }
    }

    readonly property var smallLayoutView: Component
    {
        MpvqcShortcutView {
            singleColumn: true
        }
    }

    Loader {
        id: _loader

        property string title: qsTranslate("ShortcutsDialog", "Keyboard Shortcuts")

        sourceComponent: root.singleColumn ? smallLayoutView : largeLayoutView
    }
}
