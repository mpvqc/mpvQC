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

    property int highlightMoveDuration: 200

    readonly property int _sectionSpacing: 12

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
                objectName: "colorSchemePreferenceSection"

                title: qsTranslate("AppearanceDialog", "Theme")

                Layout.fillWidth: true
                Layout.topMargin: root._sectionSpacing

                Item {
                    objectName: "colorSchemePreferencePicker"

                    // A repeater builds every swatch up front, so the row stands at its
                    // full height from the first layout pass
                    implicitHeight: _colorSchemePreferences.implicitHeight

                    Layout.fillWidth: true

                    Rectangle {
                        objectName: "colorSchemePreferenceSelectionRing"

                        // Not readonly: the Behavior below writes the interpolated values into it
                        property real _slotX: root.viewModel.colorSchemePreferenceIndex * (root._swatchFrameSize + _colorSchemePreferences.spacing)

                        x: _colorSchemePreferences.x + (_colorSchemePreferences.effectiveLayoutDirection === Qt.RightToLeft ? _colorSchemePreferences.width - width - _slotX : _slotX)
                        width: root._swatchFrameSize
                        height: root._swatchFrameSize
                        radius: root._ringRadius
                        color: "transparent"

                        border {
                            width: root._ringBorder
                            color: MpvqcAppearance.palette.accent
                        }

                        // The slot animates rather than x itself: x also moves when the row
                        // settles or flips direction, and that is not motion anybody asked for
                        Behavior on _slotX {
                            NumberAnimation {
                                duration: root.highlightMoveDuration
                                easing.type: Easing.OutCubic
                            }
                        }
                    }

                    Row {
                        id: _colorSchemePreferences

                        anchors.left: parent.left
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

                title: qsTranslate("AppearanceDialog", "Color")
                expanded: root.viewModel.accentColorSectionVisible

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
