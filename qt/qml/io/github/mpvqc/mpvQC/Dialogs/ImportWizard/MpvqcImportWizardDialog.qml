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

    readonly property list<string> _stepNames: root.viewModel.steps.map(step => root._stepName(step))

    // This belongs in Python. It sits here because lupdate marks the plural only where it reads the count
    // as a literal. MOVE back when https://bugreports.qt.io/browse/PYSIDE-3418 is fixed
    function _stepName(step: var): string {
        switch (step.kind) {
        case MpvqcImportWizardStepKind.StepKind.ERRORS:
            //: Name of the errors step in the import wizard's step navigation
            return qsTranslate("ImportWizardDialog", "Errors");
        case MpvqcImportWizardStepKind.StepKind.SESSION:
            //: Name of the session step in the import wizard's step navigation
            return qsTranslate("ImportWizardDialog", "Session");
        case MpvqcImportWizardStepKind.StepKind.VIDEO:
            //: Name of the video step in the import wizard's step navigation
            return qsTranslate("ImportWizardDialog", "Video");
        case MpvqcImportWizardStepKind.StepKind.SUBTITLES:
            //: Name of the subtitles step in the import wizard's step navigation, in the singular when a single subtitle is offered
            return qsTranslate("ImportWizardDialog", "Subtitle(s)", "", step.candidateCount);
        default:
            return "";
        }
    }

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

                stepNames: root._stepNames
                currentStepIndex: root.viewModel.currentStepIndex

                Layout.alignment: Qt.AlignHCenter

                onStepClicked: index => root.viewModel.currentStepIndex = index
            }

            Label {
                objectName: "stepName"

                text: root._stepNames[root.viewModel.currentStepIndex]
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
