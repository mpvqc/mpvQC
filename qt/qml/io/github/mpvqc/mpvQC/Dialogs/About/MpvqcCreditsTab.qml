// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

ScrollView {
    id: root

    readonly property MpvqcCreditsContent creditsContent: MpvqcCreditsContent {}

    readonly property bool isScrollBarShown: contentHeight > height

    function joinNames(names): string {
        // Reversed in RTL so the first entry sits rightmost, where reading starts
        return mirrored ? [...names].reverse().join(", ") : names.join(", ");
    }

    contentWidth: availableWidth

    ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
    ScrollBar.vertical.policy: isScrollBarShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff

    Flickable {
        boundsBehavior: Flickable.StopAtBounds
        contentHeight: _column.implicitHeight

        onVisibleChanged: {
            if (!visible) {
                contentY = 0;
            }
        }

        ColumnLayout {
            id: _column

            x: root.mirrored && root.isScrollBarShown ? 20 : 0
            width: root.availableWidth - (root.isScrollBarShown ? 20 : 0)
            spacing: 0

            Repeater {
                model: root.creditsContent.entries

                MpvqcAboutListItem {
                    required property var modelData

                    text: modelData.contribution
                    supportingText: root.joinNames(modelData.names)
                    icon.source: modelData.icon

                    Layout.fillWidth: true
                }
            }

            Repeater {
                model: MpvqcLanguageModel {}

                MpvqcAboutListItem {
                    required property string language
                    required property var translators

                    objectName: "languageCredit"
                    visible: translators.length > 0
                    text: qsTranslate("Languages", language)
                    supportingText: root.joinNames(translators)
                    icon.source: MpvqcIcons.language

                    Layout.fillWidth: true
                }
            }
        }
    }
}
