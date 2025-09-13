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
 *
 */

import QtQuick
import QtTest

TestCase {
    id: testCase

    visible: false
    name: "MpvqcContentController"

    Component {
        id: signalSpy

        SignalSpy {}
    }

    function withSpy(target, signalName, invokeFn) {
        const spy = createTemporaryObject(signalSpy, testCase, {
            target,
            signalName
        });
        verify(spy, "Failed to create SignalSpy for " + signalName);
        invokeFn(spy);
        return spy;
    }

    Component {
        id: objectUnderTest

        MpvqcContentController {
            mpvqcMpvPlayerPyObject: QtObject {
                property int pauseCount: 0
                property var lastKey
                property var lastModifiers
                function pause() {
                    pauseCount += 1;
                }
                function handle_key_event(key, modifiers) {
                    lastKey = key;
                    lastModifiers = modifiers;
                }
            }

            mpvqcManager: QtObject {
                property int openCount: 0
                property var lastOpenDocuments
                property var lastOpenVideos
                property var lastOpenSubtitles
                property int resetCount: 0
                property int saveCount: 0
                property int saveAsCount: 0

                function open(documents, videos, subtitles) {
                    openCount += 1;
                    lastOpenDocuments = documents;
                    lastOpenVideos = videos;
                    lastOpenSubtitles = subtitles;
                }
                function reset() {
                    resetCount += 1;
                }
                function save() {
                    saveCount += 1;
                }
                function saveAs() {
                    saveAsCount += 1;
                }
            }

            mpvqcExtendedDocumentExporterPyObject: QtObject {
                property int performExportCount: 0
                property url lastDocumentUrl
                property url lastTemplateUrl
                function performExport(documentUrl, templateUrl) {
                    performExportCount += 1;
                    lastDocumentUrl = documentUrl;
                    lastTemplateUrl = templateUrl;
                }
            }

            mpvqcSettings: QtObject {
                property int layoutOrientation: Qt.Vertical
                property string windowTitleFormat: ""
                property string language: "en"
            }
        }
    }

    function test_onKeyPressed_data() {
        return [
            {
                tag: "request-comment-menu",
                key: Qt.Key_E,
                modifiers: Qt.NoModifier,
                isAutoRepeat: false,
                expected: {
                    commentMenuRequestedCount: 1,
                    fullScreenRequestedCount: 0,
                    passThrough: false
                }
            },
            {
                tag: "request-fullscreen-toggle",
                key: Qt.Key_F,
                modifiers: Qt.NoModifier,
                isAutoRepeat: false,
                expected: {
                    commentMenuRequestedCount: 0,
                    fullScreenRequestedCount: 1,
                    passThrough: false
                }
            },
            {
                tag: "prevent-key-press",
                key: Qt.Key_Return,
                modifiers: Qt.NoModifier,
                isAutoRepeat: false,
                expected: {
                    commentMenuRequestedCount: 0,
                    fullScreenRequestedCount: 0,
                    passThrough: false
                }
            },
            {
                tag: "pass-through-key-press-1",
                key: Qt.Key_Return,
                modifiers: Qt.ControlModifier,
                isAutoRepeat: false,
                expected: {
                    commentMenuRequestedCount: 0,
                    fullScreenRequestedCount: 0,
                    passThrough: true
                }
            },
            {
                tag: "pass-through-key-press-2",
                key: Qt.Key_B,
                modifiers: Qt.NoModifier,
                isAutoRepeat: false,
                expected: {
                    commentMenuRequestedCount: 0,
                    fullScreenRequestedCount: 0,
                    passThrough: true
                }
            },
        ];
    }

    function test_onKeyPressed(data) {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        const newCommentRequestedSpy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: "openNewCommentMenuRequested"
        });
        const fullscreenRequestedSpy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: "toggleFullScreenRequested"
        });
        verify(newCommentRequestedSpy);
        verify(fullscreenRequestedSpy);

        control.onKeyPressed(data.key, data.modifiers, data.isAutoRepeat);

        compare(newCommentRequestedSpy.count, data.expected.commentMenuRequestedCount);
        compare(fullscreenRequestedSpy.count, data.expected.fullScreenRequestedCount);

        if (data.expected.passThrough) {
            compare(control.mpvqcMpvPlayerPyObject.lastKey, data.key);
            compare(control.mpvqcMpvPlayerPyObject.lastModifiers, data.modifiers);
        } else {
            compare(control.mpvqcMpvPlayerPyObject.lastKey, undefined);
            compare(control.mpvqcMpvPlayerPyObject.lastModifiers, undefined);
        }
    }

    function test_requestDisableFullScreen() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        withSpy(control, "disableFullScreenRequested", spy => {
            control.requestDisableFullScreen();
            compare(spy.count, 1);
        });
    }

    function test_requestToggleFullScreen() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        withSpy(control, "toggleFullScreenRequested", spy => {
            control.requestToggleFullScreen();
            compare(spy.count, 1);
        });
    }

    function test_requestResizeAppWindow() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        withSpy(control, "appWindowSizeRequested", spy => {
            const w = 1280, h = 720;
            control.requestResizeAppWindow(w, h);

            compare(spy.count, 1);
            const args = spy.signalArguments[0];
            compare(args.length, 2);
            compare(args[0], w);
            compare(args[1], h);
        });
    }

    function test_pausePlayer() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        compare(control.mpvqcMpvPlayerPyObject.pauseCount, 0);
        control.pausePlayer();
        compare(control.mpvqcMpvPlayerPyObject.pauseCount, 1);
    }

    function test_addNewEmptyComment() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        withSpy(control, "addNewCommentRequested", spy => {
            const commentType = "myCommentType";
            control.addNewEmptyComment(commentType);
            compare(spy.count, 1);
            const args = spy.signalArguments[0];
            compare(args.length, 1);
            compare(args[0], commentType);
        });
    }

    function test_saveExtendedDocument_calls_performExport() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        const doc = "file:///tmp/document.json";
        const tpl = "file:///tmp/template.html";

        compare(control.mpvqcExtendedDocumentExporterPyObject.performExportCount, 0);
        control.saveExtendedDocument(doc, tpl);

        compare(control.mpvqcExtendedDocumentExporterPyObject.performExportCount, 1);
        compare(control.mpvqcExtendedDocumentExporterPyObject.lastDocumentUrl, doc);
        compare(control.mpvqcExtendedDocumentExporterPyObject.lastTemplateUrl, tpl);
    }

    function test_openDroppedFiles() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        const documents = ["file:///d1", "file:///d2"];
        const videos = ["file:///v1"];
        const subtitles = ["file:///s1", "file:///s2"];

        compare(control.mpvqcManager.openCount, 0);
        control.openDroppedFiles(documents, videos, subtitles);

        compare(control.mpvqcManager.openCount, 1);
        compare(control.mpvqcManager.lastOpenDocuments, documents);
        compare(control.mpvqcManager.lastOpenVideos, videos);
        compare(control.mpvqcManager.lastOpenSubtitles, subtitles);
    }

    function test_preferredSplitSizes() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        const r = control.preferredSplitSizes(1000, 800);
        compare(r.width, 400);
        compare(r.height, 320);
    }

    function test_resetAppState() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        compare(control.mpvqcManager.resetCount, 0);
        control.resetAppState();
        compare(control.mpvqcManager.resetCount, 1);
    }

    function test_save() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        compare(control.mpvqcManager.saveCount, 0);
        control.save();
        compare(control.mpvqcManager.saveCount, 1);
    }

    function test_saveAs() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        compare(control.mpvqcManager.saveAsCount, 0);
        control.saveAs();
        compare(control.mpvqcManager.saveAsCount, 1);
    }

    function test_setWindowTitleFormat() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        compare(control.mpvqcSettings.windowTitleFormat, "");
        const v = "mpvQC — %FILENAME%";
        control.setWindowTitleFormat(v);
        compare(control.mpvqcSettings.windowTitleFormat, v);
    }

    function test_setApplicationLayout() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        compare(control.mpvqcSettings.layoutOrientation, Qt.Vertical);
        control.setApplicationLayout(Qt.Horizontal);
        compare(control.mpvqcSettings.layoutOrientation, Qt.Horizontal);
    }

    function test_setLanguage() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        compare(control.mpvqcSettings.language, "en");
        control.setLanguage("de");
        compare(control.mpvqcSettings.language, "de");
    }
}
