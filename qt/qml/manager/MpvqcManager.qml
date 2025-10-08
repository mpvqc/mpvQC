// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import pyobjects

import "../filedialogs"
import "../messageboxes"
import "../shared"

MpvqcObject {
    id: root

    readonly property bool saved: _backend.saved

    function save(): void {
        _backend.save_impl();
    }

    function saveAs(): void {
        _backend.save_as_impl();
    }

    MpvqcManagerBackendPyObject {
        id: _backend

        property var mpvqcDialogExportDocumentFactory: Component {
            MpvqcExportDocumentFileDialog {
                isExtendedExport: false
            }
        }
    }
}
