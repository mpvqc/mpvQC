// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

Loader {
    id: root

    enum TeardownTrigger {
        Closed,
        AcceptedOrRejected
    }

    property int teardownTrigger: MpvqcOverlayLoader.TeardownTrigger.Closed

    // Teardown must never destroy the item while the signal that triggered it
    // is still mid-emission. Delay 0 is safe: the Loader releases its item with
    // a deferred delete. Items that need to outlive their trigger signal for
    // longer set a positive delay, which routes teardown through a timer.
    property int teardownDelay: 0

    signal closed

    function open(overlay: url, properties: var): void {
        _teardownTimer.stop();
        setSource(overlay, properties ?? {});
        active = true;
    }

    function _requestTeardown(): void {
        if (teardownDelay > 0) {
            _teardownTimer.restart();
        } else {
            _teardown();
        }
    }

    function _teardown(): void {
        active = false;
        source = "";
        closed();
    }

    asynchronous: true
    active: false
    visible: status === Loader.Ready

    onLoaded: item.open() // qmllint disable

    Connections {
        enabled: root.teardownTrigger === MpvqcOverlayLoader.TeardownTrigger.Closed
        target: root.item
        ignoreUnknownSignals: true

        function onClosed(): void {
            root._requestTeardown();
        }
    }

    Connections {
        enabled: root.teardownTrigger === MpvqcOverlayLoader.TeardownTrigger.AcceptedOrRejected
        target: root.item
        ignoreUnknownSignals: true

        function onAccepted(): void {
            root._requestTeardown();
        }

        function onRejected(): void {
            root._requestTeardown();
        }
    }

    Timer {
        id: _teardownTimer

        interval: root.teardownDelay

        onTriggered: root._teardown()
    }
}
