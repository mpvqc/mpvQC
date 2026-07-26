// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Python

MpvqcOverlayLoader {
    id: root
    objectName: "messageBoxLoader"

    readonly property var _urlsByKind: ({
            [MpvqcMessageBoxKind.MessageBoxKind.CUSTOM_EXPORT]: Qt.resolvedUrl("MpvqcCustomExportMessageBox.qml"),
            [MpvqcMessageBoxKind.MessageBoxKind.EXPORT_ERROR]: Qt.resolvedUrl("MpvqcExportErrorMessageBox.qml"),
            [MpvqcMessageBoxKind.MessageBoxKind.QUIT]: Qt.resolvedUrl("MpvqcQuitMessageBox.qml"),
            [MpvqcMessageBoxKind.MessageBoxKind.RESET]: Qt.resolvedUrl("MpvqcResetMessageBox.qml"),
            [MpvqcMessageBoxKind.MessageBoxKind.VERSION_CHECK]: Qt.resolvedUrl("MpvqcVersionCheckMessageBox.qml")
        })

    function openMessageBox(kind: int): void {
        root.open(root._urlsByKind[kind]);
    }

    function openExportErrorMessageBox(errorMessage: string, errorLine: int): void {
        root.open(root._urlsByKind[MpvqcMessageBoxKind.MessageBoxKind.EXPORT_ERROR], {
            errorMessage: errorMessage,
            errorLine: errorLine
        });
    }
}
