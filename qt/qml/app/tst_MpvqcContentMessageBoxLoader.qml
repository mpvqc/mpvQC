// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtTest
import QtQuick

TestCase {
    id: testCase

    property var arguments: ({
            openExtendedExportFailedMessageBox: ["message", 1],
            openDocumentNotCompatibleMessageBox: [["doc1", "doc2"]]
        })

    width: 1280
    height: 720
    visible: true
    when: windowShown
    name: "MpvqcContentMessageBoxLoader"

    Component {
        id: signalSpy

        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcContentMessageBoxLoader {}
    }

    function makeControl(): Item {
        const control = createTemporaryObject(objectUnderTest, testCase, {
            mpvqcApplication: {
                contentItem: testCase,
                height: testCase.height,
                width: testCase.width
            }
        });
        verify(control);
        return control;
    }

    function waitUntilLoaded(control: Item): void {
        tryVerify(() => control.item);
        waitForRendering(control.item?.contentItem);
    }

    function test_open_data() {
        const probe = makeControl();
        const names = [];
        for (const k of Object.keys(probe)) {
            if (typeof probe[k] === "function" && k.startsWith("open") && k.endsWith("MessageBox")) {
                names.push(k);
            }
        }
        probe.destroy();
        names.sort();

        const rows = [];
        for (const name of names) {
            const core = name.slice(4, -10);
            const tag = core.charAt(0).toLowerCase() + core.slice(1);

            const row = {
                tag: tag,
                methodName: name,
                exec: null
            };

            switch (name) {
            case "openVersionCheckMessageBox":
                row.exec = control => {
                    control.setSource(control.messageBoxVersionCheck, {
                        controller: {
                            title: "title",
                            text: "text"
                        }
                    });
                    control.active = true;
                };
                break;
            default:
                row.exec = control => {
                    const args = testCase.arguments[name];
                    if (args) {
                        control[name](...testCase.arguments[name]);
                    } else {
                        control[name]();
                    }
                };
                break;
            }

            rows.push(row);
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
            signalName: "messageBoxClosed"
        });
        verify(spy);

        control.openExtendedExportsMessageBox();
        waitUntilLoaded(control);
        control.item.close();

        tryVerify(() => !control.item, 1000);
        compare(spy.count, 1);
    }
}
