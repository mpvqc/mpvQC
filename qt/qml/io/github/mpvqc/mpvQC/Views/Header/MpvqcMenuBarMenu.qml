// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material as M

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

MpvqcMenu {
    exit: null

    icon.width: 24
    icon.height: 24

    M.Material.background: MpvqcTheme.palette.menuBackground
    M.Material.foreground: MpvqcTheme.palette.foreground

    onAboutToShow: {
        x = isMirrored ? -width + parent.width : 0;
    }
}
