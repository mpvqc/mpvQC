// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest
import pyobjects

TestCase {
    id: testCase

    name: "Integration::VideoMenu"
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

    function test_openVideo_loadsVideoIntoPlayer(): void {
        const control = it.makeControl();

        it.triggerMenuItem(control, "videoMenu", "openVideoMenuItem");

        const dialog = it.findVisibleDialog(control, "importVideoFileDialog");
        dialog.selectedFile = it.bridge.importArtifact("video_basic.mp4");

        it.acceptDialog(dialog);

        tryVerify(() => it.bridge.openedVideoName() === "video_basic.mp4");
    }

    function test_openSubtitles_loadsSubtitleIntoPlayer(): void {
        const control = it.makeControl();

        it.triggerMenuItem(control, "videoMenu", "openSubtitlesMenuItem");

        const dialog = it.findVisibleDialog(control, "importSubtitlesFileDialog");
        dialog.selectedFile = it.bridge.importArtifact("subtitle_basic.ass");
        it.acceptDialog(dialog);

        tryVerify(() => it.bridge.openedSubtitleCount() === 1);
    }

    function test_resizeVideo_emitsAppWindowSizeRequested(): void {
        const control = it.makeControl();
        const spy = it.makeSpy(control, "appWindowSizeRequested");

        it.triggerMenuItem(control, "videoMenu", "resizeVideoMenuItem");

        tryVerify(() => spy.count === 1);
        compare(spy.signalArguments[0][0], 800);
        compare(spy.signalArguments[0][1], 600);
    }

    function test_openSubtitles_complex_promptsThenLoadsVideoAndSubtitle(): void {
        const control = it.makeControl();

        it.triggerMenuItem(control, "videoMenu", "openSubtitlesMenuItem");

        const dialog = it.findVisibleDialog(control, "importSubtitlesFileDialog");
        dialog.selectedFile = it.bridge.importArtifact("subtitle_complex.ass");
        it.acceptDialog(dialog);

        const confirmation = it.findVisibleDialog(control, "importConfirmationDialog");

        const videoList = findChild(confirmation, "videoListView");
        const subtitleList = findChild(confirmation, "subtitleListView");
        compare(videoList.count, 2, "expected one video plus skip option");
        compare(subtitleList.count, 1);

        confirmation.accept();
        it.bridge.waitForBackgroundJobs();

        tryVerify(() => it.bridge.openedVideoName() === "video_basic.mp4");
        tryVerify(() => it.bridge.openedSubtitleCount() === 1);
    }
}
