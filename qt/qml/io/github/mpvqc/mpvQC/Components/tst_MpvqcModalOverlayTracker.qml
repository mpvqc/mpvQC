// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcModalOverlayTracker"

    function makeTracker(properties = {}): MpvqcModalOverlayTracker {
        const tracker = createTemporaryObject(trackerFactory, testCase, properties);
        verify(tracker);
        return tracker;
    }

    function cleanup(): void {
        verify(!MpvqcModalState.anyModalOverlayOpen);
    }

    function test_closedTrackerDoesNotCount(): void {
        makeTracker({
            open: false
        });
        verify(!MpvqcModalState.anyModalOverlayOpen);
    }

    function test_openAtCreationCounts(): void {
        const tracker = makeTracker({
            open: true
        });
        verify(MpvqcModalState.anyModalOverlayOpen);

        tracker.open = false;
        verify(!MpvqcModalState.anyModalOverlayOpen);
    }

    function test_toggleCountsOnceEachWay(): void {
        const tracker = makeTracker({
            open: false
        });

        tracker.open = true;
        verify(MpvqcModalState.anyModalOverlayOpen);

        tracker.open = true;
        tracker.open = false;
        verify(!MpvqcModalState.anyModalOverlayOpen);
    }

    function test_overlappingTrackers(): void {
        const first = makeTracker({
            open: true
        });
        const second = makeTracker({
            open: true
        });
        verify(MpvqcModalState.anyModalOverlayOpen);

        first.open = false;
        verify(MpvqcModalState.anyModalOverlayOpen);

        second.open = false;
        verify(!MpvqcModalState.anyModalOverlayOpen);
    }

    function test_destructionWhileOpenReleases(): void {
        const tracker = makeTracker({
            open: true
        });
        verify(MpvqcModalState.anyModalOverlayOpen);

        tracker.destroy();
        tryVerify(() => !MpvqcModalState.anyModalOverlayOpen);
    }

    Component {
        id: trackerFactory

        MpvqcModalOverlayTracker {}
    }
}
