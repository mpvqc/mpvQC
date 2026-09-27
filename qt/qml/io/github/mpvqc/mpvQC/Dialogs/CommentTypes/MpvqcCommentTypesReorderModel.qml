// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQml.Models
import QtQuick

import io.github.mpvqc.mpvQC.Utility

DelegateModel {
    id: root

    enum Phase {
        Idle,
        Dragging,
        Settling
    }

    required property ListView view
    // Applies the draft move synchronously, preserving model row identity.
    required property var applyMove

    readonly property Item activeItem: _activeItem
    readonly property bool busy: _phase !== MpvqcCommentTypesReorderModel.Idle
    readonly property bool dragging: _phase === MpvqcCommentTypesReorderModel.Dragging
    readonly property bool settling: _phase === MpvqcCommentTypesReorderModel.Settling
    readonly property bool applyingMove: _applyingMove
    readonly property real pointerY: _pointerY
    readonly property real liftedY: _pointerY - _grabOffset

    property int _phase: MpvqcCommentTypesReorderModel.Idle
    property Item _activeItem: null
    property int _sourceIndex: -1
    property int _previewIndex: -1
    property bool _applyingMove: false
    property real _pointerY: 0
    property real _grabOffset: 0

    readonly property Connections _scrollTracking: Connections {
        target: root.view
        enabled: root.dragging

        function onContentYChanged(): void {
            root._preview();
        }
    }

    function begin(item: Item, sourceIndex: int, pointerY: real, grabOffset: real): void {
        if (busy) {
            return;
        }
        _sourceIndex = sourceIndex;
        _previewIndex = sourceIndex;
        _activeItem = item;
        _pointerY = pointerY;
        _grabOffset = grabOffset;
        _phase = MpvqcCommentTypesReorderModel.Dragging;
        _preview();
    }

    function track(pointerY: real): void {
        if (!dragging) {
            return;
        }
        _pointerY = pointerY;
        _preview();
    }

    function drop(): void {
        if (!dragging) {
            return;
        }
        _phase = MpvqcCommentTypesReorderModel.Settling;
        _applyingMove = true;
        if (_sourceIndex !== _previewIndex) {
            applyMove(_sourceIndex, _previewIndex);
        }
        // Reconcile the preview and model move while transitions are off.
        view.forceLayout();
        _applyingMove = false;
    }

    function finish(): void {
        if (settling) {
            _clear();
        }
    }

    function cancel(): void {
        const rollback = dragging;
        const sourceIndex = _sourceIndex;
        const previewIndex = _previewIndex;
        _clear();
        if (rollback && sourceIndex !== previewIndex) {
            items.move(previewIndex, sourceIndex);
        }
    }

    function _preview(): void {
        const rowHeight = MpvqcConstants.listRowHeight;
        // The destination stays a displayed slot while the pointer is outside the list.
        const center = Math.max(0, Math.min(view.height - 1, liftedY + rowHeight / 2));
        const position = center + view.contentY - view.originY;
        // Qt rounds contentY after a row move; the margin keeps a centre on a slot edge from flipping back.
        if (position > _previewIndex * rowHeight - 1 && position < (_previewIndex + 1) * rowHeight + 1) {
            return;
        }
        const previewIndex = Math.max(0, Math.min(items.count - 1, Math.floor(position / rowHeight)));
        if (previewIndex !== _previewIndex) {
            items.move(_previewIndex, previewIndex);
            _previewIndex = previewIndex;
        }
    }

    function _clear(): void {
        // Lower the row before enabling handlers, or its old grab can restart the drag.
        _activeItem = null;
        _phase = MpvqcCommentTypesReorderModel.Idle;
        _sourceIndex = -1;
        _previewIndex = -1;
    }
}
