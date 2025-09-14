// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import "../../shared"

MpvqcDialog {
    id: root

    title: qsTranslate("BackupDialog", "Backup Settings")

    contentItem: MpvqcBackupView {
        id: _backupView

        mpvqcApplication: root.mpvqcApplication
    }

    onAccepted: {
        _backupView.accept();
    }
}
