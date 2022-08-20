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


Label {
    text: Qt.application.name
    elide: LayoutMirroring.enabled ? Text.ElideLeft: Text.ElideRight
    horizontalAlignment: Text.AlignHCenter
    verticalAlignment: Text.AlignVCenter

    function reEvaluateTitle() {
        let title = getTitle()
        if (qcManager.saved) {
            text = title
        } else {
            //: Window title in unsaved state
            text = qsTranslate("MainWindow", "%1 (unsaved)").arg(title)
        }
    }

    function getTitle() {
        return Qt.application.name
    }

    Connections {
        target: qcManager

        function onSavedChanged() {
            reEvaluateTitle()
        }
    }
}
