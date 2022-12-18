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

import dialogs
import settings


QtObject {
    id: root

    required property var mpvqcApplication
    property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    property var mpvqcFileSystemHelperPyObject: mpvqcApplication.mpvqcFileSystemHelperPyObject

    property var messageDialog: MpvqcMessageDialogImportFoundVideoConfirmation {
        property url linkedVideo: ''

        onAccepted: {
            positive()
        }

        function positive(): void {
            root.pick(linkedVideo)
        }

        onRejected: {
            negative()
        }

        function negative(): void {
            root.pickNothing()
        }
    }

    signal videoSelected(url video)

    /** Every call to this function MUST trigger a 'videoSelected' signal. */
    function chooseBetween(standaloneVideo: url, otherVideosPotentially: Array<MpvqcImportSuccess>): void {
        if (isVideoPresent(standaloneVideo)) {
            pick(standaloneVideo)
            return
        }
        if (userNeverWantsToImportLinkedVideo()) {
            pickNothing()
            return
        }
        const linkedVideo = findFirstExistingVideoFrom(otherVideosPotentially)
        if (!isVideoPresent(linkedVideo)) {
            pickNothing()
            return
        }
        if (userAlwaysWantsToImportLinkedVideo()) {
            pick(linkedVideo)
            return
        }
        consultUserToPossiblyPick(linkedVideo)
    }

    function isVideoPresent(video: url): void {
        return video && video != ''
    }

    function pick(video: url): void {
        root.videoSelected(video)
    }

    function userNeverWantsToImportLinkedVideo(): bool {
        return mpvqcSettings.importWhenVideoLinkedInDocument === MpvqcSettings.ImportWhenVideoLinkedInDocument.NEVER
    }

    function pickNothing(): void {
        root.videoSelected('')
    }

    function findFirstExistingVideoFrom(successful: Array<MpvqcImportSuccess>): url {
        for (const document of successful) {
            const videoPath = document.video
            const url = mpvqcFileSystemHelperPyObject.absolute_path_to_url(videoPath)
            if (mpvqcFileSystemHelperPyObject.url_is_file(url)) {
                return url
            }
        }
        return ''
    }

    function userAlwaysWantsToImportLinkedVideo(): bool {
        return mpvqcSettings.importWhenVideoLinkedInDocument === MpvqcSettings.ImportWhenVideoLinkedInDocument.ALWAYS
    }

    function consultUserToPossiblyPick(linkedVideo: url): void {
        messageDialog.linkedVideo = linkedVideo
        messageDialog.open()
    }

}
