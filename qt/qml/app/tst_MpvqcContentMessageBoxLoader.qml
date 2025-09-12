/*
 * Copyright (C) 2025 mpvQC developers
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

pragma ComponentBehavior: Bound

import QtTest
import QtQuick

TestCase {
    id: testCase

    property var arguments: ({
            openExtendedExportFailedMessageBox: ["message", 1]
        })

    width: 1280
    height: 720
    visible: true
    when: windowShown
    name: "MpvqcContentMessageBoxLoader"

    QtObject {
        id: _mock

        function check_for_new_version() { /* prevent warnings if theres no such function */
        }
        signal versionChecked(title: string, text: string) // prevent warnings if theres no such signal
    }

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
                width: testCase.width,
                mpvqcVersionCheckerPyObject: _mock
            }
        });
        verify(control);
        return control;
    }

    function waitUntilLoaded(control: Item): void {
        tryVerify(() => control.item);
        waitForRendering(control.item?.contentItem);
        wait(500);
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

            rows.push({
                tag: tag,
                methodName: name,
                exec: control => {
                    const args = testCase.arguments[name];
                    if (args) {
                        control[name](...testCase.arguments[name]);
                    } else {
                        control[name]();
                    }
                }
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
