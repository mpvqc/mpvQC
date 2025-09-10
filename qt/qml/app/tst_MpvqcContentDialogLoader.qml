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

    width: 1280
    height: 720
    visible: true
    when: windowShown
    name: "MpvqcContentDialogLoader"

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
                mpvqcMpvPlayerPropertiesPyObject: {
                    mpv_version: "",
                    ffmpeg_version: ""
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
        control.openAboutDialog();
        waitUntilLoaded(control);
        control.item.close();
        tryVerify(() => !control.item, 1000);
    }
}
