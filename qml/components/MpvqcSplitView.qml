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
import Qt.labs.settings
import components.player
import components.table
import pyobjects


SplitView {
    id: splitView
    orientation: Qt.Vertical

    Settings {
        id: settings
        fileName: SettingsPyObject.backing_object_file_name
        category: "SplitView"
    }

    Item {
        SplitView.fillHeight: true

        MpvqcPlayer {}
    }

    Item {
        SplitView.preferredHeight: appWindow.height / 5

        Component.onCompleted: {
            splitView.restoreState(settings.value("dimensions"))
        }
        Component.onDestruction: {
            settings.setValue("dimensions", splitView.saveState())
        }

        MpvqcCommentTable {
            anchors.fill: parent
        }
    }

}
