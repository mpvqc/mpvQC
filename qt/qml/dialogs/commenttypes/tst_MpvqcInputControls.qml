// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtTest

MpvqcInputControls {
    id: objectUnderTest

    readonly property string badWord: "bad word"
    readonly property string goodWord: "good word"
    readonly property string exampleError: `Text includes "${badWord}"`

    focusTextFieldOnCompletion: false
    mpvqcApplication: QtObject {
        property var mpvqcTheme: QtObject {
            property color control: "purple"
        }
    }

    validateInput: text => {
        if (text.includes(badWord)) {
            return exampleError;
        }
    }

    width: 400
    height: 400

    TestCase {
        name: "MpvqcInputControls"
        when: windowShown

        SignalSpy {
            id: acceptedSpy
            target: objectUnderTest
            signalName: "accepted"
        }
        SignalSpy {
            id: doneSpy
            target: objectUnderTest
            signalName: "done"
        }

        function cleanup() {
            acceptedSpy.clear();
            doneSpy.clear();
            objectUnderTest.textField.focus = true;
        }

        function test_initial() {
            const o = objectUnderTest;
            verify(!o.acceptButton.enabled);
            verify(!o.rejectButton.enabled);
        }

        function test_validAccept() {
            const o = objectUnderTest;

            o.textField.text = o.goodWord;
            verify(o.acceptButton.enabled);
            verify(o.rejectButton.enabled);

            mouseClick(o.acceptButton);
            compare(acceptedSpy.count, 1);
            compare(doneSpy.count, 1);
            verify(!o.acceptButton.enabled);
            verify(!o.rejectButton.enabled);
        }

        function test_validReject() {
            const o = objectUnderTest;

            o.textField.text = o.goodWord;
            verify(o.acceptButton.enabled);
            verify(o.rejectButton.enabled);

            mouseClick(o.rejectButton);
            compare(acceptedSpy.count, 0);
            compare(doneSpy.count, 1);
            verify(!o.acceptButton.enabled);
            verify(!o.rejectButton.enabled);
        }

        function test_invalidAccept() {
            const o = objectUnderTest;

            o.textField.text = o.badWord;
            verify(!o.acceptButton.enabled);
            verify(o.rejectButton.enabled);

            mouseClick(o.acceptButton);
            compare(acceptedSpy.count, 0);
            compare(doneSpy.count, 0);
            verify(!o.acceptButton.enabled);
            verify(o.rejectButton.enabled);
        }

        function test_invalidReject() {
            const o = objectUnderTest;

            o.textField.text = o.badWord;
            verify(!o.acceptButton.enabled);
            verify(o.rejectButton.enabled);

            mouseClick(o.rejectButton);
            compare(acceptedSpy.count, 0);
            compare(doneSpy.count, 1);
            verify(!o.acceptButton.enabled);
            verify(!o.rejectButton.enabled);
        }

        function test_validThenInvalidThenValid() {
            const o = objectUnderTest;

            o.text = o.goodWord;
            verify(o.acceptButton.enabled);
            verify(o.rejectButton.enabled);

            o.text = o.badWord;
            verify(!o.acceptButton.enabled);
            verify(o.rejectButton.enabled);

            o.text = o.goodWord;
            verify(o.acceptButton.enabled);
            verify(o.rejectButton.enabled);
        }
    }
}
