// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import io.github.mpvqc.mpvQC.Python

Loader {
    id: root

    required property bool modalPopupOpen

    readonly property MpvqcSearchBoxViewModel viewModel: MpvqcSearchBoxViewModel {
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

    sourceComponent: MpvqcSearchBoxPopup {
        parent: root.parent
        viewModel: root.viewModel
        modalPopupOpen: root.modalPopupOpen
        onClosed: root.closed()
    }

    onLoaded: (item as MpvqcSearchBoxPopup).open()
}
