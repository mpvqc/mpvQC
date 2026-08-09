// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    name: "MpvqcApplicationContent::ImportWizardFlow"
    width: 1280
    height: 720
    visible: true
    when: windowShown

    function init(): void {
        it.resetState();
    }

    function test_complexDocument_importsCommentsVideoAndSubtitles(): void {
        const control = it.makeControl();

        it.menu.trigger(control, "fileMenu", "openQcDocumentsMenuItem");

        const fileDialog = it.find.openedDialog(control, "importDocumentsFileDialog");
        fileDialog.viewModel.openDocuments([it.bridge.importComplexDocument()]);
        fileDialog.close();
        it.bridge.waitForBackgroundJobs();

        const wizard = it.wizard.opened(control);

        it.wizard.advance(wizard);
        it.wizard.clickPrimary(wizard);

        tryVerify(() => !wizard.opened);
        it.bridge.waitForBackgroundJobs();

        it.expect.commentCount(control, 2);
        it.expect.openedVideo("video.mp4");
        it.expect.openedSubtitleCount(2);
    }

    function test_complexDocument_cancelDiscardsEverything(): void {
        const control = it.makeControl();

        it.menu.trigger(control, "fileMenu", "openQcDocumentsMenuItem");

        const fileDialog = it.find.openedDialog(control, "importDocumentsFileDialog");
        fileDialog.viewModel.openDocuments([it.bridge.importComplexDocument()]);
        fileDialog.close();
        it.bridge.waitForBackgroundJobs();

        const wizard = it.wizard.opened(control);
        it.wizard.clickCancel(wizard);
        tryVerify(() => !wizard.opened);
        it.bridge.waitForBackgroundJobs();

        it.expect.commentCount(control, 0);
        it.expect.noOpenedVideo();
        it.expect.openedSubtitleCount(0);
    }

    function test_multiVideoDrop_importsTheVideoPickedInTheWizard(): void {
        const control = it.makeControl();

        it.imports.dropFiles(control, it.bridge.importMultiVideoDocuments());

        const wizard = it.wizard.opened(control);
        it.wizard.pickVideo(wizard, 1);
        it.wizard.clickPrimary(wizard);

        tryVerify(() => !wizard.opened);
        it.bridge.waitForBackgroundJobs();

        it.expect.openedVideo("beta.mp4");
    }

    function test_pickingTheSkipEntry_importsCommentsWithoutAVideo(): void {
        const control = it.makeControl();

        it.imports.dropFiles(control, [it.bridge.importVideoOnlyDocument()]);

        const wizard = it.wizard.opened(control);
        it.wizard.pickNoVideo(wizard);
        it.wizard.clickPrimary(wizard);

        tryVerify(() => !wizard.opened);
        it.bridge.waitForBackgroundJobs();

        it.expect.commentCount(control, 1);
        it.expect.noOpenedVideo();
    }

    function test_complexDocument_deselectedSubtitleStaysOut(): void {
        const control = it.makeControl();

        it.imports.dropFiles(control, [it.bridge.importComplexDocument()]);

        const wizard = it.wizard.opened(control);
        it.wizard.advance(wizard);
        it.wizard.pickSubtitle(wizard, 1);
        it.wizard.clickPrimary(wizard);

        tryVerify(() => !wizard.opened);
        it.bridge.waitForBackgroundJobs();

        it.expect.openedSubtitles(["track1.ass"]);
    }

    function test_singleSubtitleDrop_loadsWithoutWizard(): void {
        const control = it.makeControl();

        it.imports.dropFiles(control, [it.bridge.importArtifact("subtitle_basic.ass")]);

        const dialogLoader = it.find.dialogLoader(control);
        verify(!dialogLoader.active, "wizard should not appear for a single explicit subtitle");

        it.expect.openedSubtitleCount(1);
        it.expect.noOpenedVideo();
    }

    function test_explicitSubtitle_getsASubtitlesStepWhenTheVideoIsUnresolved(): void {
        const control = it.makeControl();

        it.imports.dropFiles(control, [it.bridge.importVideoOnlyDocument(), it.bridge.importArtifact("subtitle_basic.ass")]);

        const wizard = it.wizard.opened(control);
        compare(wizard.viewModel.steps.length, 2, "the video question should bring the explicit sub along");

        it.wizard.advance(wizard);
        it.wizard.clickPrimary(wizard);
        tryVerify(() => !wizard.opened);
        it.bridge.waitForBackgroundJobs();

        it.expect.commentCount(control, 1);
        it.expect.openedVideo("video_only.mp4");
        it.expect.openedSubtitleCount(1);
    }

    function test_explicitSubtitle_loadsEvenWhenTheVideoIsSkipped(): void {
        const control = it.makeControl();

        it.imports.dropFiles(control, [it.bridge.importVideoOnlyDocument(), it.bridge.importArtifact("subtitle_basic.ass")]);

        const wizard = it.wizard.opened(control);
        compare(wizard.viewModel.steps.length, 2, "the video question should bring the explicit sub along");

        it.wizard.pickNoVideo(wizard);
        it.wizard.advance(wizard);
        it.wizard.clickPrimary(wizard);

        tryVerify(() => !wizard.opened);
        it.bridge.waitForBackgroundJobs();

        it.expect.noOpenedVideo();
        it.expect.openedSubtitleCount(1);
    }

    function test_secondDragWhileWizardOpen_isIgnored(): void {
        const control = it.makeControl();

        it.imports.dropFiles(control, [it.bridge.importVideoOnlyDocument()]);

        const wizard = it.wizard.opened(control);
        compare(wizard.viewModel.steps.length, 1);

        it.imports.dropFiles(control, [it.bridge.importComplexDocument()]);

        verify(wizard.opened, "wizard should remain open");
        compare(wizard.viewModel.steps.length, 1, "second drop should not replace wizard");
    }

    function test_nativeClose_dismissesAndFreesTheNextImport(): void {
        const control = it.makeControl();
        const dialogLoader = it.find.dialogLoader(control);

        it.imports.dropFiles(control, [it.bridge.importVideoOnlyDocument()]);

        const firstWizard = it.wizard.opened(control);
        compare(firstWizard.viewModel.steps.length, 1);
        firstWizard.reject();
        tryVerify(() => !dialogLoader.active);

        it.imports.dropFiles(control, [it.bridge.importComplexDocument()]);

        const secondWizard = it.wizard.opened(control);
        compare(secondWizard.viewModel.steps.length, 2, "second wizard should reflect complex doc");
    }

    function test_invalidDocument_opensCloseOnlyWizard(): void {
        const control = it.makeControl();

        it.menu.trigger(control, "fileMenu", "openQcDocumentsMenuItem");

        const fileDialog = it.find.openedDialog(control, "importDocumentsFileDialog");
        fileDialog.selectedFile = it.bridge.importArtifact("qc_document_invalid.txt");
        it.dialog.accept(fileDialog);

        const wizard = it.wizard.opened(control);
        verify(!wizard.viewModel.showCancel, "errors-only wizard should not show cancel");

        it.wizard.clickPrimary(wizard);
        tryVerify(() => !wizard.opened);
        it.bridge.waitForBackgroundJobs();

        it.expect.commentCount(control, 0);
        it.expect.noOpenedVideo();
        it.expect.openedSubtitleCount(0);
    }

    TestHelpers {
        id: it

        testCase: testCase
    }
}
