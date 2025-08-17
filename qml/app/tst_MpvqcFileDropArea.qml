/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

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
