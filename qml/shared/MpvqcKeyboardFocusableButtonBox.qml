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

import QtQuick
import QtQuick.Controls.Material

/* Adapted from: qtdeclarative/src/quickcontrols/material/DialogButtonBox.qml */

DialogButtonBox {
    id: root

    visible: count > 0

    contentItem: ListView {
        id: _listView

        focus: true
        implicitWidth: contentWidth
        model: root.contentModel
        spacing: root.spacing
        orientation: ListView.Horizontal
        boundsBehavior: Flickable.StopAtBounds
        snapMode: ListView.SnapToItem

        onCurrentItemChanged: {
            removeFocusFromAllItems();
            applyVisualFocusToCurrentItem();
        }

        function removeFocusFromAllItems(): void {
            for (let i = 0; i < _listView.count; i++) {
                _listView.model.get(i).down = false;
            }
        }

        function applyVisualFocusToCurrentItem(): void {
            if (currentItem) {
                currentItem.down = true;
            }
        }

        function focusRejectedButton(): void {
            const button = root.standardButton(Dialog.Cancel) ?? root.standardButton(Dialog.No) ?? root.standardButton(Dialog.Close);

            if (button) {
                for (let idx = 0; idx < _listView.count; idx++) {
                    if (_listView.model.get(idx) === button) {
                        _listView.currentIndex = idx;
                    }
                }
            }
        }
    }

    Component.onCompleted: {
        _listView.focusRejectedButton();
    }

    Shortcut {
        sequence: "return"

        onActivated: {
            _listView.currentItem.clicked();
        }
    }

    Shortcut {
        sequence: "tab"

        onActivated: {
            _listView.incrementCurrentIndex();
        }
    }

    Shortcut {
        sequence: "shift+tab"

        onActivated: {
            _listView.decrementCurrentIndex();
        }
    }
}
