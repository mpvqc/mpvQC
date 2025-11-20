// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

MpvqcMenu {
    exit: null

    onAboutToShow: {
        x = isMirrored ? -width + parent.width : 0;
    }
}
