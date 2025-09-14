// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtTest
import QtQuick

TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcFileDropArea"

    Component {
        id: signalSpy

        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcFileDropArea {
            supportedSubtitleFileExtensions: ["ass"]
        }
    }

    function test_enter() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        let accepted = false;
        control.handleEnter({
            formats: ["text/uri-list"],
            hasUrls: true,
            accept: () => {
                accepted = true;
            }
        });
        verify(accepted);

        accepted = false;
        control.handleEnter({
            formats: [],
            hasUrls: true
        });
        verify(!accepted);
    }

    function test_drop() {
        let control;

        control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        let spy = createTemporaryObject(signalSpy, control, {
            target: control,
            signalName: "filesDropped"
        });
        verify(spy);

        control.handleDrop({
            formats: ["text/uri-list"],
            hasUrls: true,
            urls: ["file:///document.txt", "file:///video.mp4", "file:///subtitle.ass"]
        });

        function validateCase1() {
            compare(spy.count, 1);
            let [documents, videos, subtitles] = spy.signalArguments[0];
            compare(documents, ["file:///document.txt"]);
            compare(videos, ["file:///video.mp4"]);
            compare(subtitles, ["file:///subtitle.ass"]);
        }

        validateCase1();

        //

        control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        spy = createTemporaryObject(signalSpy, control, {
            target: control,
            signalName: "filesDropped"
        });
        verify(spy);

        control.handleDrop({
            formats: ["text/uri-list"],
            hasUrls: true,
            urls: ["file:///document.txt", "file:///video.mp4", "file:///subtitle.ass-not"]
        });

        function validateCase2() {
            compare(spy.count, 1);
            let [documents, videos, subtitles] = spy.signalArguments[0];
            compare(documents, ["file:///document.txt"]);
            compare(videos, ["file:///video.mp4", "file:///subtitle.ass-not"]);
            compare(subtitles, []);
        }

        validateCase2();
    }
}
