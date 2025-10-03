// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import pyobjects

DropArea {
    readonly property MpvqcDropAreaViewModel viewModel: MpvqcDropAreaViewModel {}

    onEntered: event => {
        if (viewModel.canHandle(event.formats, event.hasUrls)) {
            event.accept(Qt.LinkAction);
        }
    }

    onDropped: event => {
        if (viewModel.canHandle(event.formats, event.hasUrls)) {
            viewModel.open(event.urls);
        }
    }
}
