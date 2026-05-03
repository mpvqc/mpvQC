// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import io.github.mpvqc.mpvQC.Python

Loader {
    id: root

    required property var model
    required property int selectedIndex

    readonly property MpvqcSearchBoxViewModel viewModel: MpvqcSearchBoxViewModel {
        model: root.model
        selectedIndex: root.selectedIndex
        onHighlightRequested: index => root.highlightRequested(index)
    }

    readonly property string searchQuery: (item as MpvqcSearchBoxPopup)?.searchQuery ?? ""

    signal highlightRequested(index: int)
    signal closed

    function show(): void {
        if (root.active) {
            (root.item as MpvqcSearchBoxPopup).open();
        } else {
            root.active = true;
        }
    }

    active: false
    visible: active

    onLoaded: (item as MpvqcSearchBoxPopup).open()

    sourceComponent: MpvqcSearchBoxPopup {
        parent: root.parent
        viewModel: root.viewModel
        onClosed: root.closed()
    }
}
