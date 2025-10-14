// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma Singleton

import QtQuick

import pyobjects

QtObject {
    readonly property MpvqcLabelWidthCalculatorBackend backend: MpvqcLabelWidthCalculatorBackend {}

    property int commentTypesLabelWidth: backend.commentTypesLabelWidth
    property int timeLabelWidth: backend.timeLabelWidth
}
