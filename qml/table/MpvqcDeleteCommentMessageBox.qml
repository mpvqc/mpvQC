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

import QtQuick.Controls.Material

import "../shared"

MpvqcMessageBox {
    id: root

    required property int commentIndex

    signal deleteCommentConfirmed(index: int)

    title: qsTranslate("MessageBoxes", "Delete Comment")
    text: qsTranslate("MessageBoxes", "Do you really want to delete this comment?")
    standardButtons: Dialog.Yes | Dialog.Cancel

    onAccepted: {
        root.deleteCommentConfirmed(root.commentIndex);
    }
}
