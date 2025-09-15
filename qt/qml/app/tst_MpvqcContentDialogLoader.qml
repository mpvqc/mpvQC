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
    name: "MpvqcContentDialogLoader"

    Component {
        id: signalSpy

        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcContentDialogLoader {}
    }

    function makeControl(): Item {
        const control = createTemporaryObject(objectUnderTest, testCase, {
            mpvqcApplication: {
                contentItem: testCase,
                height: testCase.height,
                width: testCase.width,
                mpvqcSettings: {
                    nickname: "nickname",
                    writeHeaderDate: true,
                    writeHeaderGenerator: true,
                    writeHeaderNickname: true,
                    writeHeaderVideoPath: true,
                    importWhenVideoLinkedInDocument: 0,
                    themeIdentifier: "Material You Dark",
                    themeColorOption: 4,
                    backupEnabled: false,
                    backupInterval: 15,
                    commentTypes: ["Comment Type"]
                },
                mpvqcTheme: {
                    availableThemes: [
                        {
                            name: "name",
                            preview: "blue"
                        }
                    ],
                    control: "blue",
                    rowHighlight: "blue",
                    getForeground: arg => "blue",
                    getBackground: arg => "blue"
                },
                mpvqcApplicationPathsPyObject: {
                    dir_backup: Qt.resolvedUrl("qmldir")
                },
                mpvqcUtilityPyObject: {
                    urlToAbsolutePath: arg => ""
                },
                mpvqcPlayerFilesPyObject: {
                    input_conf_url: Qt.resolvedUrl("qmldir"),
                    mpv_conf_url: Qt.resolvedUrl("qmldir")
                },
                LayoutMirroring: {
                    enabled: false
                }
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

        control.openAboutDialog();
        waitUntilLoaded(control);
        control.item.close();

        tryVerify(() => !control.item, 1000);
        compare(spy.count, 1);
    }
}
