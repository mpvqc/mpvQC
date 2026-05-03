// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import io.github.mpvqc.mpvQC.Components

MpvqcMenu {
    exit: null

    icon.width: 24
    icon.height: 24

    onAboutToShow: {
        x = isMirrored ? -width + parent.width : 0;
    }
}
