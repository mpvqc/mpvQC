// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

MpvqcDialog {
    id: root
    objectName: "importWizardDialog"

    required property MpvqcImportWizardViewModel viewModel

    title: root.viewModel.title
    standardButtons: Dialog.NoButton
    contentWidth: MpvqcConstants.mediumDialogContentWidth
    contentHeight: MpvqcConstants.smallDialogContentHeight
    closePolicy: Popup.NoAutoClose

    Connections {
        target: root.viewModel
        function onAcceptRequested(): void {
            root.accept();
        }
        function onRejectRequested(): void {
            root.reject();
        }
    }

    contentItem: ColumnLayout {
        spacing: 40

        MpvqcWizardStepIndicator {
            id: _stepIndicator
            objectName: "stepIndicator"

            Layout.fillWidth: true
            Layout.topMargin: 32

            stepKinds: root.viewModel.stepKinds
            currentStepIndex: root.viewModel.currentStepIndex

            onStepClicked: index => root.viewModel.currentStepIndex = index
        }

        MpvqcWizardSteps {
            objectName: "stepView"

            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.topMargin: _stepIndicator.visible ? 0 : 32

            clip: true

            viewModel: root.viewModel
        }
    }

    footer: MpvqcImportWizardFooter {
        primaryLabel: root.viewModel.primaryLabel
        showBack: root.viewModel.showBack
        showCancel: root.viewModel.showCancel

        onBackClicked: root.viewModel.back()
        onCancelClicked: root.viewModel.cancelClicked()
        onPrimaryClicked: root.viewModel.primaryClicked()
    }
}
