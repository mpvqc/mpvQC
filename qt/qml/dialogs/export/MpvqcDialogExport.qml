// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import "../../shared"

MpvqcDialog {
    id: root

    title: qsTranslate("ExportSettingsDialog", "Export Settings")

    contentItem: MpvqcExportView {
        id: _exportView

        mpvqcApplication: root.mpvqcApplication
    }

    onAccepted: {
        _exportView.accept();
    }
}
