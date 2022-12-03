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
import models

Item {
    required property int selectedIndex
    required property MpvqcCommentTypesModel model

    readonly property MpvqcCommentTypesModel modelCopy: model.copy(parent)
    readonly property int thisItemOnly: 1

    signal editClicked(string commentType)

    width: 0; height: 0

    function add(commentType: string): void {
        modelCopy.add(commentType)
    }

    function replaceWith(commentType: string): void {
        modelCopy.replace(selectedIndex, commentType)
    }

    function moveUp(): void {
        modelCopy.move(selectedIndex, selectedIndex - 1, thisItemOnly)
    }

    function moveDown(): void {
        modelCopy.move(selectedIndex, selectedIndex + 1, thisItemOnly)
    }

    function startEditing(): void {
        const item = modelCopy.get(selectedIndex)
        editClicked(item.type)
    }

    function deleteItem(): void {
        modelCopy.remove(selectedIndex)
    }

    function acceptModelCopy(): void {
        if (modelCopy.count === 0) {
            modelCopy.reset(parent)
        }
        model.replaceWith(modelCopy.items())
    }

    function reset(): void {
        modelCopy.reset(parent)
    }

}
