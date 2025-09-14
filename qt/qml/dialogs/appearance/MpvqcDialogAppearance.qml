// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material

import "../../shared"

MpvqcDialog {
    id: root

    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    readonly property var mpvqcTheme: mpvqcApplication.mpvqcTheme

    readonly property var _: QtObject {
        id: _impl

        property var initialThemeIdentifier: null
        property var initialThemeColorOption: null

        function init(): void {
            initialThemeIdentifier = root.mpvqcSettings.themeIdentifier;
            initialThemeColorOption = root.mpvqcSettings.themeColorOption;
        }

        function applyTheme(themeIdentifier: string): void {
            root.mpvqcSettings.themeIdentifier = themeIdentifier;
        }

        function applyColorOption(themeColorOption: int): void {
            root.mpvqcSettings.themeColorOption = themeColorOption;
        }

        function reset(): void {
            root.mpvqcSettings.themeIdentifier = initialThemeIdentifier;
            root.mpvqcSettings.themeColorOption = initialThemeColorOption;
        }
    }

    title: qsTranslate("AppearanceDialog", "Appearance")

    contentItem: ScrollView {

        Column {
            width: parent.width

            MpvqcHeader {
                text: qsTranslate("AppearanceDialog", "Theme")
                width: parent.width
            }

            MpvqcThemeView {
                id: _themeView

                width: parent.width

                mpvqcTheme: root.mpvqcTheme
                currentThemeIdentifier: root.mpvqcSettings.themeIdentifier

                onThemeIdentifierPressed: themeIdentifier => {
                    _impl.applyTheme(themeIdentifier);
                }

                // workaround padding issue in rtl
                Binding on x {
                    when: root.mirrored
                    value: -8
                }
            }

            MpvqcHeader {
                text: qsTranslate("AppearanceDialog", "Color")
                width: parent.width
            }

            MpvqcColorView {
                id: _colorView

                width: parent.width

                mpvqcTheme: root.mpvqcTheme
                currentThemeColorOption: root.mpvqcSettings.themeColorOption

                onColorOptionPressed: colorOption => {
                    _impl.applyColorOption(colorOption);
                }
            }
        }
    }

    onRejected: {
        _impl.reset();
    }

    Component.onCompleted: {
        _impl.init();
    }
}
