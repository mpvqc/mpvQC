// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

QtObject {
    id: root

    property string passedValue: "initial"
    property int openCalls: 0
    property bool aliveAfterEmission: false

    signal closed
    signal accepted
    signal rejected

    function open(): void {
        openCalls += 1;
    }

    function emitTrigger(signalName: string): void {
        if (signalName === "closed") {
            root.closed();
        } else if (signalName === "accepted") {
            root.accepted();
        } else if (signalName === "rejected") {
            root.rejected();
        } else {
            throw new Error(`unknown trigger signal: ${signalName}`);
        }
        aliveAfterEmission = true;
    }
}
