// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

MpvqcWizardChoiceRow {
    id: root

    required property int index
    required property string filename
    required property string fullPath
    required property bool foundInDocument
    required property bool foundInSubtitle
    required property bool isNoVideo

    required selected

    toolTipText: root.isNoVideo ? "" : root.fullPath
    toolTipSuppressed: _documentPill.hovered || _subtitlePill.hovered

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
