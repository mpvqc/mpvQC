// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

import pyobjects

import "../shared"

MpvqcMessageBox {
    property var controller: VersionCheckController {}

    title: controller.title || qsTranslate("MessageBoxes", "Checking for Updates...")
    text: controller.text || qsTranslate("MessageBoxes", "Loading...")
}
