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
import QtQuick.Controls

import shared


MpvqcDialog {
    id: root

    readonly property var mpvqcMpvFiles: mpvqcApplication.mpvqcMpvFiles
    readonly property var mpvqcResourcePyObject: mpvqcApplication.mpvqcResourcePyObject

    property alias editView: _editView

    contentWidth: Math.min(1080, mpvqcApplication.width * 0.75)
    contentHeight: Math.min(1080, mpvqcApplication.height * 0.75)
    standardButtons: Dialog.Ok | Dialog.Cancel | Dialog.Reset

    MpvqcEditInputView {
        id: _editView

        property string title: qsTranslate("EditInputConf", "Edit input.conf")

        width: root.contentWidth
        mpvqcApplication: root.mpvqcApplication
        fileContent: root.mpvqcMpvFiles.editInputInterface.fileContent
    }

    onAccepted: {
        const currentText = _editView.textArea.text
        root.mpvqcMpvFiles.editInputInterface.fileContent = currentText
    }

    onReset: {
        const defaultText = mpvqcResourcePyObject.get_input_conf_content()
        _editView.textArea.text = defaultText
    }

}
