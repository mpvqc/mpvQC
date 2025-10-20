// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

Loader {
    id: root

    required property var viewModel
    required property var searchBoxViewModel

    readonly property string searchQuery: item?.searchQuery ?? ""

    signal closed

    active: false
    visible: active

    onLoaded: item.open() // qmllint disable

    sourceComponent: MpvqcSearchBoxPopup {
        parent: root.parent
        viewModel: root.searchBoxViewModel
        onClosed: root.closed()
    }

    Connections {
        target: root.viewModel

        function onShowSearchBoxRequested(): void {
            if (root.active) {
                root.item.open(); // qmllint disable
            } else {
                root.active = true;
            }
        }
    }
}
