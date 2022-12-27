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


MpvqcDialog {
    id: root

    standardButtons: Dialog.Ok
    closePolicy: Popup.CloseOnEscape

    MpvqcAboutView {
        property string title: qsTranslate("AboutDialog", "About")

        width: root.width
    }

    MpvqcCreditsView {
        property string title: qsTranslate("AboutDialog", "Credits")

        width: root.width
    }

    MpvqcDependenciesView {
        property string title: qsTranslate("AboutDialog", "Dependencies")

        width: root.width
        mpvqcApplication: root.mpvqcApplication
    }
}
