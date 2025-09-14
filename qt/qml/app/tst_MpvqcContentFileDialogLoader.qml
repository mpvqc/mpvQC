// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtTest
import QtQuick

TestCase {
    id: testCase

    width: 1280
    height: 720
    visible: true
    when: windowShown
    name: "MpvqcContentFileDialogLoader"

    Component {
        id: signalSpy

        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcContentFileDialogLoader {
            cleanupDelay: 0
        }
    }

    function makeControl(): Item {
        const control = createTemporaryObject(objectUnderTest, testCase, {
            mpvqcApplication: {
                mpvqcSettings: {
                    lastDirectoryDocuments: Qt.resolvedUrl(""),
                    lastDirectorySubtitles: Qt.resolvedUrl(""),
                    lastDirectoryVideo: Qt.resolvedUrl("")
                },
                mpvqcUtilityPyObject: {
                    subtitleFileGlobPattern: ""
                }
            }
        });
        verify(control);
        return control;
    }

    function waitUntilLoaded(control: Item): void {
        tryVerify(() => control.item);
        tryVerify(() => control.item.visible);
    }

    function test_open_data() {
        const probe = makeControl();
        const names = [];
        for (const k of Object.keys(probe)) {
            if (typeof probe[k] === "function" && k.startsWith("open") && k.endsWith("Dialog")) {
                names.push(k);
            }
        }
        probe.destroy();
        names.sort();

        const rows = [];
        for (const name of names) {
            const core = name.slice(4, -6);
            const tag = core.charAt(0).toLowerCase() + core.slice(1);

            rows.push({
                tag: tag,
                methodName: name,
                exec: control => control[name]()
            });
        }

        return rows;
    }

    function test_open(data) {
        const control = makeControl();
        data.exec(control);
        waitUntilLoaded(control);
    }

    function test_close_clears_item() {
        const control = makeControl();

        const spy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: "dialogClosed"
        });
        verify(spy);

        control.openImportQcDocumentsDialog();
        waitUntilLoaded(control);
        control.item.close();

        tryVerify(() => !control.item, 1000);
        compare(spy.count, 1);
    }
}
