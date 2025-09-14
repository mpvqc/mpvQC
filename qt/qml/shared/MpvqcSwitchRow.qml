// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

RowLayout {
    id: root

    required property int prefWidth

    property alias toggle: _switch
    property alias checked: _switch.checked
    property alias label: _label.text

    signal toggled(bool checked)

    Label {
        id: _label

        horizontalAlignment: Text.AlignRight
        wrapMode: Text.Wrap
        Layout.preferredWidth: root.prefWidth / 2
    }

    Switch {
        id: _switch

        onCheckedChanged: {
            root.toggled(checked);
        }
    }
}
