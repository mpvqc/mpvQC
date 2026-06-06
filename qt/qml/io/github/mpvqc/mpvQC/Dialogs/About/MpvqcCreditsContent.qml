// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import io.github.mpvqc.mpvQC.Utility

QtObject {
    readonly property var entries: [
        {
            //: This describes the contribution by a group of people
            contribution: qsTranslate("AboutDialog", "Development"),
            names: ["Elias Müller", "Frechdachs"],
            icon: MpvqcIcons.code
        },
        {
            //: This describes the contribution by a group of people
            contribution: qsTranslate("AboutDialog", "Artwork"),
            names: ["maleunam"],
            icon: MpvqcIcons.palette
        },
    ]
}
