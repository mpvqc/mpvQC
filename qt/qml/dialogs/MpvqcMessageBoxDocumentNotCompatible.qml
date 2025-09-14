// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import "../shared"

MpvqcMessageBox {
    id: root

    property list<string> paths

    title: paths.length === 1
        ? qsTranslate("MessageBoxes", "Document Not Compatible")
        : qsTranslate("MessageBoxes", "Documents Not Compatible")
    text: paths.join("\n")
}
