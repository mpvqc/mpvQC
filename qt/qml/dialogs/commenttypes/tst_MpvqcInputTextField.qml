// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtTest

MpvqcInputTextField {
    id: objectUnderTest

    readonly property string badWord: "bad word"
    readonly property string goodWord: "good word"
    readonly property string exampleError: `Text includes "${badWord}"`

    focusOnCompletion: true

    validate: text => {
        if (text.includes(badWord)) {
            return exampleError;
        }
    }

    width: 400
    height: 400

    TestCase {
        name: "MpvqcInputTextField"
        when: windowShown

        SignalSpy {
            id: acceptedSpy
            target: objectUnderTest
            signalName: "acceptedInput"
        }
        SignalSpy {
            id: stoppedSpy
            target: objectUnderTest
            signalName: "editingStopped"
        }

        function cleanup() {
            acceptedSpy.clear();
            stoppedSpy.clear();
            objectUnderTest.error = "";
            objectUnderTest.focus = true;
            objectUnderTest.text = "";
        }

        function test_initial() {
            verify(!objectUnderTest.text);
            verify(!objectUnderTest.error);
            verify(objectUnderTest.focus);
            wait(0);
            verify(objectUnderTest.activeFocus);
        }

        function test_validAccept_data() {
            return [
                {
                    tag: "enter",
                    exec: () => keyClick(Qt.Key_Enter)
                },
                {
                    tag: "from-outside",
                    exec: () => objectUnderTest.accepted()
                },
            ];
        }

        function test_validAccept(data) {
            const o = objectUnderTest;

            o.text = o.goodWord;
            verify(o.hasText);
            compare(o.text, o.goodWord);
            verify(!o.hasError);
            compare(o.error, "");
            verify(o.focus);

            data.exec();
            compare(acceptedSpy.count, 1);
            compare(stoppedSpy.count, 1);
            verify(!o.hasText);
            compare(o.text, "");
            verify(!o.hasError);
            compare(o.error, "");
            verify(!o.focus);
        }

        function test_validReject_data() {
            return [
                {
                    tag: "escape",
                    exec: () => keyClick(Qt.Key_Escape)
                },
                {
                    tag: "from-outside",
                    exec: () => objectUnderTest.rejected()
                },
            ];
        }

        function test_validReject(data) {
            const o = objectUnderTest;

            o.text = o.goodWord;
            verify(o.hasText);
            compare(o.text, o.goodWord);
            verify(!o.hasError);
            compare(o.error, "");
            verify(o.focus);

            data.exec();
            compare(acceptedSpy.count, 0);
            compare(stoppedSpy.count, 1);
            verify(!o.hasText);
            compare(o.text, "");
            verify(!o.hasError);
            compare(o.error, "");
            verify(!o.focus);
        }

        function test_invalidAccept_data() {
            return [
                {
                    tag: "enter",
                    exec: () => keyClick(Qt.Key_Enter)
                },
                {
                    tag: "from-outside",
                    exec: () => objectUnderTest.accepted()
                },
            ];
        }

        function test_invalidAccept(data) {
            const o = objectUnderTest;

            o.text = o.badWord;
            verify(o.hasText);
            compare(o.text, o.badWord);
            verify(o.hasError);
            compare(o.error, o.exampleError);
            verify(o.focus);

            data.exec();
            compare(acceptedSpy.count, 0);
            compare(stoppedSpy.count, 0);
            verify(o.hasText);
            compare(o.text, o.badWord);
            verify(o.hasError);
            compare(o.error, o.exampleError);
            verify(o.focus);
        }

        function test_invalidReject_data() {
            return [
                {
                    tag: "escape",
                    exec: () => keyClick(Qt.Key_Escape)
                },
                {
                    tag: "from-outside",
                    exec: () => objectUnderTest.rejected()
                },
            ];
        }

        function test_invalidReject(data) {
            const o = objectUnderTest;

            o.text = o.badWord;
            verify(o.hasText);
            compare(o.text, o.badWord);
            verify(o.hasError);
            compare(o.error, o.exampleError);
            verify(o.focus);

            data.exec();
            compare(acceptedSpy.count, 0);
            compare(stoppedSpy.count, 1);
            verify(!o.hasText);
            compare(o.text, "");
            verify(!o.hasError);
            compare(o.error, "");
            verify(!o.focus);
        }

        function test_validThenInvalidThenValid() {
            const o = objectUnderTest;

            o.text = o.goodWord;
            verify(!o.hasError);
            compare(o.error, "");

            o.text = o.badWord;
            verify(o.hasError);
            compare(o.error, o.exampleError);

            o.text = o.goodWord;
            verify(!o.hasError);
            compare(o.error, "");
        }
    }
}
