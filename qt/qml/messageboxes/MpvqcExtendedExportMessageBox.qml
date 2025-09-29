// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

import "../shared"

MpvqcMessageBox {
    title: qsTranslate("MessageBoxes", "Extended Exports")

    //: %1 will be the link to the Jinja templating engine. %2 will be the link to mpvQC's documentation about export templates
    text: qsTranslate("MessageBoxes", "mpvQC allows for customizing report exports using the %1 engine. To begin, visit %2") //
    .arg(`<a href="https://jinja.palletsprojects.com/en/3.1.x/">Jinja template</a>`) //
    .arg(`<a href="https://mpvqc.github.io/export-templates">https://mpvqc.github.io/export-templates</a>`)
}
