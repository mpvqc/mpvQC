// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import "../../shared"

MpvqcDialog {
    id: root

    title: qsTranslate("ImportSettingsDialog", "Import Settings")

    contentItem: MpvqcImportView {
        id: _importView

        mpvqcApplication: root.mpvqcApplication
    }

    onAccepted: {
        _importView.accept();
    }
}
