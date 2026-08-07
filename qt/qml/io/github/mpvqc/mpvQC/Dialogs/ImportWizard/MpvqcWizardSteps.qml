// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls

import io.github.mpvqc.mpvQC.Python

StackView {
    id: root

    required property MpvqcImportWizardViewModel viewModel
    readonly property real slideDistance: width / 4
    property int animationDuration: 120

    function _stepComponentFor(step: var): Component {
        switch (step.kind) {
        case MpvqcImportWizardStepKind.StepKind.ERRORS:
            return _errorsStep;
        case MpvqcImportWizardStepKind.StepKind.SESSION:
            return _sessionStep;
        case MpvqcImportWizardStepKind.StepKind.VIDEO:
            return _videoStep;
        case MpvqcImportWizardStepKind.StepKind.SUBTITLES:
            return _subtitlesStep;
        }
        return null;
    }

    pushEnter: Transition {
        ParallelAnimation {
            NumberAnimation {
                property: "opacity"
                from: 0
                to: 1
                duration: root.animationDuration
                easing.type: Easing.OutCubic
            }
            NumberAnimation {
                property: "x"
                from: root.slideDistance
                to: 0
                duration: root.animationDuration
                easing.type: Easing.OutCubic
            }
        }
    }

    pushExit: Transition {
        ParallelAnimation {
            NumberAnimation {
                property: "opacity"
                from: 1
                to: 0
                duration: root.animationDuration
                easing.type: Easing.OutCubic
            }
            NumberAnimation {
                property: "x"
                from: 0
                to: -root.slideDistance
                duration: root.animationDuration
                easing.type: Easing.OutCubic
            }
        }
    }

    popEnter: Transition {
        ParallelAnimation {
            NumberAnimation {
                property: "opacity"
                from: 0
                to: 1
                duration: root.animationDuration
                easing.type: Easing.OutCubic
            }
            NumberAnimation {
                property: "x"
                from: -root.slideDistance
                to: 0
                duration: root.animationDuration
                easing.type: Easing.OutCubic
            }
        }
    }

    popExit: Transition {
        ParallelAnimation {
            NumberAnimation {
                property: "opacity"
                from: 1
                to: 0
                duration: root.animationDuration
                easing.type: Easing.OutCubic
            }
            NumberAnimation {
                property: "x"
                from: 0
                to: root.slideDistance
                duration: root.animationDuration
                easing.type: Easing.OutCubic
            }
        }
    }

    Component.onCompleted: {
        const step = root.viewModel.steps[root.viewModel.currentStepIndex];
        root.push(root._stepComponentFor(step), {
            viewModel: step
        }, StackView.Immediate);
    }

    Connections {
        target: root.viewModel

        function onNavigated(direction: int) {
            const step = root.viewModel.steps[root.viewModel.currentStepIndex];
            const forward = direction === MpvqcImportWizardNavigationDirection.NavigationDirection.FORWARD;
            const operation = forward ? StackView.PushTransition : StackView.PopTransition;
            root.replace(root._stepComponentFor(step), {
                viewModel: step
            }, operation);
        }
    }

    Component {
        id: _errorsStep

        MpvqcWizardErrorsStep {}
    }

    Component {
        id: _sessionStep

        MpvqcWizardSessionStep {}
    }

    Component {
        id: _videoStep

        MpvqcWizardVideoStep {}
    }

    Component {
        id: _subtitlesStep

        MpvqcWizardSubtitlesStep {}
    }
}
