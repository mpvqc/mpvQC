// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

Item {
    id: root

    required property MpvqcImportWizardViewModel viewModel

    property int sweepDuration: MpvqcConstants.wizardStepMotionDuration

    // Not readonly: the Behavior below writes the interpolated values into it.
    property real _sweptHeight: _card.implicitHeight

    property bool _navigated: false

    function _stepFor(kind: int): var {
        return root.viewModel.steps.find(step => step.kind === kind) ?? null;
    }

    implicitHeight: root._sweptHeight
    clip: true

    MpvqcSectionCard {
        id: _card

        width: root.width
        height: root.height

        Loader {
            id: _errorsStep

            readonly property var stepViewModel: root._stepFor(MpvqcImportWizardStepKind.StepKind.ERRORS)

            active: _errorsStep.stepViewModel !== null
            visible: root.viewModel.currentStepKind === MpvqcImportWizardStepKind.StepKind.ERRORS

            sourceComponent: MpvqcWizardErrorsStep {
                viewModel: _errorsStep.stepViewModel
            }

            Layout.fillWidth: true
        }

        Loader {
            id: _sessionStep

            readonly property var stepViewModel: root._stepFor(MpvqcImportWizardStepKind.StepKind.SESSION)

            active: _sessionStep.stepViewModel !== null
            visible: root.viewModel.currentStepKind === MpvqcImportWizardStepKind.StepKind.SESSION

            sourceComponent: MpvqcWizardSessionStep {
                viewModel: _sessionStep.stepViewModel
            }

            Layout.fillWidth: true
        }

        Loader {
            id: _videoStep

            readonly property var stepViewModel: root._stepFor(MpvqcImportWizardStepKind.StepKind.VIDEO)

            active: _videoStep.stepViewModel !== null
            visible: root.viewModel.currentStepKind === MpvqcImportWizardStepKind.StepKind.VIDEO

            sourceComponent: MpvqcWizardVideoStep {
                viewModel: _videoStep.stepViewModel
            }

            Layout.fillWidth: true
        }

        Loader {
            id: _subtitlesStep

            readonly property var stepViewModel: root._stepFor(MpvqcImportWizardStepKind.StepKind.SUBTITLES)

            active: _subtitlesStep.stepViewModel !== null
            visible: root.viewModel.currentStepKind === MpvqcImportWizardStepKind.StepKind.SUBTITLES

            sourceComponent: MpvqcWizardSubtitlesStep {
                viewModel: _subtitlesStep.stepViewModel
            }

            Layout.fillWidth: true
        }
    }

    Connections {
        target: root.viewModel
        function onCurrentStepChanged(): void {
            root._navigated = true;
        }
    }

    Behavior on _sweptHeight {
        enabled: root._navigated

        NumberAnimation {
            duration: root.sweepDuration
            easing.type: Easing.OutCubic
        }
    }
}
