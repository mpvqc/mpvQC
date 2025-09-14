// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

// https://martin.rpdev.net/2019/01/15/using-delegatemodel-in-qml-for-sorting-and-filtering.html

import QtQuick
import QtQml.Models

DelegateModel {
    property var filterAcceptsItem: item => true

    groups: DelegateModelGroup {
        id: visibleItems

        name: "visible"
        includeByDefault: false
    }

    filterOnGroup: "visible"

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

    Component.onCompleted: {
        update();
    }
}
