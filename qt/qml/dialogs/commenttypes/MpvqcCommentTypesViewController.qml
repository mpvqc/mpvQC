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

QtObject {
    required property int selectedIndex
    required property list<string> model

    property list<string> modelCopy: [...model]
    property bool countIncreased: false

    signal editClicked(string commentType)
    signal highlightIndexRequested(int index)
    signal acceptCopyRequested(list<string> copy)
    signal resetRequested

    function add(commentType: string): void {
        modelCopy.push(commentType);
        highlightIndexRequested(modelCopy.length - 1);
    }

    function replaceWith(commentType: string): void {
        modelCopy[selectedIndex] = commentType;
    }

    function moveUp(): void {
        const current = selectedIndex;
        const previous = current - 1;
        [modelCopy[current], modelCopy[previous]] = [modelCopy[previous], modelCopy[current]];
        highlightIndexRequested(previous);
    }

    function moveDown(): void {
        const current = selectedIndex;
        const next = current + 1;
        [modelCopy[current], modelCopy[next]] = [modelCopy[next], modelCopy[current]];
        highlightIndexRequested(next);
    }

    function startEditing(): void {
        const item = modelCopy[selectedIndex];
        editClicked(item);
    }

    function deleteItem(): void {
        const current = selectedIndex;
        const isLastIndex = current === modelCopy.length - 1;

        modelCopy.splice(current, 1);

        if (isLastIndex) {
            highlightIndexRequested(current - 1);
        } else {
            highlightIndexRequested(current);
        }
    }

    function acceptModelCopy(): void {
        acceptCopyRequested(modelCopy);
    }

    function reset(): void {
        resetRequested();
    }
}
