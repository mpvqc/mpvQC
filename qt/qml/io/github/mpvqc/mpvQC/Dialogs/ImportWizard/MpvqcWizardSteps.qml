// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import io.github.mpvqc.mpvQC.Python

StackView {
    id: root

    required property MpvqcImportWizardViewModel viewModel
    property int animationDuration: 120
    readonly property real slideDistance: width / 4

    property int _lastIndex: 0

    initialItem: root._stepComponentFor(root.viewModel.stepKinds[0])

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

    Connections {
        target: root.viewModel

        function onCurrentStepChanged() {
            const currentIndex = root.viewModel.currentStepIndex;
            const kind = root.viewModel.stepKinds[currentIndex];
            if (currentIndex > root._lastIndex) {
                root.replace(root._stepComponentFor(kind), {}, StackView.PushTransition);
            } else if (currentIndex < root._lastIndex) {
                root.replace(root._stepComponentFor(kind), {}, StackView.PopTransition);
            }
            root._lastIndex = currentIndex;
        }
    }

    function _stepComponentFor(kind: int): Component {
        switch (kind) {
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

    Component {
        id: _errorsStep

        MpvqcWizardErrorsStep {
            viewModel: root.viewModel.errorsStepViewModel
        }
    }

    Component {
        id: _sessionStep

        MpvqcWizardSessionStep {
            viewModel: root.viewModel.sessionStepViewModel
        }
    }

    Component {
        id: _videoStep

        MpvqcWizardVideoStep {
            viewModel: root.viewModel.videoStepViewModel
        }
    }

    Component {
        id: _subtitlesStep

        MpvqcWizardSubtitlesStep {
            viewModel: root.viewModel.subtitlesStepViewModel
        }
    }
}
