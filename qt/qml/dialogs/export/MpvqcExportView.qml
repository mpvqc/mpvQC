// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Layouts

import "../../shared"

ColumnLayout {
    id: root

    required property var mpvqcApplication

    property var mpvqcSettings: mpvqcApplication.mpvqcSettings

    property alias nicknameInput: _nicknameInput
    property alias dateToggle: _dateToggle
    property alias generatorToggle: _generatorToggle
    property alias nicknameToggle: _nicknameToggle
    property alias pathToggle: _pathToggle

    property string currentNickname: root.mpvqcSettings.nickname
    property bool currentWriteHeaderDate: root.mpvqcSettings.writeHeaderDate
    property bool currentWriteHeaderGenerator: root.mpvqcSettings.writeHeaderGenerator
    property bool currentWriteHeaderNickname: root.mpvqcSettings.writeHeaderNickname
    property bool currentWriteHeaderVideoPath: root.mpvqcSettings.writeHeaderVideoPath

    function accept(): void {
        root.mpvqcSettings.nickname = currentNickname;
        root.mpvqcSettings.writeHeaderDate = currentWriteHeaderDate;
        root.mpvqcSettings.writeHeaderGenerator = currentWriteHeaderGenerator;
        root.mpvqcSettings.writeHeaderNickname = currentWriteHeaderNickname;
        root.mpvqcSettings.writeHeaderVideoPath = currentWriteHeaderVideoPath;
    }

    MpvqcTextFieldRow {
        id: _nicknameInput

        label: qsTranslate("ExportSettingsDialog", "Nickname")
        input: root.currentNickname
        spacing: 16
        fontWeight: Font.DemiBold
        prefWidth: root.width
        implicitTextFieldWidth: 150
        Layout.topMargin: 20

        onTextChanged: text => {
            root.currentNickname = text;
        }
    }

    MpvqcHeader {
        text: qsTranslate("ExportSettingsDialog", "Document Header")
        Layout.topMargin: 30
        Layout.bottomMargin: 10
        Layout.fillWidth: true

        horizontalAlignment: Text.AlignHCenter
    }

    MpvqcSwitchRow {
        id: _dateToggle

        label: qsTranslate("ExportSettingsDialog", "Write Date")
        checked: root.currentWriteHeaderDate
        prefWidth: root.width

        onToggled: state => {
            root.currentWriteHeaderDate = state;
        }
    }

    MpvqcSwitchRow {
        id: _generatorToggle

        //: %1 will be the application name. Most probably 'mpvQC' :)
        label: qsTranslate("ExportSettingsDialog", "Write '%1'").arg(Qt.application.name)
        checked: root.currentWriteHeaderGenerator
        prefWidth: root.width

        onToggled: state => {
            root.currentWriteHeaderGenerator = state;
        }
    }

    MpvqcSwitchRow {
        id: _nicknameToggle

        label: qsTranslate("ExportSettingsDialog", "Write Nickname")
        checked: root.currentWriteHeaderNickname
        prefWidth: root.width

        onToggled: state => {
            root.currentWriteHeaderNickname = state;
        }
    }

    MpvqcSwitchRow {
        id: _pathToggle

        label: qsTranslate("ExportSettingsDialog", "Write Video Path")
        checked: root.currentWriteHeaderVideoPath
        prefWidth: root.width

        onToggled: state => {
            root.currentWriteHeaderVideoPath = state;
        }
    }

    Item {
        Layout.fillWidth: true
        Layout.fillHeight: true
    }
}
