// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import "../../shared"

MpvqcDialog {
    title: qsTranslate("ShortcutsDialog", "Keyboard Shortcuts")

    contentWidth: 500
    contentHeight: Math.min(1080, mpvqcApplication.height * 0.75)

    contentItem: MpvqcShortcutView {}
}
