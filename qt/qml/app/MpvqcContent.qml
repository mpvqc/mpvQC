/*
 * Copyright (C) 2022 mpvQC developers
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
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

    MpvqcContentController {
        id: _controller

        mpvqcMpvPlayerPyObject: root.mpvqcMpvPlayerPyObject
        mpvqcManager: root.mpvqcApplication.mpvqcManager
        mpvqcExtendedDocumentExporterPyObject: root.mpvqcExtendedDocumentExporterPyObject
        mpvqcSettings: root.mpvqcSettings

        onToggleFullScreenRequested: root.toggleFullScreenRequested()

        onDisableFullScreenRequested: root.disableFullScreenRequested()

        onAppWindowSizeRequested: (width, height) => root.appWindowSizeRequested(width, height)

        onOpenNewCommentMenuRequested: _commentMenu.popup()

        onAddNewCommentRequested: commentType => _mpvqcCommentTable.addNewComment(commentType)

        onSplitViewTableSizeRequested: (width, height) => _tableContainer.setPreferredSizes(width, height)
    }

    Keys.onEscapePressed: _controller.requestDisableFullScreen()

    Keys.onPressed: event => _controller.onKeyPressed(event.key, event.modifiers, event.isAutoRepeat)

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

            SplitView.minimumHeight: _controller.minContainerHeight
            SplitView.minimumWidth: _controller.minContainerWidth
            SplitView.fillHeight: true
            SplitView.fillWidth: true

            onAddNewCommentMenuRequested: _controller.openNewCommentMenuRequested()

            onToggleFullScreenRequested: _controller.requestToggleFullScreen()
        }

        Column {
            id: _tableContainer

            visible: !root.mpvqcApplication.fullscreen

            SplitView.minimumHeight: _controller.minContainerHeight
            SplitView.minimumWidth: _controller.minContainerWidth

            function setPreferredSizes(width, height) {
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
                    // force a redraw to avoid leftover alternating row color artifacts
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
            _controller.openDroppedFiles(documents, videos, subtitles);
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
            _controller.pausePlayer();
        }

        onCommentTypeChosen: commentType => {
            _controller.requestDisableFullScreen();
            _controller.addNewEmptyComment(commentType);
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
            _controller.requestResizeAppWindow(width, height);
        }

        onSplitViewTableSizeRequested: (width, height) => {
            _tableContainer.setPreferredSizes(width, height);
        }
    }

    Connections {
        target: root.headerController

        function onResetAppStateRequested(): void {
            _controller.resetAppState();
        }

        function onOpenQcDocumentsRequested(): void {
            _fileDialogLoader.openImportQcDocumentsDialog();
        }

        function onSaveQcDocumentsRequested(): void {
            _controller.save();
        }

        function onSaveQcDocumentsAsRequested(): void {
            _controller.saveAs();
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
            _videoResizer.recalculateSizes();
        }

        function onAppearanceDialogRequested(): void {
            _dialogLoader.openAppearanceDialog();
        }

        function onCommentTypesDialogRequested(): void {
            _dialogLoader.openCommentTypesDialog();
        }

        function onWindowTitleFormatConfigured(updatedValue): void {
            _controller.setWindowTitleFormat(updatedValue);
        }

        function onApplicationLayoutConfigured(updatedValue): void {
            _controller.setApplicationLayout(updatedValue);
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

        function onLanguageConfigured(updatedLanguageIdentifier): void {
            _controller.setLanguage(updatedLanguageIdentifier);
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

    MpvqcContentFileDialogLoader {
        id: _fileDialogLoader

        mpvqcApplication: root.mpvqcApplication
        cleanupDelay: 250

        onExtendedDocumentSaved: (document, template) => {
            _controller.saveExtendedDocument(document, template);
        }

        onDialogClosed: {
            root.focusCommentTable();
        }
    }

    MpvqcContentMessageBoxLoader {
        id: _messageBoxLoader

        mpvqcApplication: root.mpvqcApplication

        onMessageBoxClosed: {
            root.focusCommentTable();
        }
    }

    Connections {
        target: root.mpvqcExtendedDocumentExporterPyObject

        function onErrorOccurred(message: string, line: int): void {
            _messageBoxLoader.openExtendedExportFailedMessageBox(message, line);
        }
    }

    Component.onCompleted: {
        const preferred = _controller.preferredSplitSizes(_splitView.width, _splitView.height);
        _tableContainer.setPreferredSizes(preferred.width, preferred.height);
    }
}
