// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
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

    contentItem: ColumnLayout {
        spacing: 20

        ColumnLayout {
            id: _stepNavigation

            spacing: 20
            visible: root.viewModel.multiStep

            Layout.alignment: Qt.AlignHCenter
            Layout.topMargin: 24

            MpvqcWizardStepPager {
                objectName: "stepPager"

                stepNames: root.viewModel.stepNames
                currentStepIndex: root.viewModel.currentStepIndex

                Layout.alignment: Qt.AlignHCenter

                onStepClicked: index => root.viewModel.currentStepIndex = index
            }

            Label {
                objectName: "stepName"

                text: root.viewModel.currentStepName
                font.weight: Font.DemiBold
                horizontalAlignment: Text.AlignHCenter

                Layout.alignment: Qt.AlignHCenter
            }
        }

        MpvqcWizardStepScrollView {
            id: _stepScroll
            objectName: "stepScroll"

            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.topMargin: _stepNavigation.visible ? 0 : 24

            MpvqcWizardSteps {
                objectName: "stepView"

                viewModel: root.viewModel

                Layout.fillWidth: true
            }
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

    onAccepted: root.viewModel.finish()
    onRejected: root.viewModel.dismiss()

    Connections {
        target: root.viewModel

        function onCurrentStepChanged(): void {
            _stepScroll.scrollToTop();
        }

        function onAcceptRequested(): void {
            root.accept();
        }

        function onRejectRequested(): void {
            root.reject();
        }
    }
}
