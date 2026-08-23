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
        bridge.switchPlatform("headless");
    }

    function test_platformCapabilities_data(): var {
        return [
            {
                tag: "windows",
                platform: "windows",
                keepsNativeFrame: true,
                canDrawOwnFrame: false,
                preferredPopupType: Popup.Window
            },
            {
                tag: "linux-desktop",
                platform: "linux-desktop",
                keepsNativeFrame: false,
                canDrawOwnFrame: true,
                preferredPopupType: Popup.Item
            },
            {
                tag: "linux-tiling",
                platform: "linux-tiling",
                keepsNativeFrame: false,
                canDrawOwnFrame: false,
                preferredPopupType: Popup.Item
            },
            {
                tag: "headless",
                platform: "headless",
                keepsNativeFrame: false,
                canDrawOwnFrame: false,
                preferredPopupType: Popup.Item
            }
        ];
    }

    function test_platformCapabilities(data): void {
        bridge.switchPlatform(data.platform);

        compare(MpvqcPlatform.keepsNativeFrame, data.keepsNativeFrame);
        compare(MpvqcPlatform.canDrawOwnFrame, data.canDrawOwnFrame);
        compare(MpvqcPlatform.preferredPopupType, data.preferredPopupType);
    }

    function test_openedPopup_data(): var {
        return [
            {
                tag: "windows-separate-window",
                platform: "windows",
                separateWindow: true
            },
            {
                tag: "linux-desktop-in-scene",
                platform: "linux-desktop",
                separateWindow: false
            }
        ];
    }

    function test_openedPopup(data): void {
        bridge.switchPlatform(data.platform);

        const popup = makePopup();
        popup.open();
        tryVerify(() => popup.opened);

        verify(popup.contentItem.popupWindow);
        compare(popup.contentItem.popupWindow !== testCase._hostWindow, data.separateWindow);
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
