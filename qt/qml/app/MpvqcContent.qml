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

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import "../footer"
import "../header"
import "../player"
import "../table"

Page {
    id: root

    required property var mpvqcApplication
    required property MpvqcAppHeaderController headerController

    readonly property var mpvqcExtendedDocumentExporterPyObject: mpvqcApplication.mpvqcExtendedDocumentExporterPyObject
    readonly property var mpvqcManager: mpvqcApplication.mpvqcManager
    readonly property var mpvqcMpvPlayerPropertiesPyObject: mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject
    readonly property var mpvqcMpvPlayerPyObject: mpvqcApplication.mpvqcMpvPlayerPyObject
    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    readonly property var mpvqcUtilityPyObject: mpvqcApplication.mpvqcUtilityPyObject
    readonly property var supportedSubtitleFileExtensions: mpvqcUtilityPyObject.subtitleFileExtensions

    readonly property int commentCount: _mpvqcCommentTable.commentCount

    signal appWindowSizeRequested(width: int, height: int)
    signal disableFullScreenRequested
    signal toggleFullScreenRequested

    function focusCommentTable(): void {
        _mpvqcCommentTable.forceActiveFocus();
    }

    QtObject {
        id: _impl

        readonly property int minContainerHeight: 200
        readonly property int minContainerWidth: 500
        readonly property real defaultSplitRatio: 0.4

        function applySaneDefaultSplitViewSize(): void {
            const prefHeight = _splitView.height * defaultSplitRatio;
            const prefWidth = _splitView.width * defaultSplitRatio;
            _tableContainer.setPreferredSizes(prefWidth, prefHeight);
        }

        function resizeVideoToOriginalResolution(): void {
            _videoResizer.recalculateSizes();
        }

        function isPreventReachingMpvCustomCommand(key: int, modifiers: int): bool {
            const noModifier = modifiers === Qt.NoModifier;
            const ctrlModifier = modifiers & Qt.ControlModifier;

            return key === Qt.Key_Up  //
            || key === Qt.Key_Down //
            || (key === Qt.Key_Return && noModifier) //
            || (key === Qt.Key_Escape && noModifier) //
            || (key === Qt.Key_Delete && noModifier) //
            || (key === Qt.Key_Backspace && noModifier) //
            || (key === Qt.Key_F && ctrlModifier) //
            || (key === Qt.Key_C && ctrlModifier) //
            || (key === Qt.Key_Z && ctrlModifier);
        }

        function handleMpvCustomCommand(key: int, modifiers: int): void {
            root.mpvqcMpvPlayerPyObject.handle_key_event(key, modifiers);
        }

        function pausePlayer(): void {
            root.mpvqcMpvPlayerPyObject.pause();
        }

        function openNewCommentMenu(): void {
            _commentMenu.popup();
        }

        function addNewEmptyComment(commentType: string): void {
            _mpvqcCommentTable.addNewComment(commentType);
        }

        function requestToggleFullScreen(): void {
            root.toggleFullScreenRequested();
        }

        function requestDisableFullScreen(): void {
            root.disableFullScreenRequested();
        }

        function requestResizeAppWindow(width: int, height: int): void {
            root.appWindowSizeRequested(width, height);
        }

        function saveExtendedDocument(document: url, template: url): void {
            root.mpvqcExtendedDocumentExporterPyObject.export(document, template);
        }

        function resetState(): void {
            root.mpvqcManager.reset();
        }
    }

    Keys.onEscapePressed: {
        _impl.requestDisableFullScreen();
    }

    Keys.onPressed: event => {
        const key = event.key;
        const modifiers = event.modifiers;
        const plainPress = !event.isAutoRepeat && modifiers === Qt.NoModifier;

        if (key === Qt.Key_E && plainPress) {
            _impl.openNewCommentMenu();
            return;
        }

        if (key === Qt.Key_F && plainPress) {
            _impl.requestToggleFullScreen();
            return;
        }

        if (_impl.isPreventReachingMpvCustomCommand(key, modifiers)) {
            return;
        }

        _impl.handleMpvCustomCommand(key, modifiers);
    }

    SplitView {
        id: _splitView

        readonly property int tableContainerHeight: _tableContainer.height
        readonly property int tableContainerWidth: _tableContainer.width
        readonly property int draggerHeight: _splitView.height - _player.height - tableContainerHeight
        readonly property int draggerWidth: _splitView.width - _player.width - tableContainerWidth

        focus: true
        anchors.fill: root.contentItem
        orientation: root.mpvqcSettings.layoutOrientation

        MpvqcPlayer {
            id: _player

            mpvPlayer: root.mpvqcMpvPlayerPyObject
            isFullScreen: root.mpvqcApplication.fullscreen

            SplitView.minimumHeight: _impl.minContainerHeight
            SplitView.minimumWidth: _impl.minContainerWidth
            SplitView.fillHeight: true
            SplitView.fillWidth: true

            onAddNewCommentMenuRequested: {
                _impl.openNewCommentMenu();
            }

            onToggleFullScreenRequested: {
                _impl.requestToggleFullScreen();
            }
        }

        Column {
            id: _tableContainer

            visible: !root.mpvqcApplication.fullscreen

            SplitView.minimumHeight: _impl.minContainerHeight
            SplitView.minimumWidth: _impl.minContainerWidth

            function setPreferredSizes(width: int, height: int): void {
                SplitView.preferredWidth = width;
                SplitView.preferredHeight = height;
            }

            MpvqcTable {
                id: _mpvqcCommentTable

                mpvqcApplication: root.mpvqcApplication
                focus: true
                width: _tableContainer.width
                height: _tableContainer.height - _footer.height

                onCommentCountChanged: {
                    // we effectively force a redraw of the table here. if we don't do this and delete the last row
                    // in the table, the table will not rerender completely and there might be color artifacts of the
                    // alternating row colors
                    _footer.height += 1;
                    _footer.height -= 1;
                }
            }

            MpvqcFooter {
                id: _footer

                mpvqcApplication: root.mpvqcApplication
                width: _tableContainer.width

                selectedCommentIndex: _mpvqcCommentTable.selectedCommentIndex
                totalCommentCount: _mpvqcCommentTable.commentCount
            }
        }
    }

    MpvqcFileDropArea {
        anchors.fill: _splitView
        supportedSubtitleFileExtensions: root.supportedSubtitleFileExtensions

        onFilesDropped: (documents, videos, subtitles) => {
            root.mpvqcManager.open(documents, videos, subtitles);
        }
    }

    MpvqcNewCommentMenu {
        id: _commentMenu

        commentTypes: root.mpvqcSettings.commentTypes

        function _adjustPosition(): void {
            const isMirrored = root.mpvqcApplication.LayoutMirroring.enabled;
            const global = root.mpvqcUtilityPyObject.cursorPosition;
            const local = _commentMenu.parent.mapFromGlobal(global);
            _commentMenu.x = isMirrored ? local.x - width : local.x;
            _commentMenu.y = local.y;
        }

        onAboutToShow: {
            _adjustPosition();
            _impl.pausePlayer();
        }

        onCommentTypeChosen: commentType => {
            _impl.requestDisableFullScreen();
            _impl.addNewEmptyComment(commentType);
        }
    }

    MpvqcResizeHandler {
        id: _videoResizer

        headerHeight: root.header.height
        appBorderSize: root.mpvqcApplication.windowBorder
        videoWidth: root.mpvqcMpvPlayerPropertiesPyObject.scaledWidth
        videoHeight: root.mpvqcMpvPlayerPropertiesPyObject.scaledHeight

        isAppFullScreen: root.mpvqcApplication.fullscreen
        isAppMaximized: root.mpvqcApplication.maximized
        videoPath: root.mpvqcMpvPlayerPropertiesPyObject.path

        splitViewOrientation: _splitView.orientation
        splitViewHandleWidth: _splitView.draggerWidth
        splitViewHandleHeight: _splitView.draggerHeight
        splitViewTableContainerWidth: _splitView.tableContainerWidth
        splitViewTableContainerHeight: _splitView.tableContainerHeight

        onAppWindowSizeRequested: (width, height) => {
            _impl.requestResizeAppWindow(width, height);
        }

        onSplitViewTableSizeRequested: (width, height) => {
            _tableContainer.setPreferredSizes(width, height);
        }
    }

    Connections {
        target: root.headerController

        function onResetAppStateRequested(): void {
            if (root.mpvqcManager.saved) {
                _impl.resetState();
            } else {
                _messageBoxLoader.openNewDocumentMessageBox();
            }
        }

        function onOpenQcDocumentsRequested(): void {
            _fileDialogLoader.openImportQcDocumentsDialog();
        }

        function onSaveQcDocumentsRequested(): void {
            root.mpvqcManager.save();
        }

        function onSaveQcDocumentsAsRequested(): void {
            root.mpvqcManager.saveAs();
        }

        function onExtendedExportRequested(name: string, path: url): void {
            const proposal = root.mpvqcUtilityPyObject.generate_file_path_proposal();
            _fileDialogLoader.openExtendedDocumentExportDialog(proposal, path);
        }

        function onOpenVideoRequested(): void {
            _fileDialogLoader.openImportVideoDialog();
        }

        function onOpenSubtitlesRequested(): void {
            _fileDialogLoader.openImportSubtitlesDialog();
        }

        function onResizeVideoRequested(): void {
            _impl.resizeVideoToOriginalResolution();
        }

        function onAppearanceDialogRequested(): void {
            _dialogLoader.openAppearanceDialog();
        }

        function onCommentTypesDialogRequested(): void {
            _dialogLoader.openCommentTypesDialog();
        }

        function onWindowTitleFormatConfigured(updatedValue): void {
            root.mpvqcSettings.windowTitleFormat = updatedValue;
        }

        function onApplicationLayoutConfigured(updatedValue): void {
            root.mpvqcSettings.layoutOrientation = updatedValue;
        }

        function onBackupSettingsDialogRequested(): void {
            _dialogLoader.openBackupSettingsDialog();
        }

        function onExportSettingsDialogRequested(): void {
            _dialogLoader.openExportSettingsDialog();
        }

        function onImportSettingsDialogRequested(): void {
            _dialogLoader.openImportSettingsDialog();
        }

        function onEditMpvConfigDialogRequested(): void {
            _dialogLoader.openEditMpvDialog();
        }

        function onEditInputConfigDialogRequested(): void {
            _dialogLoader.openEditInputDialog();
        }

        function onLanguageConfigured(updatedLanguageIdentifier: string): void {
            root.mpvqcSettings.language = updatedLanguageIdentifier;
        }

        function onUpdateDialogRequested(): void {
            _messageBoxLoader.openVersionCheckMessageBox();
        }

        function onKeyboardShortcutsDialogRequested(): void {
            _dialogLoader.openShortcutsDialog();
        }

        function onExtendedExportDialogRequested(): void {
            _messageBoxLoader.openExtendedExportsMessageBox();
        }

        function onAboutDialogRequested(): void {
            _dialogLoader.openAboutDialog();
        }
    }

    MpvqcContentDialogLoader {
        id: _dialogLoader

        mpvqcApplication: root.mpvqcApplication

        onDialogClosed: {
            root.focusCommentTable();
        }
    }

    Loader {
        id: _fileDialogLoader

        readonly property url importQcDocumentsDialog: Qt.resolvedUrl("../dialogs/MpvqcDialogImportDocuments.qml")
        readonly property url importVideoDialog: Qt.resolvedUrl("../dialogs/MpvqcDialogImportVideo.qml")
        readonly property url importSubtitlesDialog: Qt.resolvedUrl("../dialogs/MpvqcDialogImportSubtitles.qml")
        readonly property url exportQcDocumentDialog: Qt.resolvedUrl("../dialogs/MpvqcDialogExportDocument.qml")

        asynchronous: true
        active: false
        visible: active

        function openImportQcDocumentsDialog(): void {
            setSource(importQcDocumentsDialog, {
                mpvqcApplication: root.mpvqcApplication
            });
            active = true;
        }

        function openExtendedDocumentExportDialog(proposal: url, exportTemplate: url): void {
            setSource(exportQcDocumentDialog, {
                isExtendedExport: true,
                selectedFile: proposal,
                exportTemplate: exportTemplate
            });
            active = true;
        }

        function openImportVideoDialog(): void {
            setSource(importVideoDialog, {
                mpvqcApplication: root.mpvqcApplication
            });
            active = true;
        }

        function openImportSubtitlesDialog(): void {
            setSource(importSubtitlesDialog, {
                mpvqcApplication: root.mpvqcApplication
            });
            active = true;
        }

        onLoaded: item.open() // qmllint disable

        Connections {
            enabled: _fileDialogLoader.item
            target: _fileDialogLoader.item
            ignoreUnknownSignals: true

            function onAccepted(): void {
                _delayCleanupTimer.restart();
            }

            function onRejected(): void {
                _delayCleanupTimer.restart();
            }

            function onExtendedSavePressed(document: url, template: url): void {
                _impl.saveExtendedDocument(document, template);
            }
        }

        Timer {
            id: _delayCleanupTimer

            interval: 250

            onTriggered: {
                _fileDialogLoader.active = false;
                _fileDialogLoader.source = "";
                root.focusCommentTable();
            }
        }
    }

    Loader {
        id: _messageBoxLoader

        readonly property url messageBoxExtendedExport: Qt.resolvedUrl("../dialogs/MpvqcMessageBoxExtendedExport.qml")
        readonly property url messageBoxExtendedExportFailed: Qt.resolvedUrl("../dialogs/MpvqcMessageBoxExtendedExportError.qml")
        readonly property url messageBoxNewDocument: Qt.resolvedUrl("../dialogs/MpvqcMessageBoxNewDocument.qml")
        readonly property url messageBoxVersionCheck: Qt.resolvedUrl("../dialogs/MpvqcMessageBoxVersionCheck.qml")

        asynchronous: true
        active: false
        visible: active

        function openExtendedExportFailedMessageBox(message: string, lineNr: int): void {
            setSource(messageBoxExtendedExportFailed, {
                mpvqcApplication: root.mpvqcApplication,
                errorMessage: message,
                errorLine: lineNr
            });
            active = true;
        }

        function openCheckForUpdateMessageBox(): void {
            setSource(messageBoxVersionCheck, {
                mpvqcApplication: root.mpvqcApplication
            });
            active = true;
        }

        function openExtendedExportsMessageBox(): void {
            setSource(messageBoxExtendedExport, {
                mpvqcApplication: root.mpvqcApplication
            });
            active = true;
        }

        function openVersionCheckMessageBox(): void {
            setSource(messageBoxVersionCheck, {
                mpvqcApplication: root.mpvqcApplication
            });
            active = true;
        }

        function openNewDocumentMessageBox(): void {
            setSource(messageBoxNewDocument, {
                mpvqcApplication: root.mpvqcApplication
            });
            active = true;
        }

        onLoaded: item.open() // qmllint disable

        Connections {
            enabled: _messageBoxLoader.item
            target: _messageBoxLoader.item

            function onResetDocumentConfirmedByUser(): void {
                _impl.resetState();
            }

            function onClosed(): void {
                _messageBoxLoader.active = false;
                _messageBoxLoader.source = "";
                root.focusCommentTable();
            }
        }
    }

    Connections {
        target: root.mpvqcExtendedDocumentExporterPyObject

        function onErrorOccurred(message: string, line: int): void {
            _messageBoxLoader.openExtendedExportFailedMessageBox(message, line);
        }
    }

    Component.onCompleted: {
        _impl.applySaneDefaultSplitViewSize();
    }
}
