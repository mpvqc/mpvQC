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
    objectName: "appearanceDialog"

    readonly property MpvqcAppearanceDialogViewModel viewModel: MpvqcAppearanceDialogViewModel {}

    readonly property int _sectionSpacing: 12
    readonly property int _highlightMoveDuration: 200

    // the ring surrounds the swatch, so both read the same frame size
    readonly property int _swatchFrameSize: 70
    readonly property int _swatchSpacing: 16
    readonly property int _ringRadius: 23
    readonly property int _ringBorder: 3

    contentHeight: MpvqcConstants.smallDialogContentHeight

    title: qsTranslate("AppearanceDialog", "Appearance")
    standardButtons: Dialog.Ok | Dialog.Cancel

    contentItem: ScrollView {
        id: _scroll

        contentWidth: availableWidth
        contentHeight: _sections.implicitHeight

        ColumnLayout {
            id: _sections

            width: _scroll.availableWidth
            spacing: root._sectionSpacing

            MpvqcAppearanceSection {
                objectName: "colorSchemeSection"

                title: qsTranslate("AppearanceDialog", "Color scheme")

                Layout.fillWidth: true
                Layout.topMargin: root._sectionSpacing

                Item {
                    objectName: "colorSchemePicker"

                    // A repeater builds every swatch up front, so the row stands at its
                    // full height from the first layout pass
                    implicitHeight: _colorSchemePreferences.implicitHeight

                    Layout.fillWidth: true

                    Rectangle {
                        x: root.viewModel.colorSchemePreferenceIndex * (root._swatchFrameSize + _colorSchemePreferences.spacing)
                        width: root._swatchFrameSize
                        height: root._swatchFrameSize
                        radius: root._ringRadius
                        color: "transparent"

                        border {
                            width: root._ringBorder
                            color: MpvqcAppearance.palette.accent
                        }

                        Behavior on x {
                            NumberAnimation {
                                duration: root._highlightMoveDuration
                                easing.type: Easing.OutCubic
                            }
                        }
                    }

                    Row {
                        id: _colorSchemePreferences

                        spacing: root._swatchSpacing

                        Repeater {
                            model: MpvqcColorSchemePreferenceModel {}

                            delegate: MpvqcColorSchemePreferenceSwatch {
                                id: _colorSchemePreferenceSwatch

                                required property int index

                                frameSize: root._swatchFrameSize
                                selected: _colorSchemePreferenceSwatch.index === root.viewModel.colorSchemePreferenceIndex

                                onPicked: preference => root.viewModel.setColorSchemePreference(preference)
                            }
                        }
                    }
                }
            }

            MpvqcAppearanceSection {
                objectName: "accentColorSection"

                title: qsTranslate("AppearanceDialog", "Accent color")
                expanded: root.viewModel.accentSectionVisible

                Layout.fillWidth: true

                Flow {
                    objectName: "accentColorFlow"

                    spacing: 4

                    Layout.fillWidth: true

                    Repeater {
                        model: root.viewModel.accentColorModel

                        delegate: MpvqcAccentColorSwatch {
                            id: _accentColorSwatch

                            selected: _accentColorSwatch.index === root.viewModel.accentColorIndex

                            onPicked: accentColor => root.viewModel.setAccentColor(accentColor)
                        }
                    }
                }
            }
        }
    }

    onRejected: root.viewModel.reject()
}
