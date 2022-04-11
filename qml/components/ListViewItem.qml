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
import QtQuick.Layouts
import helpers


Item {

    id: current

    property var index
    property var timeInt
    property var timeStr
    property var type
    property var comment

    width: parent.width
    height: 40

    RowLayout {

        width: parent.width
        spacing: 0

        ButtonPlay {
            id: playButton
            property int time: current.timeInt

            onClicked: {
                eventRegistry.produce(eventRegistry.EventJumpToVideoPosition, playButton.time)
            }
        }

        LabelTime {
            time: current.timeStr
            Layout.minimumWidth: 100
            Layout.maximumWidth: 100
        }

        LabelType {
            text: qsTranslate("CommentTypes", current.type)
            Layout.minimumWidth: CommentTypeWidthCalculator.width
            Layout.maximumWidth: CommentTypeWidthCalculator.width
        }

        LabelComment {
            comment: current.comment
            Layout.fillWidth: parent
        }

        ButtonMore {
            id: button
            property var index: current.index

            onClicked: {
                listView.model.removeRow(button.index)
            }

        }

        Item {
            width: 16
            height: 0
        }

    }

}
