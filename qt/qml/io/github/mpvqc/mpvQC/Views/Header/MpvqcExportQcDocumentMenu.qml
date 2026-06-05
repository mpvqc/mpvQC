// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls

import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

MpvqcMenuBarMenu {
    id: root
    objectName: "exportQcDocumentMenu"

    signal classicExportTriggered
    signal customExportTriggered(name: string, path: url)

    title: qsTranslate("MainWindow", "Export QC Document")
    icon.source: MpvqcIcons.fileExport

    MpvqcMenuBarItem {
        objectName: "exportClassicMenuItem"
        text: "mpvQC Classic"
        icon.source: MpvqcIcons.mpvqcLogo
        onTriggered: root.classicExportTriggered()
    }

    MenuSeparator {
        visible: _exportTemplateModel.count > 0
        height: visible ? implicitHeight : 0
    }

    Repeater {
        model: MpvqcExportTemplateModel {
            id: _exportTemplateModel
        }

        delegate: MpvqcMenuBarItem {
            required property string name
            required property url path

            text: name
            icon.source: MpvqcIcons.notes
            onTriggered: root.customExportTriggered(name, path)
        }
    }
}
