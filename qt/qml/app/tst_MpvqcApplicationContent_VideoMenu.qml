// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    name: "MpvqcApplicationContent::VideoMenu"
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

        it.menu.trigger(control, "videoMenu", "openVideoMenuItem");

        const dialog = it.find.openedDialog(control, "importVideoFileDialog");
        dialog.selectedFile = it.bridge.importArtifact("video_basic.mp4");

        it.dialog.accept(dialog);

        tryVerify(() => it.bridge.openedVideoName() === "video_basic.mp4");
    }

    function test_openSubtitles_loadsSubtitleIntoPlayer(): void {
        const control = it.makeControl();

        it.menu.trigger(control, "videoMenu", "openSubtitlesMenuItem");

        const dialog = it.find.openedDialog(control, "importSubtitlesFileDialog");
        dialog.selectedFile = it.bridge.importArtifact("subtitle_basic.ass");
        it.dialog.accept(dialog);

        tryVerify(() => it.bridge.openedSubtitleCount() === 1);
    }

    function test_openSubtitles_complex_promptsThenLoadsVideoAndSubtitle(): void {
        const control = it.makeControl();

        it.menu.trigger(control, "videoMenu", "openSubtitlesMenuItem");

        const dialog = it.find.openedDialog(control, "importSubtitlesFileDialog");
        dialog.selectedFile = it.bridge.importArtifact("subtitle_complex.ass");
        it.dialog.accept(dialog);

        const confirmation = it.find.openedDialog(control, "importConfirmationDialog");

        const videoList = findChild(confirmation, "videoListView");
        const subtitleList = findChild(confirmation, "subtitleListView");
        compare(videoList.count, 2, "expected one video plus skip option");
        compare(subtitleList.count, 1);

        confirmation.accept();
        it.bridge.waitForBackgroundJobs();

        tryVerify(() => it.bridge.openedVideoName() === "video_basic.mp4");
        tryVerify(() => it.bridge.openedSubtitleCount() === 1);
    }

    function test_resizeVideo_emitsAppWindowSizeRequested(): void {
        const control = it.makeControl();
        const spy = it.makeSpy(control, "appWindowSizeRequested");

        it.menu.trigger(control, "videoMenu", "resizeVideoMenuItem");

        tryVerify(() => spy.count === 1);
        compare(spy.signalArguments[0][0], 800);
        compare(spy.signalArguments[0][1], 600);
    }
}
