// SPDX-FileCopyrightText: 2017 The Qt Company Ltd.
// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

/* Adapted from: qtdeclarative/src/quickcontrols/material/DialogButtonBox.qml */

DialogButtonBox {
    id: root

    readonly property bool isMirrored: Application.layoutDirection === Qt.RightToLeft

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

    LayoutMirroring.enabled: isMirrored
    LayoutMirroring.childrenInherit: true
}
