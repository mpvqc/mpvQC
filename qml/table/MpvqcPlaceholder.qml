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


Flickable {
    id: root

    clip: true

    component MpvqcDescriptiveText: Label {
        Layout.alignment : Qt.AlignVCenter | Qt.AlignRight
    }

    component MpvqcButtonRendered: Button {
        enabled: false
        contentItem: Label {
            text: parent.text
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    GridLayout {
        anchors.centerIn: root.contentItem
        columns: 2
        columnSpacing: 30

        MpvqcDescriptiveText {
            text: qsTranslate("CommentTable", "Open QC Document(s)")
        }

        RowLayout {

            MpvqcButtonRendered {
                text: qsTranslate("CommentTable", "Ctrl")
            }

            Label {
                text: '+'
            }

            MpvqcButtonRendered {
                text: 'O'
            }

        }


        MpvqcDescriptiveText {
            text: qsTranslate("CommentTable", "Open Video")
        }

        RowLayout {

            MpvqcButtonRendered {
                text: qsTranslate("CommentTable", "Ctrl")
            }

            Label {
                text: '+'
            }

            MpvqcButtonRendered {
                text: qsTranslate("CommentTable", "Shift")
            }

            Label {
                text: '+'
            }

            MpvqcButtonRendered {
                text: 'O'
            }

        }


        MpvqcDescriptiveText {
            text: qsTranslate("CommentTable", "Add Comment")
        }

        MpvqcButtonRendered {
            text: 'E'
        }

    }

}
