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
import QtQuick.Layouts
import settings


MouseArea {
    id: dragArea
    height: row.height

    property alias backgroundColor: rowContent.color
    property alias commentType: label.text
    property int listViewHeight
    property var listViewParent

    property int spacerWidth
    property bool held: false

    signal deletePressed()
    signal editPressed()
    signal moved(var sourceIndex, var targetIndex)
    signal selected()

    drag {
        target: held ? row : undefined
        axis: Drag.YAxis
    }

    onPressed: (event) => {
        const draggerPressed = dragger.x <= event.x && event.x <= (dragger.x + dragger.width)
            && dragger.y <= event.y && event.y <= (dragger.y + dragger.height)
        held = draggerPressed
        selected()
    }

    onReleased: {
        held = false
    }

    onPositionChanged: {
        if (!drag.active) {
            return
        }
        if (row.y <= 0) {
            row.y = 0
        } else if (row.y + row.height >= listViewHeight) {
            row.y = listViewHeight - row.height
        }
    }

    Rectangle {
        id: row
        width: parent.width
        height: dragger.height
        color: 'transparent'

        Drag.active: dragArea.held
        Drag.source: dragArea
        Drag.hotSpot.x: width / 2
        Drag.hotSpot.y: height / 2

        states: State {
            when: dragArea.held

            ParentChange {
                target: row
                parent: listViewParent
            }

            AnchorChanges {
                target: row

                anchors {
                    horizontalCenter: undefined
                    verticalCenter: undefined
                }
            }
        }

        Rectangle {
            id: rowContent
            x: mirrored ? spacerWidth : 0
            height: 45
            width: parent.width - spacerWidth

            RowLayout {
                width: parent.width

                ToolButton {
                    id: dragger
                    hoverEnabled: false
                    enabled: false
                    icon {
                        width: 20
                        height: 20
                        source: "qrc:/data/icons/drag_indicator_black_24dp.svg"
                        color: otherButton.icon.color
                    }
                }

                Label {
                    id: label
                    horizontalAlignment: Text.AlignLeft
                    wrapMode: Text.WordWrap
                    Layout.fillWidth: true
                }

                MpvqcCommentTypeMoreButton {
                    id: otherButton

                    onDeletePressed: {
                        dragArea.deletePressed()
                    }

                    onEditPressed: {
                        dragArea.editPressed()
                    }
                }
            }
        }

    }

    DropArea {
        anchors.fill: parent

        onEntered: (drag) => {
            const source = drag.source.DelegateModel.itemsIndex
            const target = dragArea.DelegateModel.itemsIndex
            moved(source, target)
        }
    }
}
