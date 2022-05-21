/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick
import Qt.labs.platform
import pyobjects
import settings
import "MpvqcDocumentExporter.mjs" as MpvqcDocumentExporter


QtObject {
    required property url currentVideo

    property url currentDocument: ''
    property var commentModel: undefined

    function requestSave() {
        if (currentDocument != '') {
            _save(currentDocument)
        } else {
            requestSaveAs()
        }
    }

    function _save(url) {
        const payload = _generateDocumentPayload(url)
        FileIoPyObject.write(url, payload)
        currentDocument = url
    }

    function _generateDocumentPayload(documentUrl) {
        const data = {
            date: new Date().toLocaleString(Qt.locale(MpvqcSettings.language)),
            generator: `${Qt.application.name} ${Qt.application.version}`,
            nickname: MpvqcSettings.nickname,
            videoPath: currentVideo ? FileIoPyObject.abs_path_of(currentVideo) : '',
            comments: commentModel.comments(),
        }
        const settings = {
            writeHeader: MpvqcSettings.writeHeader,
            writeHeaderDate: MpvqcSettings.writeHeaderDate,
            writeHeaderGenerator: MpvqcSettings.writeHeaderGenerator,
            writeHeaderNickname: MpvqcSettings.writeHeaderNickname,
            writeHeaderVideoPath: MpvqcSettings.writeHeaderVideoPath,
        }
        return MpvqcDocumentExporter.generateDocumentFrom(data, settings)
    }

    function requestSaveAs() {
        const url = "qrc:/qml/components/dialogs/MpvqcExportDocumentDialog.qml"
        const component = Qt.createComponent(url)
        const dialog = component.createObject(appWindow)
        dialog.currentFolder = _generateFilePathProposal()
        dialog.savePressed.connect(_save)
        dialog.open()
    }

    function _generateFilePathProposal() {
        const directory = currentVideo != ''
            ? FileIoPyObject.parent_of(currentVideo)
            : StandardPaths.writableLocation(StandardPaths.DocumentsLocation)
        const videoName = currentVideo != ''
            ? FileIoPyObject.stem_of(currentVideo)
            : qsTranslate("FileInteractionDialogs", "untitled")
        const fileProposal = MpvqcSettings.appendNickname
            ? `[QC]_${videoName}_${MpvqcSettings.nickname}.txt`
            : `[QC]_${videoName}.txt`
        return `${directory}/${fileProposal}`
    }

}
