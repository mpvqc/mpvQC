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

    property int _focusedIndex: 0

    function _initFocus(): void {
        for (let idx = 0; idx < count; idx++) {
            const item = contentModel.get(idx);
            if (!item)
                continue;
            const role = item.DialogButtonBox.buttonRole;
            if (role === DialogButtonBox.RejectRole || role === DialogButtonBox.NoRole) {
                _focusedIndex = idx;
                _updateVisualFocus();
                return;
            }
        }
        _focusedIndex = 0;
        _updateVisualFocus();
    }

    function _updateVisualFocus(): void {
        for (let i = 0; i < count; i++) {
            const item = contentModel.get(i);
            if (item)
                item.down = (i === _focusedIndex);
        }
    }

    visible: count > 0

    contentItem: ListView {
        id: _listView

        currentIndex: root._focusedIndex
        implicitWidth: contentWidth
        model: root.contentModel
        spacing: root.spacing
        orientation: ListView.Horizontal
        boundsBehavior: Flickable.StopAtBounds
        snapMode: ListView.SnapToItem
    }

    Component.onCompleted: {
        _initFocus();
    }

    Shortcut {
        sequence: "return"
        onActivated: {
            const item = root.contentModel.get(root._focusedIndex);
            if (item) {
                item.clicked();
            }
        }
    }

    Shortcut {
        sequence: "tab"
        onActivated: {
            root._focusedIndex = (root._focusedIndex + 1) % root.count;
            root._updateVisualFocus();
        }
    }

    Shortcut {
        sequence: "shift+tab"
        onActivated: {
            root._focusedIndex = (root._focusedIndex - 1 + root.count) % root.count;
            root._updateVisualFocus();
        }
    }

    Shortcut {
        sequence: "right"
        onActivated: {
            root._focusedIndex = (root._focusedIndex + (root.isMirrored ? -1 : 1) + root.count) % root.count;
            root._updateVisualFocus();
        }
    }

    Shortcut {
        sequence: "left"
        onActivated: {
            root._focusedIndex = (root._focusedIndex + (root.isMirrored ? 1 : -1) + root.count) % root.count;
            root._updateVisualFocus();
        }
    }

    LayoutMirroring.enabled: isMirrored
    LayoutMirroring.childrenInherit: true
}
