// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls
import QtTest

import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcPlatform"

    readonly property MpvqcTestBridge bridge: MpvqcTestBridge {}

    // Attached properties resolve only in the scope they attach to, so every
    // object whose Window.window a test reads carries it as a plain property.
    readonly property var _hostWindow: Window.window

    function makePopup(): Popup {
        const popup = createTemporaryObject(_popupProbe, testCase);
        verify(popup);
        return popup;
    }

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
                drawsDropShadow: false,
                preferredPopupType: Popup.Window
            },
            {
                tag: "linux-desktop",
                arrangement: "linux-desktop",
                keepsNativeFrame: false,
                drawsDropShadow: true,
                preferredPopupType: Popup.Item
            },
            {
                tag: "linux-tiling",
                arrangement: "linux-tiling",
                keepsNativeFrame: false,
                drawsDropShadow: false,
                preferredPopupType: Popup.Item
            },
            {
                tag: "headless",
                arrangement: "headless",
                keepsNativeFrame: false,
                drawsDropShadow: false,
                preferredPopupType: Popup.Item
            }
        ];
    }

    function test_arrangement(data): void {
        bridge.switchPlatformArrangement(data.arrangement);

        compare(MpvqcPlatform.keepsNativeFrame, data.keepsNativeFrame);
        compare(MpvqcPlatform.drawsDropShadow, data.drawsDropShadow);
        compare(MpvqcPlatform.preferredPopupType, data.preferredPopupType);
    }

    function test_openedPopup_data(): var {
        return [
            {
                tag: "windows-separate-window",
                arrangement: "windows",
                separateWindow: true
            },
            {
                tag: "linux-desktop-in-scene",
                arrangement: "linux-desktop",
                separateWindow: false
            }
        ];
    }

    function test_openedPopup(data): void {
        bridge.switchPlatformArrangement(data.arrangement);

        const popup = makePopup();
        popup.open();
        tryVerify(() => popup.opened);

        verify(popup.contentItem.popupWindow);
        compare(popup.contentItem.popupWindow !== testCase._hostWindow, data.separateWindow);
    }

    function test_resetReturnsToHeadless(): void {
        bridge.switchPlatformArrangement("windows");
        verify(MpvqcPlatform.keepsNativeFrame);

        bridge.resetState();

        verify(!MpvqcPlatform.keepsNativeFrame);
        verify(!MpvqcPlatform.drawsDropShadow);
    }

    Component {
        id: _popupProbe

        Popup {
            width: 50
            height: 50
            popupType: MpvqcPlatform.preferredPopupType

            contentItem: Item {
                readonly property var popupWindow: Window.window
            }
        }
    }
}
