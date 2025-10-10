// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

MpvqcMenu {
    exit: null

    onAboutToShow: {
        x = isMirrored ? -width + parent.width : 0;
        transformOrigin = isMirrored ? Popup.TopRight : Popup.TopLeft;
    }
}
