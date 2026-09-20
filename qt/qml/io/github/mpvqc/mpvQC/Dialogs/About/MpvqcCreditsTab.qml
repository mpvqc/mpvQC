// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

MpvqcAboutScrollView {
    id: root

    readonly property MpvqcCreditsContent creditsContent: MpvqcCreditsContent {}

    function joinNames(names): string {
        // Reversed in RTL so the first entry sits rightmost, where reading starts
        return mirrored ? [...names].reverse().join(", ") : names.join(", ");
    }

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

            width: root.availableWidth
            spacing: MpvqcConstants.dialogSectionSpacing

            MpvqcSectionCard {
                Layout.fillWidth: true

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
            }

            MpvqcSectionCard {
                Layout.fillWidth: true

                Repeater {
                    model: MpvqcLanguageModel {}

                    MpvqcAboutListItem {
                        objectName: "languageCredit"

                        required property string language
                        required property var translators

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
}
