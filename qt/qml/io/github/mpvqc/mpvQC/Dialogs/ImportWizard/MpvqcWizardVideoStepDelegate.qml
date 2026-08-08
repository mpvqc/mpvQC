// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

ItemDelegate {
    id: root

    required property int index
    required property string filename
    required property string fullPath
    required property bool foundInDocument
    required property bool foundInSubtitle
    required property bool isNoVideo

    required property bool selected

    property bool _animated: false

    height: Math.max(root.implicitHeight, MpvqcConstants.listRowHeight)
    verticalPadding: 10
    horizontalPadding: 14
    hoverEnabled: true

    ToolTip.text: root.fullPath
    // The pills carry their own tooltip, and two attached tooltips would fight over the shared popup
    ToolTip.visible: !root.isNoVideo && root.hovered && !_documentPill.hovered && !_subtitlePill.hovered
    ToolTip.delay: MpvqcConstants.tooltipDelay

    background: Rectangle {
        // Capped at the shared row height, so a wrapped filename keeps the corner every other row has
        radius: Math.min(height, MpvqcConstants.listRowHeight) / 2
        color: {
            if (root.selected) {
                return Qt.alpha(MpvqcAppearance.palette.accent, 0.16);
            }
            return root.hovered ? Qt.alpha(MpvqcAppearance.palette.foreground, 0.08) : "transparent";
        }

        Behavior on color {
            enabled: root._animated

            ColorAnimation {
                duration: 120
            }
        }
    }

    contentItem: RowLayout {
        spacing: 12

        MpvqcRadioIndicator {
            objectName: "radioIndicator"

            selected: root.selected

            Layout.alignment: Qt.AlignVCenter
        }

        Label {
            objectName: "label"

            text: root.isNoVideo ? qsTranslate("ImportWizardDialog", "Skip video") : root.filename
            horizontalAlignment: Text.AlignLeft
            wrapMode: Text.WrapAtWordBoundaryOrAnywhere

            Layout.fillWidth: true
            Layout.alignment: Qt.AlignVCenter
        }

        MpvqcWizardOriginPill {
            id: _documentPill
            objectName: "fromDocumentPill"

            visible: root.foundInDocument
            icon: MpvqcIcons.description
            selected: root.selected

            //: Tooltip on the per-row origin pill — the candidate video is referenced by one of the QC documents being imported
            toolTipText: qsTranslate("ImportWizardDialog", "Referenced by an imported QC document")

            Layout.alignment: Qt.AlignVCenter
        }

        MpvqcWizardOriginPill {
            id: _subtitlePill
            objectName: "fromSubtitlePill"

            visible: root.foundInSubtitle
            icon: MpvqcIcons.subtitles
            selected: root.selected

            //: Tooltip on the per-row origin pill — the candidate video is referenced by one of the subtitle files being imported
            toolTipText: qsTranslate("ImportWizardDialog", "Referenced by an imported subtitle file")

            Layout.alignment: Qt.AlignVCenter
        }
    }

    Component.onCompleted: root._animated = true
}
