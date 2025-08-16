/*
mpvQC

Copyright (C) 2024 mpvQC developers

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

// https://martin.rpdev.net/2019/01/15/using-delegatemodel-in-qml-for-sorting-and-filtering.html

import QtQuick
import QtQml.Models

DelegateModel {
    property var filterAcceptsItem: item => true

    function update(): void {
        if (items.count > 0) {
            items.setGroups(0, items.count, "items");
        }

        const visible = [];
        for (let i = 0; i < items.count; ++i) {
            const item = items.get(i);
            if (filterAcceptsItem(item.model)) {
                visible.push(item);
            }
        }

        for (let i = 0; i < visible.length; ++i) {
            const item = visible[i];
            item.inVisible = true;
            if (item.visibleIndex !== i) {
                visibleItems.move(item.visibleIndex, i, 1);
            }
        }
    }

    groups: DelegateModelGroup {
        id: visibleItems

        name: "visible"
        includeByDefault: false
    }

    filterOnGroup: "visible"

    Component.onCompleted: {
        _filterModel.update();
    }
}
