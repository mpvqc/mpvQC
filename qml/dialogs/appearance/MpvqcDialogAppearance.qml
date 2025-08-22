/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

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

    onRejected: {
        _impl.reset();
    }

    ScrollView {
        property string title: qsTranslate("AppearanceDialog", "Appearance")

        width: parent.width

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

    Component.onCompleted: {
        _impl.init();
    }
}
