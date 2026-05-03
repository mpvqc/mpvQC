// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import io.github.mpvqc.mpvQC.Components

MpvqcMessageBox {
    objectName: "documentNotCompatibleMessageBox"

    required property list<string> files

    title: qsTranslate("MessageBoxes", "Document Not Compatible", "", files.length)
    text: files.join("\n")
}
