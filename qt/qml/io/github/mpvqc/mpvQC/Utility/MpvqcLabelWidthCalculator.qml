// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma Singleton

import QtQuick

import io.github.mpvqc.mpvQC.Python

QtObject {
    // Mutable, not readonly: the QML test harness swaps in a fresh view model per test.
    property MpvqcCommentLabelWidthCalculatorViewModel viewModel: MpvqcCommentLabelWidthCalculatorViewModel {}

    property int commentTypesLabelWidth: viewModel.commentTypesLabelWidth
    property int timeLabelWidth: viewModel.timeLabelWidth
}
