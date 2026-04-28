// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

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

    function test_newQcDocumentWhenSaved_resetsDirectly(): void {
        const control = it.makeControl();
        verify(it.bridge.saved, "expected initial state to be saved");

        it.menu.trigger(control, "fileMenu", "newQcDocumentMenuItem");

        const messageBoxLoader = it.find.messageBoxLoader(control);
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
        it.comment.add(control, "Translation", "");
        tryVerify(() => !it.bridge.saved);

        it.menu.trigger(control, "fileMenu", "newQcDocumentMenuItem");

        const messageBox = it.find.openedDialog(control, "resetMessageBox");

        const button = messageBox.standardButton(data.button);
        verify(button, "dialog button not found");
        mouseClick(button);

        it.expect.commentCount(control, data.remainingComments);
        tryVerify(() => it.bridge.saved === data.expectedSaved);
    }

    function test_openQcDocument_data() {
        return [
            {
                tag: "accepted",
                interact: dialog => {
                    dialog.selectedFile = it.bridge.importArtifact("qc_document_basic.txt");
                    it.dialog.accept(dialog);
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

        it.menu.trigger(control, "fileMenu", "openQcDocumentsMenuItem");

        const dialog = it.find.openedDialog(control, "importDocumentsFileDialog");

        data.interact(dialog);

        it.expect.commentCount(control, data.expectedComments);
    }

    function test_openQcDocument_incompatibleDocument_opensNotCompatibleMessageBox(): void {
        const control = it.makeControl();

        it.menu.trigger(control, "fileMenu", "openQcDocumentsMenuItem");

        const dialog = it.find.openedDialog(control, "importDocumentsFileDialog");
        dialog.selectedFile = it.bridge.importArtifact("qc_document_invalid.txt");
        it.dialog.accept(dialog);

        const messageBox = it.find.openedDialog(control, "documentNotCompatibleMessageBox");
        verify(messageBox.text.includes("qc_document_invalid.txt"));
        it.expect.commentCount(control, 0);
    }

    function test_openQcDocument_complex_promptsThenLoadsVideoAndSubtitles(): void {
        const control = it.makeControl();

        it.menu.trigger(control, "fileMenu", "openQcDocumentsMenuItem");

        const dialog = it.find.openedDialog(control, "importDocumentsFileDialog");
        dialog.selectedFile = it.bridge.importComplexDocument();
        it.dialog.accept(dialog);

        const confirmation = it.find.openedDialog(control, "importConfirmationDialog");

        const videoList = findChild(confirmation, "videoListView");
        const subtitleList = findChild(confirmation, "subtitleListView");
        compare(videoList.count, 2, "expected one video plus skip option");
        compare(subtitleList.count, 2);

        confirmation.accept();
        it.bridge.waitForBackgroundJobs();

        it.expect.commentCount(control, 2);
        tryVerify(() => it.bridge.openedVideoName() === "video.mp4");
        tryVerify(() => it.bridge.openedSubtitleCount() === 2);
    }

    function test_openQcDocument_complex_rejectingConfirmationSkipsVideoAndSubtitles(): void {
        const control = it.makeControl();

        it.menu.trigger(control, "fileMenu", "openQcDocumentsMenuItem");

        const dialog = it.find.openedDialog(control, "importDocumentsFileDialog");
        dialog.selectedFile = it.bridge.importComplexDocument();
        it.dialog.accept(dialog);

        const confirmation = it.find.openedDialog(control, "importConfirmationDialog");
        confirmation.reject();
        it.bridge.waitForBackgroundJobs();

        it.expect.commentCount(control, 2);
        compare(it.bridge.openedVideoName(), "", "no video should be opened");
        compare(it.bridge.openedSubtitleCount(), 0, "no subtitles should be opened");
    }

    function test_saveQcDocument_promptsThenSavesDirectly(): void {
        const control = it.makeControl();
        it.comment.add(control, "Translation", "hello");

        it.menu.trigger(control, "fileMenu", "saveQcDocumentMenuItem");

        const dialog = it.find.openedDialog(control, "saveDocumentFileDialog");

        const savePath = it.bridge.tempSavePath();
        dialog.selectedFile = savePath;
        it.dialog.accept(dialog);

        tryVerify(() => it.bridge.saved);
        verify(it.bridge.fileContains(savePath, "Translation"), "first save should write Translation");
        verify(it.bridge.fileContains(savePath, "hello"), "first save should write the typed comment");

        it.comment.add(control, "Spelling", "world");

        it.menu.trigger(control, "fileMenu", "saveQcDocumentMenuItem");

        const fileDialogLoader = it.find.fileDialogLoader(control);
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
        it.comment.add(control, "Translation", "hello");

        it.menu.trigger(control, "fileMenu", "saveQcDocumentAsMenuItem");

        const firstDialog = it.find.openedDialog(control, "saveDocumentFileDialog");
        const firstPath = it.bridge.tempSavePath();
        firstDialog.selectedFile = firstPath;
        it.dialog.accept(firstDialog);

        tryVerify(() => it.bridge.saved);
        verify(it.bridge.fileContains(firstPath, "hello"));

        tryVerify(() => !findChild(control, "saveDocumentFileDialog"));

        it.comment.add(control, "Spelling", "world");

        it.menu.trigger(control, "fileMenu", "saveQcDocumentAsMenuItem");

        const secondDialog = it.find.openedDialog(control, "saveDocumentFileDialog");
        const secondPath = it.bridge.tempSavePath();
        secondDialog.selectedFile = secondPath;
        it.dialog.accept(secondDialog);

        verify(it.bridge.fileContains(secondPath, "hello"), "second save should contain hello");
        verify(it.bridge.fileContains(secondPath, "world"), "second save should contain world");
        verify(it.bridge.fileContains(firstPath, "hello"), "first file should still contain hello");
        verify(!it.bridge.fileContains(firstPath, "world"), "first file should not contain world");
    }

    function test_extendedExport_writesFileUsingTemplate(): void {
        const control = it.makeControl();
        const sentinel = "extended-export-payload";
        it.comment.add(control, "Translation", sentinel);

        it.menu.triggerSubItemByText(control, "fileMenu", "exportQcDocumentMenu", "working");

        const dialog = it.find.openedDialog(control, "exportDocumentFileDialog");
        const savePath = it.bridge.tempSavePath();
        dialog.selectedFile = savePath;
        it.dialog.accept(dialog);

        verify(it.bridge.fileContains(savePath, sentinel), "exported file should contain comment text");
    }

    function test_extendedExport_brokenTemplate_opensErrorMessageBox(): void {
        const control = it.makeControl();
        it.comment.add(control, "Translation", "extended-export-payload");

        it.menu.triggerSubItemByText(control, "fileMenu", "exportQcDocumentMenu", "error");

        const dialog = it.find.openedDialog(control, "exportDocumentFileDialog");
        dialog.selectedFile = it.bridge.tempSavePath();
        it.dialog.accept(dialog);

        it.find.openedDialog(control, "extendedExportErrorMessageBox");
    }

    function test_exitMpvqcEmitsCloseRequested(): void {
        const control = it.makeControl();
        const spy = it.makeSpy(control, "closeRequested");

        it.menu.trigger(control, "fileMenu", "exitMpvqcMenuItem");

        tryVerify(() => spy.count === 1);
    }
}
