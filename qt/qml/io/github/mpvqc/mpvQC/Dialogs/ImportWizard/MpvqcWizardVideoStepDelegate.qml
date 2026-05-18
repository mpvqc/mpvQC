// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
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

    readonly property int iconSize: 24

    verticalPadding: 16

    contentItem: RowLayout {
        spacing: 12

        MpvqcAnimatedIcon {
            objectName: "radioIcon"

            active: root.selected
            activeIcon: MpvqcIcons.radioButtonChecked
            inactiveIcon: MpvqcIcons.radioButtonUnchecked
            iconColor: MpvqcTheme.palette.foreground
            iconSize: root.iconSize
            activationDuration: 150
            deactivationDuration: 75
        }

        Label {
            objectName: "label"

            Layout.fillWidth: true
            Layout.alignment: Qt.AlignVCenter

            text: root.isNoVideo ? qsTranslate("ImportWizardDialog", "Skip video") : root.filename
            horizontalAlignment: Text.AlignLeft
            wrapMode: Text.Wrap
            maximumLineCount: 2
            elide: Text.ElideRight

            HoverHandler {
                id: _labelHover
            }

            ToolTip.text: root.fullPath
            ToolTip.visible: !root.isNoVideo && _labelHover.hovered
            ToolTip.delay: MpvqcConstants.tooltipDelay
        }

        MpvqcIconLabel {
            objectName: "fromDocumentIcon"

            Layout.preferredWidth: root.iconSize
            Layout.preferredHeight: root.iconSize

            visible: root.foundInDocument
            opacity: 0.6
            icon.source: MpvqcIcons.description
            icon.width: root.iconSize
            icon.height: root.iconSize

            //: Tooltip on the per-row icon — the candidate video is referenced by one of the QC documents being imported
            toolTipText: qsTranslate("ImportWizardDialog", "Referenced by an imported QC document")
        }

        MpvqcIconLabel {
            objectName: "fromSubtitleIcon"

            Layout.preferredWidth: root.iconSize
            Layout.preferredHeight: root.iconSize

            visible: root.foundInSubtitle
            opacity: 0.6
            icon.source: MpvqcIcons.subtitles
            icon.width: root.iconSize
            icon.height: root.iconSize

            //: Tooltip on the per-row icon — the candidate video is referenced by one of the subtitle files being imported
            toolTipText: qsTranslate("ImportWizardDialog", "Referenced by an imported subtitle file")
        }
    }
}
