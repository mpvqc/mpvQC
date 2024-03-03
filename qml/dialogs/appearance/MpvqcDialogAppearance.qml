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

    ScrollView {
        property string title: qsTranslate("AppearanceDialog", "Appearance")

        width: parent.width

        Column {
            width: parent.width

            MpvqcHeader {
                text: qsTranslate("AppearanceDialog", "Theme")
                width: parent.width
            }

            MpvqcThemeView {
                mpvqcApplication: root.mpvqcApplication
                width: parent.width

                // workaround padding issue in rtl
                Binding on x { when: root.mirrored; value: -8 }
            }

            MpvqcHeader {
                text: qsTranslate("AppearanceDialog", "Color")
                width: parent.width
            }

            MpvqcColorView {
                mpvqcApplication: root.mpvqcApplication
                width: parent.width
            }
        }
    }

}
