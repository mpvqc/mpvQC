// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtTest

import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase
    name: "MpvqcPlatform"

    readonly property MpvqcTestBridge bridge: MpvqcTestBridge {}

    function init(): void {
        bridge.resetState();
    }

    function cleanup(): void {
        bridge.switchPlatformArrangement("headless");
    }

    function test_arrangement_data(): var {
        return [
            {
                tag: "windows",
                arrangement: "windows",
                keepsNativeFrame: true,
                drawsDropShadow: false
            },
            {
                tag: "linux-desktop",
                arrangement: "linux-desktop",
                keepsNativeFrame: false,
                drawsDropShadow: true
            },
            {
                tag: "linux-tiling",
                arrangement: "linux-tiling",
                keepsNativeFrame: false,
                drawsDropShadow: false
            },
            {
                tag: "headless",
                arrangement: "headless",
                keepsNativeFrame: false,
                drawsDropShadow: false
            }
        ];
    }

    function test_arrangement(data): void {
        bridge.switchPlatformArrangement(data.arrangement);

        compare(MpvqcPlatform.keepsNativeFrame, data.keepsNativeFrame);
        compare(MpvqcPlatform.drawsDropShadow, data.drawsDropShadow);
    }

    function test_resetReturnsToHeadless(): void {
        bridge.switchPlatformArrangement("windows");
        verify(MpvqcPlatform.keepsNativeFrame);

        bridge.resetState();

        verify(!MpvqcPlatform.keepsNativeFrame);
        verify(!MpvqcPlatform.drawsDropShadow);
    }
}
