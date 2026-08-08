// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Layouts

ColumnLayout {
    id: root

    required property var viewModel

    spacing: 20

    MpvqcWizardStepHeader {
        objectName: "errorsHeader"
        //: Header above the list of QC documents the importer rejected
        text: qsTranslate("ImportWizardDialog", "%Ln QC document(s) could not be imported:", "", _rows.count)
    }

    ColumnLayout {
        spacing: 8

        Layout.fillWidth: true

        Repeater {
            id: _rows
            objectName: "errorRows"

            model: root.viewModel.documents

            delegate: MpvqcWizardErrorsStepDelegate {
                Layout.fillWidth: true
            }
        }
    }
}
