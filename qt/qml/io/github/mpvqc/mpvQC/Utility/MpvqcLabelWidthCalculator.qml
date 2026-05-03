// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma Singleton

import QtQuick

import io.github.mpvqc.mpvQC.Python

QtObject {
    readonly property MpvqcLabelWidthCalculatorViewModel viewModel: MpvqcLabelWidthCalculatorViewModel {}

    property int commentTypesLabelWidth: viewModel.commentTypesLabelWidth
    property int timeLabelWidth: viewModel.timeLabelWidth
}
