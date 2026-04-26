// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest
import pyobjects

TestCase {
    id: testCase

    name: "Integration::FileMenu"
    width: 1280
    height: 720
    visible: true
    when: windowShown

    TestHelpers {
        id: it

        testCase: testCase
    }

    function init(): void {
        it.resetState();
    }

    function triggerExportTemplate(control: Item, templateName: string): void {
        const fileMenu = findChild(control, "fileMenu");
        verify(fileMenu, "fileMenu not found");
        fileMenu.open();
        tryVerify(() => fileMenu.opened);

        const submenu = findChild(fileMenu, "exportQcDocumentMenu");
        verify(submenu, "exportQcDocumentMenu not found");
        submenu.open();
        tryVerify(() => submenu.opened);

        let item = null;
        for (let i = 0; i < submenu.count; i++) {
            const candidate = submenu.itemAt(i);
            if (candidate && candidate.text === templateName) {
                item = candidate;
                break;
            }
        }
        verify(item, `template ${templateName} not found`);
        mouseClick(item);
        tryVerify(() => !submenu.opened);
    }

    function test_newQcDocumentWhenSaved_resetsDirectly(): void {
        const control = it.makeControl();
        verify(it.bridge.saved, "expected initial state to be saved");

        it.triggerMenuItem(control, "fileMenu", "newQcDocumentMenuItem");

        const messageBoxLoader = findChild(control, "messageBoxLoader");
        verify(messageBoxLoader, "messageBoxLoader not found");
        verify(!messageBoxLoader.active, "no confirmation expected when state is saved");
    }

    function test_newQcDocumentWhenUnsaved_data() {
        return [
            {
                tag: "accepted",
                button: Dialog.Yes,
                remainingComments: 0,
                expectedSaved: true
            },
            {
                tag: "denied",
                button: Dialog.No,
                remainingComments: 1,
                expectedSaved: false
            },
        ];
    }

    function test_newQcDocumentWhenUnsaved(data): void {
        const control = it.makeControl();
        it.addComment(control, "Translation", "");
        tryVerify(() => !it.bridge.saved);

        it.triggerMenuItem(control, "fileMenu", "newQcDocumentMenuItem");

        const messageBox = it.findOpenedDialog(control, "resetMessageBox");

        const button = messageBox.standardButton(data.button);
        verify(button, "dialog button not found");
        mouseClick(button);

        const tableView = findChild(control, "tableView");
        tryVerify(() => tableView.commentCount === data.remainingComments);
        tryVerify(() => it.bridge.saved === data.expectedSaved);
    }

    function test_openQcDocument_data() {
        return [
            {
                tag: "accepted",
                interact: dialog => {
                    dialog.selectedFile = it.bridge.importArtifact("qc_document_basic.txt");
                    it.acceptDialog(dialog);
                },
                expectedComments: 2
            },
            {
                tag: "rejected",
                interact: dialog => dialog.reject(),
                expectedComments: 0
            },
        ];
    }

    function test_openQcDocument(data): void {
        const control = it.makeControl();

        it.triggerMenuItem(control, "fileMenu", "openQcDocumentsMenuItem");

        const dialog = it.findOpenedDialog(control, "importDocumentsFileDialog");

        data.interact(dialog);

        const tableView = findChild(control, "tableView");
        verify(tableView, "tableView not found");
        tryVerify(() => tableView.commentCount === data.expectedComments);
    }

    function test_openQcDocument_incompatibleDocument_opensNotCompatibleMessageBox(): void {
        const control = it.makeControl();

        it.triggerMenuItem(control, "fileMenu", "openQcDocumentsMenuItem");

        const dialog = it.findOpenedDialog(control, "importDocumentsFileDialog");
        dialog.selectedFile = it.bridge.importArtifact("qc_document_invalid.txt");
        it.acceptDialog(dialog);

        const messageBox = it.findOpenedDialog(control, "documentNotCompatibleMessageBox");
        verify(messageBox.text.includes("qc_document_invalid.txt"));

        const tableView = findChild(control, "tableView");
        verify(tableView, "tableView not found");
        compare(tableView.commentCount, 0, "no comments should be imported from an invalid document");
    }

    function test_openQcDocument_complex_promptsThenLoadsVideoAndSubtitles(): void {
        const control = it.makeControl();

        it.triggerMenuItem(control, "fileMenu", "openQcDocumentsMenuItem");

        const dialog = it.findOpenedDialog(control, "importDocumentsFileDialog");
        dialog.selectedFile = it.bridge.importComplexDocument();
        it.acceptDialog(dialog);

        const confirmation = it.findOpenedDialog(control, "importConfirmationDialog");

        const videoList = findChild(confirmation, "videoListView");
        const subtitleList = findChild(confirmation, "subtitleListView");
        compare(videoList.count, 2, "expected one video plus skip option");
        compare(subtitleList.count, 2);

        confirmation.accept();
        it.bridge.waitForBackgroundJobs();

        const tableView = findChild(control, "tableView");
        tryVerify(() => tableView.commentCount === 2);
        tryVerify(() => it.bridge.openedVideoName() === "video.mp4");
        tryVerify(() => it.bridge.openedSubtitleCount() === 2);
    }

    function test_openQcDocument_complex_rejectingConfirmationSkipsVideoAndSubtitles(): void {
        const control = it.makeControl();

        it.triggerMenuItem(control, "fileMenu", "openQcDocumentsMenuItem");

        const dialog = it.findOpenedDialog(control, "importDocumentsFileDialog");
        dialog.selectedFile = it.bridge.importComplexDocument();
        it.acceptDialog(dialog);

        const confirmation = it.findOpenedDialog(control, "importConfirmationDialog");
        confirmation.reject();
        it.bridge.waitForBackgroundJobs();

        const tableView = findChild(control, "tableView");
        tryVerify(() => tableView.commentCount === 2);
        compare(it.bridge.openedVideoName(), "", "no video should be opened");
        compare(it.bridge.openedSubtitleCount(), 0, "no subtitles should be opened");
    }

    function test_saveQcDocument_promptsThenSavesDirectly(): void {
        const control = it.makeControl();
        it.addComment(control, "Translation", "hello");

        it.triggerMenuItem(control, "fileMenu", "saveQcDocumentMenuItem");

        const dialog = it.findOpenedDialog(control, "saveDocumentFileDialog");

        const savePath = it.bridge.tempSavePath();
        dialog.selectedFile = savePath;
        it.acceptDialog(dialog);

        tryVerify(() => it.bridge.saved);
        verify(it.bridge.fileContains(savePath, "Translation"), "first save should write Translation");
        verify(it.bridge.fileContains(savePath, "hello"), "first save should write the typed comment");

        it.addComment(control, "Spelling", "world");

        it.triggerMenuItem(control, "fileMenu", "saveQcDocumentMenuItem");

        const fileDialogLoader = findChild(control, "fileDialogLoader");
        verify(fileDialogLoader, "fileDialogLoader not found");
        verify(!fileDialogLoader.active, "no save dialog expected once document path is known");

        it.bridge.waitForBackgroundJobs();
        verify(it.bridge.fileContains(savePath, "Translation"), "direct save should preserve Translation");
        verify(it.bridge.fileContains(savePath, "hello"), "direct save should preserve hello");
        verify(it.bridge.fileContains(savePath, "Spelling"), "direct save should add Spelling");
        verify(it.bridge.fileContains(savePath, "world"), "direct save should add world");
    }

    function test_saveQcDocumentAs_alwaysPromptsForPath(): void {
        const control = it.makeControl();
        it.addComment(control, "Translation", "hello");

        it.triggerMenuItem(control, "fileMenu", "saveQcDocumentAsMenuItem");

        const firstDialog = it.findOpenedDialog(control, "saveDocumentFileDialog");
        const firstPath = it.bridge.tempSavePath();
        firstDialog.selectedFile = firstPath;
        it.acceptDialog(firstDialog);

        tryVerify(() => it.bridge.saved);
        verify(it.bridge.fileContains(firstPath, "hello"));

        tryVerify(() => !findChild(control, "saveDocumentFileDialog"));

        it.addComment(control, "Spelling", "world");

        it.triggerMenuItem(control, "fileMenu", "saveQcDocumentAsMenuItem");

        const secondDialog = it.findOpenedDialog(control, "saveDocumentFileDialog");
        const secondPath = it.bridge.tempSavePath();
        secondDialog.selectedFile = secondPath;
        it.acceptDialog(secondDialog);

        verify(it.bridge.fileContains(secondPath, "hello"), "second save should contain hello");
        verify(it.bridge.fileContains(secondPath, "world"), "second save should contain world");
        verify(it.bridge.fileContains(firstPath, "hello"), "first file should still contain hello");
        verify(!it.bridge.fileContains(firstPath, "world"), "first file should not contain world");
    }

    function test_extendedExport_writesFileUsingTemplate(): void {
        const control = it.makeControl();
        const sentinel = "extended-export-payload";
        it.addComment(control, "Translation", sentinel);

        triggerExportTemplate(control, "working");

        const dialog = it.findOpenedDialog(control, "exportDocumentFileDialog");
        const savePath = it.bridge.tempSavePath();
        dialog.selectedFile = savePath;
        it.acceptDialog(dialog);

        verify(it.bridge.fileContains(savePath, sentinel), "exported file should contain comment text");
    }

    function test_extendedExport_brokenTemplate_opensErrorMessageBox(): void {
        const control = it.makeControl();
        it.addComment(control, "Translation", "extended-export-payload");

        triggerExportTemplate(control, "error");

        const dialog = it.findOpenedDialog(control, "exportDocumentFileDialog");
        dialog.selectedFile = it.bridge.tempSavePath();
        it.acceptDialog(dialog);

        it.findOpenedDialog(control, "extendedExportErrorMessageBox");
    }

    function test_exitMpvqcEmitsCloseRequested(): void {
        const control = it.makeControl();
        const spy = it.makeSpy(control, "closeRequested");

        it.triggerMenuItem(control, "fileMenu", "exitMpvqcMenuItem");

        tryVerify(() => spy.count === 1);
    }
}
