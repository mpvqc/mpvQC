// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import "../shared"

MpvqcMessageBox {
    id: root

    property list<string> paths

    title: qsTranslate("MessageBoxes", "Document Not Compatible", "", paths.length)
    text: paths.join("\n")
}
